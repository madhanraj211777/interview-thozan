"""Smoke-test app.py WITHOUT Streamlit installed, using a small fake `streamlit` module.

The fake mimics the parts of Streamlit that app.py uses (session_state, widgets, callbacks that run
before the script, columns/containers). It does not test the visual look - only that every page runs
and every button/flow works. Run the real app with `streamlit run app.py` to check the visuals.
"""
import runpy
import sys
import types
from pathlib import Path
from unittest.mock import MagicMock

import pytest

import data

APP = str(Path(__file__).resolve().parent.parent / "app.py")


class State(dict):
    def __getattr__(self, k):
        try:
            return self[k]
        except KeyError:
            raise AttributeError(k)

    def __setattr__(self, k, v):
        self[k] = v

    def __delattr__(self, k):
        del self[k]


class Ctx:
    def __init__(self, fake):
        self._fake = fake

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def __getattr__(self, name):
        return getattr(self._fake, name)


class FakeStreamlit(types.ModuleType):
    def __init__(self):
        super().__init__("streamlit")
        self.session_state = State()
        self.upload = None
        self.registry = {}
        self.new_registry = {}
        self.out = []
        self.sidebar = Ctx(self)

    # ---- helpers for tests
    def text(self):
        return "\n".join(self.out)

    # ---- layout
    def columns(self, spec, **kw):
        n = spec if isinstance(spec, int) else len(spec)
        return [Ctx(self) for _ in range(n)]

    def container(self, **kw):
        return Ctx(self)

    def expander(self, label, **kw):
        self.out.append(f"[expander] {label}")
        return Ctx(self)

    def tabs(self, labels):
        return [Ctx(self) for _ in labels]

    # ---- output
    def _emit(self, *a, **kw):
        if a:
            self.out.append(str(a[0]))

    markdown = write = caption = info = warning = error = success = _emit

    def set_page_config(self, **kw):
        pass

    def progress(self, v, **kw):
        assert 0.0 <= v <= 1.0, f"progress out of range: {v}"

    def metric(self, *a, **kw):
        self._emit(*a)

    def plotly_chart(self, fig, **kw):
        pass

    def line_chart(self, *a, **kw):
        pass

    bar_chart = line_chart

    # ---- widgets
    def button(self, label, key=None, on_click=None, args=(), **kw):
        assert key, f"button '{label}' needs a unique key"
        assert key not in self.new_registry, f"duplicate widget key {key}"
        self.new_registry[key] = (on_click, args)
        assert on_click is not None, f"button '{label}' has no action"
        return False

    def _widget(self, key, default, on_change=None, args=()):
        assert key, "widget needs a key"
        assert key not in self.new_registry, f"duplicate widget key {key}"
        self.new_registry[key] = (on_change, args)
        if key not in self.session_state:
            self.session_state[key] = default
        return self.session_state[key]

    def selectbox(self, label, options, index=0, key=None, **kw):
        v = self._widget(key, options[index])
        assert v in options
        return v

    def radio(self, label, options, index=0, key=None, **kw):
        v = self._widget(key, options[index])
        assert v in options
        return v

    def text_area(self, label, value="", key=None, **kw):
        return self._widget(key, value)

    def checkbox(self, label, value=False, key=None, on_change=None, args=(), **kw):
        return self._widget(key, value, on_change, args)

    def file_uploader(self, *a, **kw):
        return self.upload

    def write_(self, *a):
        pass

    def rerun(self):
        raise AssertionError("app should not need st.rerun()")


def _write(self, *a, **kw):
    self._emit(*a)


FakeStreamlit.write = _write


class Runner:
    def __init__(self):
        self.st = FakeStreamlit()
        sys.modules["streamlit"] = self.st
        sys.modules["plotly"] = MagicMock()
        sys.modules["plotly.graph_objects"] = MagicMock()

    @property
    def state(self):
        return self.st.session_state

    def run(self, nav=None, click=None, change=None):
        """Simulate one user action then one script run (callbacks run first, like Streamlit)."""
        st = self.st
        if not st.registry:  # first render so widgets/buttons exist, like a real browser session
            st.out, st.new_registry = [], {}
            runpy.run_path(APP, run_name="__main__")
            st.registry = st.new_registry
        if nav:
            label = next(p for p in ["🏠 Dashboard", "📄 Resume Analyzer", "🎯 Mock Interview", "📊 Performance Report",
                                     "🧑‍🏫 Career Mentor", "🗺️ Learning Roadmap"] if p.endswith(nav))
            st.session_state["nav"] = label
        if change:
            for key, value in change.items():
                st.session_state[key] = value
                cb, args = st.registry.get(key, (None, ()))
                if cb:
                    cb(*args)
        if click:
            assert click in st.registry, f"button {click!r} not on screen. On screen: {sorted(st.registry)}"
            cb, args = st.registry[click]
            cb(*args)
        st.out = []
        st.new_registry = {}
        runpy.run_path(APP, run_name="__main__")
        st.registry = st.new_registry
        return st.text()


@pytest.fixture
def app():
    r = Runner()
    yield r
    for m in ("streamlit", "plotly", "plotly.graph_objects"):
        sys.modules.pop(m, None)


PAGES = ["Dashboard", "Resume Analyzer", "Mock Interview", "Performance Report", "Career Mentor", "Learning Roadmap"]


def test_every_page_renders_on_fresh_start(app):
    for p in PAGES:
        out = app.run(nav=p)
        assert out.strip(), p


