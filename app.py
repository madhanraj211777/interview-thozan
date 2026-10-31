"""Interview Thozhan - offline, rule-based interview practice demo.

Run with:  streamlit run app.py
No AI models, no API keys, no internet needed (after installing the requirements).
"""
import html as _html
import random
from datetime import datetime
from pathlib import Path

import streamlit as st

import data
import utils

try:  # Plotly is optional; Streamlit's own charts are used as a fallback
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:  # pragma: no cover
    go = None
    HAS_PLOTLY = False

st.set_page_config(page_title="Interview Thozhan", page_icon="🎯", layout="wide", initial_sidebar_state="expanded")

PAGES = ["🏠 Dashboard", "📄 Resume Analyzer", "🎯 Mock Interview", "📊 Performance Report",
         "🧑‍🏫 Career Mentor", "🗺️ Learning Roadmap"]

esc = _html.escape


# =====================================================================
# Small helpers
# =====================================================================
def load_css():
    css_file = Path(__file__).parent / "styles.css"
    try:
        st.markdown(f"<style>{css_file.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
    except OSError:
        st.warning("styles.css was not found, so the default theme is being used.")


def md(html_text):
    """Render HTML on a single line (avoids Markdown turning indented lines into code blocks)."""
    st.markdown(" ".join(line.strip() for line in html_text.splitlines()), unsafe_allow_html=True)


def init_state():
    defaults = {
        "nav": PAGES[0], "sessions": [], "activity": [], "analysis": None, "match": None,
        "resume_text": "", "resume_source": "", "resume_is_sample": False, "jd_text": "",
        "last_upload": None, "upload_error": None, "last_report": None, "report_is_sample": False,
        "demo_loaded": False, "roadmap_done": {}, "iv_stage": "setup", "iv": None,
        "mentor_topic": list(data.MENTOR_TOPICS)[0], "mentor_lang": "English", "roadmap_role": "Python Developer",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def now_label():
    return datetime.now().strftime("%d %b, %H:%M")


def log_activity(text, sample=False):
    st.session_state.activity.append({"text": text, "sample": sample, "time": now_label()})


def chips(items, kind=""):
    if not items:
        return ""
    return "".join(f'<span class="chip {kind}">{esc(str(i))}</span>' for i in items)


def sample_badge(is_sample=True):
    return '<span class="badge sample">Sample demo data</span>' if is_sample else '<span class="badge live">Your data</span>'


def page_header(title, subtitle):
    md(f'<div class="page-title">{esc(title)}</div><div class="page-sub">{esc(subtitle)}</div>')


def empty_state(icon, title, text):
    md(f'<div class="empty"><div class="big">{icon}</div><div class="t">{esc(title)}</div><div>{esc(text)}</div></div>')


def metric_card(label, value, hint=""):
    md(f'<div class="metric"><div class="label">{esc(label)}</div><div class="value">{esc(str(value))}</div>'
       f'<div class="hint">{esc(hint)}</div></div>')


def view_sessions():
    """Sessions to display. Before anything is done, a clearly labelled sample preview is shown."""
    sessions = st.session_state.sessions
    if sessions:
        return sessions, False
    return [dict(s) for s in data.DEMO_SESSIONS], True


# =====================================================================
# Callbacks (state changes happen here so Streamlit reruns cleanly)
# =====================================================================
def go_to(name):
    for label in PAGES:
        if label.endswith(name):
            st.session_state.nav = label
            return


def load_demo():
    s = st.session_state
    s.sessions = [dict(x) for x in data.DEMO_SESSIONS]
    s.resume_text = data.SAMPLE_RESUME
    s.resume_source = "Sample resume (demo data)"
    s.resume_is_sample = True
    s.jd_text = data.SAMPLE_JD
    s.pop("jd_widget", None)
    s.analysis = utils.analyze_resume(data.SAMPLE_RESUME)
    s.match = utils.match_job(s.analysis["skills"], data.SAMPLE_JD)
    s.last_report = utils.build_demo_report()
    s.report_is_sample = True
    s.demo_loaded = True
    s.activity = [{"text": t, "sample": True, "time": "sample"} for t in reversed(data.DEMO_ACTIVITY)]
    s.iv_stage, s.iv = "setup", None
    s.roadmap_role = "Python Developer"


def reset_all():
    keep = {"nav"}
    for key in list(st.session_state.keys()):
        if key not in keep:
            del st.session_state[key]
    init_state()


def use_sample_resume():
    s = st.session_state
    s.resume_text, s.resume_source, s.resume_is_sample = data.SAMPLE_RESUME, "Sample resume (demo data)", True
    s.upload_error = None


def use_sample_jd():
    st.session_state.jd_text = data.SAMPLE_JD
    st.session_state.pop("jd_widget", None)  # widget re-reads its value from jd_text


def run_analysis():
    s = st.session_state
    if not s.resume_text:
        s.analysis_error = "Please upload a PDF resume or click 'Use sample resume' first."
        return
    s.analysis_error = None
    s.analysis = utils.analyze_resume(s.resume_text)
    jd = (s.get("jd_widget") if "jd_widget" in s else s.jd_text) or ""
    jd = jd.strip()
    s.jd_text = jd
    s.match = utils.match_job(s.analysis["skills"], jd) if jd else None
    s.analysis_note = None
    if not jd:
        s.analysis_note = "Add a job description to see matching and missing skills."
    elif s.match is None:
        s.analysis_note = "No known skills were recognised in the job description. Try pasting the full requirements section."
    log_activity("Analyzed a resume" + (" (sample)" if s.resume_is_sample else ""), s.resume_is_sample)


def start_interview():
    s = st.session_state
    clear_answer_boxes()
    role, diff, itype = s.cfg_role, s.cfg_diff, s.cfg_type
    questions = utils.select_questions(role, diff, itype, seed=random.randint(1, 10**9), n=5)
    s.iv = {"questions": questions, "idx": 0, "results": [], "submitted": False, "error": None,
            "role": role, "difficulty": diff, "type": itype}
    s.iv_stage = "running"
    s.roadmap_role = role


def clear_answer_boxes():
    for key in list(st.session_state.keys()):
        if key.startswith("ans_"):
            del st.session_state[key]


def reset_interview():
    clear_answer_boxes()
    st.session_state.iv_stage, st.session_state.iv = "setup", None


def submit_answer():
    iv = st.session_state.iv
    idx = iv["idx"]
    answer = (st.session_state.get(f"ans_{idx}") or "").strip()
    if utils.word_count(answer) < 3:
        iv["error"] = "Please write at least a few words before submitting. Even a short attempt helps you learn."
        return
    iv["error"] = None
    question = iv["questions"][idx]
    iv["results"].append({"q": question, "answer": answer, "ev": utils.evaluate_answer(question, answer)})
    iv["submitted"] = True


def next_question():
    s = st.session_state
    iv = s.iv
    iv["idx"] += 1
    iv["submitted"] = False
    iv["error"] = None
    if iv["idx"] >= len(iv["questions"]):
        report = utils.build_report(iv["results"])
        s.last_report, s.report_is_sample = report, False
        s.sessions.append({"label": now_label(), "role": iv["role"], "type": iv["type"],
                           "difficulty": iv["difficulty"], "score": report["overall"], "sample": False})
        log_activity(f"Completed a {iv['type']} mock interview ({iv['role']}) - score {report['overall']}/10")
        s.iv_stage = "done"


def toggle_day(key):
    st.session_state.roadmap_done[key] = bool(st.session_state.get(key))


def reset_roadmap():
    role = st.session_state.roadmap_role
    for day in range(1, 8):
        key = f"rm_{role}_{day}"
        st.session_state.roadmap_done[key] = False
        st.session_state.pop(key, None)


def pick_topic(topic):
    st.session_state.mentor_topic = topic


# =====================================================================
# Charts (Plotly when installed, Streamlit charts otherwise)
# =====================================================================
def style_fig(fig, height=300):
    fig.update_layout(
        height=height, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#c9d0ee"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.06)", zeroline=False),
        yaxis=dict(gridcolor="rgba(255,255,255,0.06)", zeroline=False),
    )
    return fig


def line_chart(labels, values, title):
    if HAS_PLOTLY:
        fig = go.Figure(go.Scatter(
            x=labels, y=values, mode="lines+markers", line=dict(color="#8b5cf6", width=3, shape="spline"),
            marker=dict(size=10, color="#22d3ee", line=dict(color="#0d1226", width=2)),
            fill="tozeroy", fillcolor="rgba(139,92,246,0.16)"))
        fig.update_layout(title=dict(text=title, font=dict(size=13)), yaxis=dict(range=[0, 10]))
        st.plotly_chart(style_fig(fig, 280))
    else:
        import pandas as pd
        st.caption(title)
        st.line_chart(pd.DataFrame({"Score": values}, index=labels))


def bar_chart(labels, values, title, horizontal=False):
    if HAS_PLOTLY:
        colors = ["#34d399" if v >= 7 else "#fbbf24" if v >= 5 else "#f87171" for v in values]
        if horizontal:
            fig = go.Figure(go.Bar(x=values, y=labels, orientation="h", marker_color=colors))
            fig.update_layout(xaxis=dict(range=[0, 10]), yaxis=dict(autorange="reversed"))
        else:
            fig = go.Figure(go.Bar(x=labels, y=values, marker_color=colors, text=values, textposition="outside"))
            fig.update_layout(yaxis=dict(range=[0, 11]))
        fig.update_layout(title=dict(text=title, font=dict(size=13)))
        st.plotly_chart(style_fig(fig, 280))
    else:
        import pandas as pd
        st.caption(title)
        st.bar_chart(pd.DataFrame({"Score": values}, index=labels))


def gauge(value, title):
    if HAS_PLOTLY:
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=value, number=dict(suffix=" / 10", font=dict(color="#fff", size=34)),
            title=dict(text=title, font=dict(size=14, color="#c9d0ee")),
            gauge=dict(axis=dict(range=[0, 10], tickcolor="#9aa3c2"), bar=dict(color="#8b5cf6"),
                       bgcolor="rgba(255,255,255,0.05)", borderwidth=0,
                       steps=[dict(range=[0, 4], color="rgba(248,113,113,0.20)"),
                              dict(range=[4, 7], color="rgba(251,191,36,0.18)"),
                              dict(range=[7, 10], color="rgba(52,211,153,0.20)")])))
        st.plotly_chart(style_fig(fig, 280))
    else:
        st.metric(title, f"{value} / 10")
        st.progress(min(1.0, value / 10))


