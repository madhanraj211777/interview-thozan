"""Pure-Python helpers: resume parsing, rule-based evaluation, reports and roadmap. No Streamlit, no AI."""
import random
import re
from collections import OrderedDict

import data

MAX_PDF_MB = 5

# ------------------------------------------------------------------ PDF
def extract_pdf_text(file_bytes):
    """Return (text, error). Uses PyMuPDF if installed. Never raises."""
    if not file_bytes:
        return None, "The file is empty."
    if len(file_bytes) > MAX_PDF_MB * 1024 * 1024:
        return None, f"The file is larger than {MAX_PDF_MB} MB. Please upload a smaller PDF."
    if not file_bytes.lstrip()[:5].startswith(b"%PDF"):
        return None, "This does not look like a valid PDF file."
    try:
        import fitz  # PyMuPDF
    except ImportError:
        return None, "PyMuPDF is not installed. Run: pip install pymupdf  (or use the sample resume)."
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
    except Exception:
        return None, "Could not read this PDF. It may be damaged or password protected."
    if not text.strip():
        return None, "No selectable text found. Scanned/image PDFs are not supported."
    return text, None


# ------------------------------------------------------------------ Resume analysis
def detect_skills(text):
    """Return skills (display names) that appear in the text. Only reports what is actually written."""
    lower = (text or "").lower()
    found = []
    for name, aliases in data.SKILLS.items():
        for alias in aliases:
            pattern = r"(?<![a-z0-9+#])" + re.escape(alias) + r"(?![a-z0-9+#])"
            if re.search(pattern, lower):
                found.append(name)
                break
    return found


_HEADINGS = {
    "education": {"education", "academic", "academics", "qualification", "qualifications", "academic qualification"},
    "projects": {"projects", "project", "academic projects", "personal projects"},
    "experience": {"experience", "work experience", "internship", "internships", "professional experience",
                   "internship experience"},
    "skills": {"skills", "technical skills", "key skills"},
    "certifications": {"certifications", "certificates", "certification", "achievements"},
    "summary": {"summary", "objective", "career objective", "profile", "professional summary"},
}
_HEADING_LOOKUP = {alias: key for key, aliases in _HEADINGS.items() for alias in aliases}


def extract_sections(text):
    """Split resume text under recognised headings. Missing sections stay empty (nothing is invented)."""
    sections = {k: [] for k in _HEADINGS}
    current = None
    for raw in (text or "").splitlines():
        line = raw.strip()
        if not line:
            continue
        key = _HEADING_LOOKUP.get(line.lower().rstrip(":").strip())
        if key:
            current = key
        elif current:
            sections[current].append(line)
    return sections


def analyze_resume(text):
    skills = detect_skills(text)
    sections = extract_sections(text)
    parts = [f"{len(skills)} recognised skill(s)"]
    for key in ("education", "projects", "experience", "certifications"):
        parts.append(f"{len(sections[key])} line(s) under {key}")
    summary = "Rule-based summary - this resume contains " + ", ".join(parts) + ". "
    if skills:
        summary += "Skills found: " + ", ".join(skills[:8]) + ("..." if len(skills) > 8 else "") + "."
    else:
        summary += "No known skills were recognised from the skill list."
    return {"skills": skills, "sections": sections, "summary": summary, "word_count": word_count(text)}


def match_job(resume_skills, jd_text):
    """Compare resume skills with skills named in the job description."""
    jd_skills = detect_skills(jd_text)
    if not jd_skills:
        return None
    have = set(resume_skills)
    matching = [s for s in jd_skills if s in have]
    missing = [s for s in jd_skills if s not in have]
    return {
        "jd_skills": jd_skills,
        "matching": matching,
        "missing": missing,
        "percent": round(100 * len(matching) / len(jd_skills)),
    }