def test_fresh_dashboard_is_labelled_sample(app):
    out = app.run()
    assert "Sample demo data" in out and "Madhanraj" in out


def test_explore_demo_populates_everything(app):
    app.run()
    app.run(click="dash_demo")
    s = app.state
    assert s.demo_loaded and s.analysis and s.match and s.last_report and s.report_is_sample
    assert len(s.sessions) == len(data.DEMO_SESSIONS) and all(x["sample"] for x in s.sessions)
    for p in PAGES:
        app.run(nav=p)
    assert "sample" in app.run(nav="Performance Report").lower()
    assert "Question-by-question" in app.run(nav="Performance Report")


def test_full_interview_flow(app):
    app.run(nav="Mock Interview")
    app.run(click="start_iv")
    iv = app.state.iv
    assert app.state.iv_stage == "running" and len(iv["questions"]) == 5

    # empty answer is rejected, nothing recorded, example answer not revealed
    out = app.run(click="submit_0")
    assert iv["results"] == [] and "at least a few words" in out
    assert iv["questions"][0]["example"] not in out

    for i, q in enumerate(iv["questions"]):
        app.run(change={f"ans_{i}": q["example"] if i % 2 == 0 else "I am not sure."})
        out = app.run(click=f"submit_{i}")
        assert len(iv["results"]) == i + 1 and iv["submitted"]
        assert q["example"] in out  # shown only after submitting
        assert "What was good" in out and "What is missing" in out and "Suggested improvement" in out
        app.run(click=f"next_{i}")

    assert app.state.iv_stage == "done"
    assert len(app.state.sessions) == 1 and not app.state.sessions[0]["sample"]
    assert app.state.report_is_sample is False
    out = app.run()  # still on Mock Interview page, done view
    assert "Interview complete" in out
    out = app.run(nav="Performance Report")
    assert "Strongest skill" in out and "Your own answers" not in out
    dash = app.run(nav="Dashboard")
    assert "Your data" in dash and "Showing only your own practice sessions" in dash
    assert len(app.state.activity) == 1
    # start again, answers must not be prefilled
    app.run(nav="Mock Interview")
    app.run(click="done_again")
    app.run(click="start_iv")
    assert not app.state.get("ans_0")


@pytest.mark.parametrize("itype", data.INTERVIEW_TYPES)
def test_each_interview_type_runs(app, itype):
    app.run(nav="Mock Interview")
    app.run(change={"cfg_type": itype, "cfg_diff": "Advanced", "cfg_role": "Data Analyst"})
    app.run(click="start_iv")
    assert app.state.iv["type"] == itype
    app.run()


def test_resume_analyzer_flow(app):
    out = app.run(nav="Resume Analyzer")
    assert "No analysis yet" in out
    out = app.run(click="analyze")
    assert "upload a PDF resume" in out and not app.state.analysis  # graceful error
    app.run(click="sample_resume")
    out = app.run(click="analyze")
    assert "Skills detected" in out and "Python" in out and "No job description" not in out
    assert "Add a job description" in out and app.state.match is None
    app.run(click="sample_jd")
    out = app.run(click="analyze")
    assert app.state.match and "Missing skills" in out and "Recommendations" in out
    # unusable JD
    app.run(change={"jd_widget": "hello world"})
    out = app.run(click="analyze")
    assert "No known skills were recognised in the job description" in out


def test_bad_pdf_upload_is_handled(app):
    class Up:
        name, size = "x.pdf", 10

        def getvalue(self):
            return b"not really a pdf"

    app.st.upload = Up()
    out = app.run(nav="Resume Analyzer")
    assert "valid PDF" in out and not app.state.resume_text


def test_mentor_topics_and_tamil(app):
    app.run(nav="Career Mentor")
    for topic in data.MENTOR_TOPICS:
        app.run(click=f"topic_{topic}")
        assert app.state.mentor_topic == topic
    app.run(change={"mentor_lang_w": "Tamil"})
    out = app.run(click="topic_OOP concepts")
    assert "மரபுரிமை" in out
    app.run(change={"mentor_lang_w": "English"})
    assert "Inheritance:" in app.run()


def test_roadmap_progress_persists_across_pages(app):
    app.run(click="side_demo")
    app.run(nav="Learning Roadmap")
    out = app.run()
    assert "0 of 7 days completed" in out and "Docker" in out  # gaps come from the sample resume analysis
    app.run(change={"rm_Python Developer_1": True, "rm_Python Developer_2": True})
    assert "2 of 7 days completed" in app.run()
    app.state.pop("rm_Python Developer_1"), app.state.pop("rm_Python Developer_2")  # Streamlit drops unrendered widget keys
    app.run(nav="Dashboard")
    out = app.run(nav="Learning Roadmap")
    assert "2 of 7 days completed" in out
    app.run(click="rm_reset")
    assert "0 of 7 days completed" in app.run()


def test_reset_all_clears_demo(app):
    app.run(click="side_demo")
    app.run(click="side_reset")
    assert not app.state.demo_loaded and app.state.sessions == []


def test_html_has_no_unescaped_user_text(app):
    app.run(nav="Mock Interview")
    app.run(click="start_iv")
    app.run(change={"ans_0": "<script>alert(1)</script> because it is a test for example"})
    out = app.run(click="submit_0")
    assert "<script>" not in out and "&lt;script&gt;" in out