def radar(labels, values):
    if HAS_PLOTLY:
        fig = go.Figure(go.Scatterpolar(r=values + values[:1], theta=labels + labels[:1], fill="toself",
                                        line=dict(color="#8b5cf6", width=3), fillcolor="rgba(139,92,246,0.25)"))
        fig.update_layout(polar=dict(bgcolor="rgba(255,255,255,0.03)",
                                     radialaxis=dict(range=[0, 10], gridcolor="rgba(255,255,255,0.1)"),
                                     angularaxis=dict(gridcolor="rgba(255,255,255,0.1)")),
                          title=dict(text="Skill radar (0-10)", font=dict(size=13)))
        st.plotly_chart(style_fig(fig, 300))
    else:
        bar_chart(labels, values, "Skill overview (0-10)")


# =====================================================================
# Sidebar
# =====================================================================
def render_sidebar():
    with st.sidebar:
        md('<div class="brand"><div class="brand-logo">'
           '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2" '
           'stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l2.4 5.4L20 9.3l-4 4 1 5.7-5-2.8L7 19l1-5.7-4-4 5.6-.9z"/></svg>'
           '</div><div><div class="brand-name">Interview Thozhan</div>'
           f'<div class="brand-tag">{esc(data.TAGLINE)}</div></div></div>')
        st.write("")
        st.radio("Navigation", PAGES, key="nav", label_visibility="collapsed")
        st.write("")
        st.button("✨ Explore Demo", key="side_demo", on_click=load_demo, help="Loads a labelled sample candidate, resume analysis and report.")
        if st.session_state.demo_loaded or st.session_state.sessions:
            st.button("↺ Reset all data", key="side_reset", on_click=reset_all)
        md('<div class="side-note"><span class="badge mode">Offline demo</span><br>'
           'Rule-based feedback only. No AI model, internet or API key is used. Your data stays in this browser session.</div>')