def recommendations(match):
    if not match:
        return []
    recs = []
    pct = match["percent"]
    if pct >= 80:
        recs.append("Your listed skills cover most of this job description. Focus on explaining each one confidently.")
    elif pct >= 50:
        recs.append("You match about half of the listed skills. Closing the top gaps below will make a real difference.")
    else:
        recs.append("There are many gaps for this job. Pick one or two skills at a time and build small projects.")
    for skill in match["missing"][:5]:
        recs.append(f"**{skill}:** " + data.SKILL_TASKS.get(skill, f"Learn the basics of {skill} and prepare 3 interview questions about it."))
    if match["matching"]:
        recs.append("Prepare one project example for each matching skill: " + ", ".join(match["matching"][:5]) + ".")
    recs.append("This is a keyword comparison only. It cannot verify your real ability or predict hiring decisions.")
    return recs


# ------------------------------------------------------------------ Interview
def select_questions(role, difficulty, interview_type, seed=None, n=5):
    """Pick n questions from the local bank, nearest to the chosen difficulty first."""
    if role not in data.ROLES or difficulty not in data.LEVEL or interview_type not in data.INTERVIEW_TYPES:
        raise ValueError("Unknown role, difficulty or interview type.")
    rng = random.Random(seed)
    target = data.LEVEL[difficulty]

    def pick(pool_role, k):
        pool = [q for q in data.QUESTIONS if q["role"] == pool_role]
        groups = OrderedDict()
        for q in pool:
            groups.setdefault(abs(q["level"] - target), []).append(q)
        ordered = []
        for dist in sorted(groups):
            items = groups[dist][:]
            rng.shuffle(items)
            ordered.extend(items)
        return ordered[:k]

    if interview_type == "Technical":
        chosen = pick(role, n)
    elif interview_type == "HR":
        chosen = pick("HR", n)
    else:
        tech, hr = pick(role, n - n // 2), pick("HR", n // 2)
        tech = tech[: n - len(hr)]
        chosen = []
        for i in range(max(len(tech), len(hr))):
            if i < len(tech):
                chosen.append(tech[i])
            if i < len(hr):
                chosen.append(hr[i])
    return [dict(q) for q in chosen]


def word_count(text):
    return len(re.findall(r"\w+", text or ""))


_EXAMPLE_MARKERS = ["for example", "for instance", "such as", "e.g", "in my project", "i built", "i worked",
                    "i used", "in my college", "when i"]
_CONNECTORS = ["because", "so that", "therefore", "first", "second", "finally", "however", "which means",
               "as a result", "so ", "then "]


def evaluate_answer(question, answer):
    """Rule-based scoring out of 10: concept coverage (6) + detail (2) + structure/example (2)."""
    text = (answer or "").strip()
    lower = text.lower()
    words = word_count(text)

    matched, missing = [], []
    for label, terms in question["concepts"]:
        (matched if any(t in lower for t in terms) else missing).append(label)
    total = len(question["concepts"])
    coverage = len(matched) / total if total else 0.0
    coverage_pts = coverage * 6

    if words >= 60:
        depth_pts = 2.0
    elif words >= 35:
        depth_pts = 1.6
    elif words >= 20:
        depth_pts = 1.2
    elif words >= 10:
        depth_pts = 0.7
    else:
        depth_pts = 0.3

    has_example = words >= 15 and any(m in lower for m in _EXAMPLE_MARKERS)
    n_conn = sum(1 for c in _CONNECTORS if c in lower)
    structure_pts = (1.0 if has_example else 0.0) + min(1.0, n_conn / 2)

    score = coverage_pts + depth_pts + structure_pts
    if words < 5:
        score = min(score, 2.0)
    score = round(max(0.0, min(10.0, score)), 1)

    good = [f"You covered: {label}" for label in matched]
    if depth_pts >= 1.2:
        good.append("Your answer had a good level of detail.")
    if has_example:
        good.append("You used an example - interviewers like this.")
    if n_conn >= 2:
        good.append("Your answer was well connected (reasons and steps).")
    if not good:
        good.append("You made an attempt - that is how practice begins.")

    tips = []
    if missing:
        tips.append("Try to include these points: " + "; ".join(missing) + ".")
    if not has_example:
        tips.append("Add a short example from your project or college.")
    if words < 20:
        tips.append("Aim for 3-5 sentences (about 30-60 words).")
    if n_conn < 2:
        tips.append("Use linking words like 'because', 'for example' and 'so' to make your answer flow.")
    if not tips:
        tips.append("Strong answer! Practise saying it smoothly in under a minute.")

    if score >= 8:
        verdict = "Excellent"
    elif score >= 6:
        verdict = "Good"
    elif score >= 4:
        verdict = "Fair"
    else:
        verdict = "Needs work"

    return {
        "score": score,
        "verdict": verdict,
        "tech": round(coverage * 10, 1),
        "comm": round((depth_pts + structure_pts) / 4 * 10, 1),
        "good": good,
        "missing": missing,
        "tips": tips,
        "example": question["example"],
        "words": words,
    }


def build_report(results):
    """results: list of {'q': question, 'answer': str, 'ev': evaluation}. Returns summary metrics."""
    if not results:
        return None
    n = len(results)
    overall = round(sum(r["ev"]["score"] for r in results) / n, 1)
    technical = round(sum(r["ev"]["tech"] for r in results) / n, 1)
    communication = round(sum(r["ev"]["comm"] for r in results) / n, 1)
    quality = round(100 * sum(1 for r in results if r["ev"]["score"] >= 6) / n)
    topics = OrderedDict()
    for r in results:
        topics.setdefault(r["q"]["topic"], []).append(r["ev"]["score"])
    topic_avg = OrderedDict((t, round(sum(v) / len(v), 1)) for t, v in topics.items())
    strongest = max(topic_avg, key=topic_avg.get)
    weakest = min(topic_avg, key=topic_avg.get) if len(topic_avg) > 1 else None
    weak_topics = [t for t, s in sorted(topic_avg.items(), key=lambda kv: kv[1]) if s < 6][:3]
    return {
        "overall": overall, "technical": technical, "communication": communication, "quality": quality,
        "topic_avg": topic_avg, "strongest": strongest, "weakest": weakest, "weak_topics": weak_topics,
        "results": results, "count": n,
    }


def build_demo_report():
    """Score the canned demo answers with the real rule-based checker."""
    by_id = {q["id"]: q for q in data.QUESTIONS}
    results = []
    for qid in data.DEMO_INTERVIEW_IDS:
        q = by_id[qid]
        ans = data.DEMO_ANSWERS[qid]
        results.append({"q": q, "answer": ans, "ev": evaluate_answer(q, ans)})
    return build_report(results)


def readiness(sessions):
    """Average session score as a percentage (None if there are no sessions)."""
    if not sessions:
        return None
    return round(sum(s["score"] for s in sessions) / len(sessions) * 10)


# ------------------------------------------------------------------ Roadmap
def generate_roadmap(role, gaps):
    """Seven-day plan. gaps = skills/topics to work on (may be empty)."""
    gaps = list(OrderedDict.fromkeys(g for g in gaps if g))
    for fallback in data.ROLE_DEFAULT_GAPS.get(role, []):
        if len(gaps) >= 3:
            break
        if fallback not in gaps:
            gaps.append(fallback)

    def task_for(gap):
        return data.SKILL_TASKS.get(gap, f"Read a beginner guide on {gap}, then write 3 interview-style questions about it and answer them aloud.")

    days = [{"day": 1, "objective": f"Know your starting point for {role}",
             "task": "Take one 5-question mock interview in this app and note your weakest answers."}]
    for i, gap in enumerate(gaps[:3]):
        days.append({"day": 2 + i, "objective": f"Strengthen: {gap}", "task": task_for(gap)})
    days.append({"day": 5, "objective": "Revise core concepts out loud",
                 "task": "Pick 5 questions from the mock interview. Answer each in 4-5 sentences with one example."})
    days.append({"day": 6, "objective": "Prepare your HR story",
                 "task": "Write and practise 'Tell me about yourself' and one STAR story (Situation, Task, Action, Result) in 60 seconds each."})
    days.append({"day": 7, "objective": "Full mock interview and reflection",
                 "task": "Take a Mixed mock interview and compare your score with Day 1. Note two things that improved."})
    return days