# =====================================================================
# Pages
# =====================================================================
def page_dashboard():
    sessions, preview = view_sessions()
    s = st.session_state
    md(f'<div class="hero"><div class="eyebrow">Welcome back</div>'
       f'<h1>Hello, {esc(data.CANDIDATE["name"])} 👋</h1>'
       f'<p>Career target: <b>{esc(data.CANDIDATE["target"])}</b>. Practise real interview questions, get clear feedback, '
       f'and build your confidence one day at a time.</p></div>')

    b1, b2, b3, _ = st.columns([1.2, 1.2, 1, 2])
    b1.button("🎯 Start Mock Interview", key="dash_start", on_click=go_to, args=("Mock Interview",))
    b2.button("📄 Analyze Resume", key="dash_resume", on_click=go_to, args=("Resume Analyzer",))
    b3.button("✨ Explore Demo", key="dash_demo", on_click=load_demo)

    if preview:
        md(f'{sample_badge(True)} &nbsp;<span style="color:#9aa3c2;font-size:0.85rem">This is a preview with sample numbers. '
           f'Complete a mock interview or click <b>Explore Demo</b> to continue.</span>')
    elif any(x.get("sample") for x in sessions):
        md(f'{sample_badge(True)} &nbsp;<span style="color:#9aa3c2;font-size:0.85rem">Sample sessions are labelled "Week n". '
           f'Sessions you complete are added as your own data.</span>')
    else:
        md(f'{sample_badge(False)} &nbsp;<span style="color:#9aa3c2;font-size:0.85rem">Showing only your own practice sessions.</span>')

    ready = utils.readiness(sessions)
    if s.match:
        improve, improve_src = s.match["missing"][:5], "from your resume vs job description"
    elif s.last_report and s.last_report["weak_topics"]:
        improve, improve_src = s.last_report["weak_topics"], "from your latest report"
    else:
        improve, improve_src = data.DEMO_SKILLS_TO_IMPROVE, "sample data"
    best = max(x["score"] for x in sessions)

    st.write("")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        metric_card("Interview readiness", f"{ready}%", "average practice score" + (" (sample)" if preview else ""))
    with m2:
        metric_card("Interviews completed", len(sessions), "sample sessions included" if any(x.get("sample") for x in sessions) else "your sessions")
    with m3:
        metric_card("Skills to improve", len(improve), improve_src)
    with m4:
        metric_card("Best score", f"{best}/10", "single interview")

    st.write("")
    left, right = st.columns([1.6, 1])
    with left:
        with st.container(border=True):
            md('<div class="section-title">Progress across practice sessions</div>')
            line_chart([x["label"] for x in sessions], [x["score"] for x in sessions], "Interview score (out of 10)")
    with right:
        with st.container(border=True):
            md('<div class="section-title">Skills to improve</div>')
            md(chips(improve, "warn"))
            md(f'<div style="color:#9aa3c2;font-size:0.8rem;margin-top:8px">Source: {esc(improve_src)}</div>')
            st.write("")
            md('<div class="section-title">Recent activity</div>')
            acts = list(reversed(s.activity))[:5] if s.activity else [{"text": t, "sample": True} for t in data.DEMO_ACTIVITY]
            for a in acts:
                tag = ' <span class="badge sample">sample</span>' if a.get("sample") else ""
                md(f'<div class="activity"><div class="dot"></div><div class="txt">{esc(a["text"])}{tag}</div></div>')

    md(f'<div class="footer-note">{esc(data.DISCLAIMER)}</div>')


def show_analysis():
    s = st.session_state
    a, m = s.analysis, s.match
    sample = s.resume_is_sample
    st.write("")
    md(f'<div class="section-title">Resume analysis &nbsp;{sample_badge(True) if sample else sample_badge(False)}</div>')
    with st.container(border=True):
        st.write(a["summary"])
        md('<div class="section-title">Skills detected</div>')
        md(chips(a["skills"], "good") or '<span style="color:#9aa3c2">No known skills were recognised in this resume.</span>')

    tabs = st.tabs(["🎓 Education", "🛠️ Projects", "💼 Experience", "📜 Certifications"])
    for tab, key in zip(tabs, ["education", "projects", "experience", "certifications"]):
        with tab:
            lines = a["sections"][key]
            if lines:
                for line in lines:
                    md(f'<div class="activity"><div class="dot"></div><div class="txt">{esc(line)}</div></div>')
            else:
                st.info(f"No '{key}' section was found in this resume. Nothing has been guessed or added.")

    st.write("")
    md('<div class="section-title">Job match</div>')
    if s.get("analysis_note"):
        st.info(s.analysis_note)
    if m:
        c1, c2 = st.columns([1, 2])
        with c1:
            with st.container(border=True):
                metric_card("Skill match", f"{m['percent']}%", f"{len(m['matching'])} of {len(m['jd_skills'])} skills in the job description")
                st.progress(m["percent"] / 100)
        with c2:
            with st.container(border=True):
                md('<div class="section-title">Matching skills</div>' + (chips(m["matching"], "good") or "None found"))
                md('<div class="section-title" style="margin-top:12px">Missing skills</div>' + (chips(m["missing"], "warn") or "None - great!"))
        with st.container(border=True):
            md('<div class="section-title">Recommendations</div>')
            for rec in utils.recommendations(m):
                st.markdown(f"- {rec}")
        st.button("🗺️ Build my learning roadmap", key="to_roadmap", on_click=go_to, args=("Learning Roadmap",))


def page_resume():
    s = st.session_state
    page_header("Resume Analyzer", "Upload your PDF resume and compare it with a job description. Everything is checked with simple keyword rules.")

    left, right = st.columns(2)
    with left:
        with st.container(border=True):
            md('<div class="section-title">1. Your resume</div>')
            up = st.file_uploader("Upload resume (PDF, up to 5 MB)", type=["pdf"], key="resume_pdf")
            if up is not None:
                signature = (up.name, up.size)
                if s.last_upload != signature:
                    s.last_upload = signature
                    text, err = utils.extract_pdf_text(up.getvalue())
                    s.upload_error = err
                    if text:
                        s.resume_text, s.resume_source, s.resume_is_sample = text, up.name, False
                        s.analysis = s.match = None
                if s.upload_error:
                    st.error(s.upload_error)
            else:
                s.last_upload = None
            st.button("Use sample resume", key="sample_resume", on_click=use_sample_resume)
            if s.resume_text:
                md(f'{sample_badge(s.resume_is_sample)} &nbsp;<span style="color:#9aa3c2">{esc(s.resume_source)} - '
                   f'{utils.word_count(s.resume_text)} words read</span>')
            else:
                st.caption("No resume loaded yet.")
    with right:
        with st.container(border=True):
            md('<div class="section-title">2. Job description</div>')
            s.jd_text = st.text_area("Paste the job description", value=s.jd_text, key="jd_widget", height=190,
                                     placeholder="Paste the requirements section of a job post here...")
            st.button("Use sample job description", key="sample_jd", on_click=use_sample_jd)

    st.write("")
    st.button("🔍 Analyze", key="analyze", on_click=run_analysis)
    if s.get("analysis_error"):
        st.error(s.analysis_error)
    if s.analysis:
        show_analysis()
    elif not s.get("analysis_error"):
        st.write("")
        empty_state("📄", "No analysis yet", "Upload a resume (or use the sample), add a job description and click Analyze.")


def feedback_html(kind, title, items):
    lis = "".join(f"<li>{esc(i)}</li>" for i in items)
    return f'<div class="fb {kind}"><div class="fb-title">{title}</div><ul>{lis}</ul></div>'


def show_evaluation(result):
    ev = result["ev"]
    c1, c2 = st.columns([1, 3])
    with c1:
        md(f'<div class="ring" style="--p:{ev["score"] * 10}"><span>{ev["score"]}</span><small>/10</small></div>')
        md(f'<div style="text-align:center;margin-top:8px"><span class="chip {"good" if ev["score"] >= 6 else "warn" if ev["score"] >= 4 else "bad"}">{ev["verdict"]}</span></div>')
    with c2:
        md(feedback_html("good", "✅ What was good", ev["good"]))
        md(feedback_html("miss", "⚠️ What is missing", ev["missing"] or ["Nothing major - you covered the key points."]))
    md(feedback_html("tip", "💡 Suggested improvement", ev["tips"]))
    md(f'<div class="fb ex"><div class="fb-title">📘 Example answer</div>{esc(ev["example"])}</div>')


def interview_setup():
    with st.container(border=True):
        md('<div class="section-title">Set up your interview</div>')
        c1, c2, c3 = st.columns(3)
        c1.selectbox("Job role", data.ROLES, key="cfg_role")
        c2.selectbox("Difficulty", data.DIFFICULTIES, key="cfg_diff")
        c3.selectbox("Interview type", data.INTERVIEW_TYPES, key="cfg_type")
        st.caption("5 questions, one at a time. Mixed = technical + HR questions. Questions come from a local question bank.")
        st.button("🚀 Start Interview", key="start_iv", on_click=start_interview)
    st.write("")
    empty_state("🎤", "Ready when you are", "Answer in your own words. Your answer is checked for key concepts, detail and structure - not grammar or accent.")


def interview_running():
    iv = st.session_state.iv
    total, idx = len(iv["questions"]), iv["idx"]
    q = iv["questions"][idx]
    done = idx + (1 if iv["submitted"] else 0)

    md(chips([iv["role"], iv["difficulty"], iv["type"]]))
    st.progress(done / total)
    st.caption(f"Question {idx + 1} of {total}  ·  {done} answered")
    md(f'<div class="q-card"><div class="qnum">Question {idx + 1} of {total} &nbsp;·&nbsp; {esc(q["topic"])}</div>'
       f'<div class="qtext">{esc(q["question"])}</div></div>')

    if not iv["submitted"]:
        st.text_area("Your answer", key=f"ans_{idx}", height=190,
                     placeholder="Type your answer here. Aim for 3-5 sentences and include one example...")
        if iv["error"]:
            st.warning(iv["error"])
        st.button("Submit Answer", key=f"submit_{idx}", on_click=submit_answer)
    else:
        result = iv["results"][-1]
        md(f'<div class="fb tip"><div class="fb-title">Your answer</div>{esc(result["answer"])}</div>')
        show_evaluation(result)
        last = idx + 1 >= total
        st.button("🏁 Finish & see report" if last else "Next Question ➜", key=f"next_{idx}", on_click=next_question)

    previous = iv["results"][:-1] if iv["submitted"] else iv["results"]
    if previous:
        st.write("")
        with st.expander(f"Interview history ({len(previous)} answered)"):
            for n, r in enumerate(previous, 1):
                st.markdown(f"**Q{n}. {r['q']['question']}**  \nScore: **{r['ev']['score']}/10** ({r['ev']['verdict']})")
                st.caption(r["answer"])
    st.write("")
    st.button("Quit this interview", key="quit_iv", on_click=reset_interview)


def interview_done():
    report = st.session_state.last_report
    md(f'<div class="hero"><div class="eyebrow">Interview complete</div><h1>Well done, {esc(data.CANDIDATE["name"])}! 🎉</h1>'
       f'<p>You answered {report["count"]} questions. Your overall practice score is <b>{report["overall"]}/10</b>. '
       f'Every session makes the next one easier.</p></div>')
    c1, c2, _ = st.columns([1.3, 1.3, 2])
    c1.button("📊 View Performance Report", key="done_report", on_click=go_to, args=("Performance Report",))
    c2.button("🔁 Start another interview", key="done_again", on_click=reset_interview)


def page_interview():
    page_header("Mock Interview", "Practise one question at a time and get instant, rule-based feedback.")
    stage = st.session_state.iv_stage
    if stage == "running" and st.session_state.iv:
        interview_running()
    elif stage == "done" and st.session_state.last_report:
        interview_done()
    else:
        interview_setup()
    md(f'<div class="footer-note">{esc(data.DISCLAIMER)}</div>')


def page_report():
    s = st.session_state
    page_header("Performance Report", "See how you did, question by question, and where to focus next.")
    r = s.last_report
    if not r:
        empty_state("📊", "No report yet", "Complete a mock interview, or load the sample report with Explore Demo.")
        st.write("")
        c1, c2, _ = st.columns([1.3, 1.3, 2])
        c1.button("🎯 Start Mock Interview", key="rep_start", on_click=go_to, args=("Mock Interview",))
        c2.button("✨ Explore Demo", key="rep_demo", on_click=load_demo)
        return

    md(sample_badge(s.report_is_sample) + ' &nbsp;<span style="color:#9aa3c2;font-size:0.85rem">'
       + ("This report was generated from canned sample answers." if s.report_is_sample else "Generated from your own answers.") + "</span>")
    st.write("")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        metric_card("Overall score", f"{r['overall']}/10", "average of all answers")
    with m2:
        metric_card("Technical score", f"{r['technical']}/10", "key concepts covered")
    with m3:
        metric_card("Communication", f"{r['communication']}/10", "detail and structure")
    with m4:
        metric_card("Answer quality", f"{r['quality']}%", "answers scoring 6/10 or more")

    st.write("")
    g, rd = st.columns(2)
    with g:
        with st.container(border=True):
            gauge(r["overall"], "Overall score")
    with rd:
        with st.container(border=True):
            radar(["Technical", "Communication", "Answer quality", "Overall"],
                  [r["technical"], r["communication"], round(r["quality"] / 10, 1), r["overall"]])

    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            bar_chart([f"Q{i}" for i in range(1, r["count"] + 1)], [x["ev"]["score"] for x in r["results"]], "Score per question")
    with c2:
        with st.container(border=True):
            bar_chart(list(r["topic_avg"].keys()), list(r["topic_avg"].values()), "Average score by topic", horizontal=True)

    st.write("")
    k1, k2 = st.columns(2)
    with k1:
        md(f'<div class="fb good"><div class="fb-title">💪 Strongest skill</div><b>{esc(r["strongest"])}</b> ({r["topic_avg"][r["strongest"]]}/10)</div>')
    with k2:
        if r["weakest"]:
            md(f'<div class="fb miss"><div class="fb-title">🎯 Weakest skill</div><b>{esc(r["weakest"])}</b> ({r["topic_avg"][r["weakest"]]}/10)</div>')
        else:
            md('<div class="fb miss"><div class="fb-title">🎯 Weakest skill</div>Only one topic was covered, so a weakest skill cannot be compared.</div>')

    st.write("")
    md('<div class="section-title">Question-by-question evaluation</div>')
    for i, item in enumerate(r["results"], 1):
        ev = item["ev"]
        with st.expander(f"Q{i}. {item['q']['question']}  -  {ev['score']}/10 ({ev['verdict']})"):
            md(f'<div class="fb tip"><div class="fb-title">Your answer</div>{esc(item["answer"])}</div>')
            show_evaluation(item)

    sessions, preview = view_sessions()
    st.write("")
    with st.container(border=True):
        md(f'<div class="section-title">Progress across sessions &nbsp;{sample_badge(preview or any(x.get("sample") for x in sessions))}</div>')
        line_chart([x["label"] for x in sessions], [x["score"] for x in sessions], "Interview score (out of 10)")
    st.write("")
    st.button("🗺️ Turn this into a learning roadmap", key="rep_roadmap", on_click=go_to, args=("Learning Roadmap",))
    md(f'<div class="footer-note">{esc(data.DISCLAIMER)}</div>')


def page_mentor():
    s = st.session_state
    page_header("Career Mentor", "Pick a topic for a clear explanation - in English or Tamil. Content is pre-written, not AI-generated.")
    s.mentor_lang = st.radio("Language / மொழி", ["English", "Tamil"], index=0 if s.mentor_lang == "English" else 1,
                             key="mentor_lang_w", horizontal=True)

    topics = list(data.MENTOR_TOPICS)
    for row_start in range(0, len(topics), 4):
        cols = st.columns(4)
        for col, topic in zip(cols, topics[row_start:row_start + 4]):
            info = data.MENTOR_TOPICS[topic]
            marker = "✓ " if topic == s.mentor_topic else ""
            col.button(f"{marker}{info['icon']} {topic}", key=f"topic_{topic}", on_click=pick_topic, args=(topic,))

    topic = s.mentor_topic
    info = data.MENTOR_TOPICS[topic]
    lang = "ta" if s.mentor_lang == "Tamil" else "en"
    st.write("")
    with st.container(border=True):
        md(f'<div class="section-title">{info["icon"]} {esc(topic)} &nbsp;<span class="badge mode">{"தமிழ்" if lang == "ta" else "English"}</span></div>')
        st.markdown(info[lang])
        if lang == "ta":
            st.caption("Interview answers should still be practised in English. Use the Tamil explanation to understand the concept first.")
    with st.expander("Practice questions for this topic"):
        for p in info["practice"]:
            st.markdown(f"- {p}")
        st.button("Practise in a mock interview", key="mentor_to_iv", on_click=go_to, args=("Mock Interview",))

    r = s.last_report
    if r and r["weak_topics"]:
        st.write("")
        md(f'<div class="fb tip"><div class="fb-title">From your latest report'
           f'{" (sample)" if s.report_is_sample else ""}</div>Topics to revisit: {esc(", ".join(r["weak_topics"]))}</div>')
    md(f'<div class="footer-note">{esc(data.DISCLAIMER)}</div>')


def page_roadmap():
    s = st.session_state
    page_header("Learning Roadmap", "A simple 7-day plan built from your role and skill gaps. Tick each day when you finish it.")
    s.roadmap_role = st.selectbox("Career role", data.ROLES, index=data.ROLES.index(s.roadmap_role), key="roadmap_role_w")
    role = s.roadmap_role

    if s.match and s.match["missing"]:
        gaps, source = s.match["missing"], "missing skills from your resume analysis" + (" (sample)" if s.resume_is_sample else "")
    elif s.last_report and s.last_report["weak_topics"]:
        gaps, source = s.last_report["weak_topics"], "weak topics from your latest report" + (" (sample)" if s.report_is_sample else "")
    else:
        gaps, source = [], "default topics for this role (analyze a resume or finish an interview to personalise)"
    md(f'<span style="color:#9aa3c2">Built from: {esc(source)}</span>')

    days = utils.generate_roadmap(role, gaps)
    keys = [f"rm_{role}_{d['day']}" for d in days]
    completed = sum(1 for k in keys if s.roadmap_done.get(k))
    st.write("")
    c1, c2 = st.columns([3, 1])
    with c1:
        st.progress(completed / len(days))
        st.caption(f"{completed} of {len(days)} days completed")
    with c2:
        st.button("Reset progress", key="rm_reset", on_click=reset_roadmap)

    for d, k in zip(days, keys):
        with st.container(border=True):
            md(f'<div class="eyebrow">Day {d["day"]}</div><div class="section-title">{esc(d["objective"])}</div>'
               f'<div style="color:#c9d0ee"><b>Practice task:</b> {esc(d["task"])}</div>')
            st.checkbox(f"Mark Day {d['day']} complete", value=s.roadmap_done.get(k, False), key=k,
                        on_change=toggle_day, args=(k,))
    if completed == len(days):
        st.success("You finished the 7-day plan - great consistency! Take a new mock interview and compare your score.")
    md(f'<div class="footer-note">A practice plan, not a guarantee of any hiring outcome.</div>')


# =====================================================================
# Main
# =====================================================================
def main():
    init_state()
    load_css()
    render_sidebar()
    page = st.session_state.nav
    handlers = {
        PAGES[0]: page_dashboard, PAGES[1]: page_resume, PAGES[2]: page_interview,
        PAGES[3]: page_report, PAGES[4]: page_mentor, PAGES[5]: page_roadmap,
    }
    handlers.get(page, page_dashboard)()


main()
