<<<<<<< HEAD
# 🎯 Interview Thozhan

**Your Personal AI Interview Companion**: practise interviews, get feedback, build confidence. Made for college students, fresh graduates and job seekers, especially from rural backgrounds. Includes Tamil explanations.

> **Honest note:** this version is an **offline demo**. There is **no AI model** and no API key.
> Feedback comes from simple, transparent Python rules (keyword coverage, answer detail, structure).
> Scores are practice feedback only, not a hiring assessment.

## Run it

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Then open the link Streamlit prints (usually http://localhost:8501).
Click **✨ Explore Demo** in the sidebar to load a labelled sample candidate straight away.

## Pages

| Page | What it does |
|---|---|
| Dashboard | Readiness, sessions, progress chart, skills to improve, recent activity |
| Resume Analyzer | Upload a PDF (PyMuPDF), detect skills, compare with a job description |
| Mock Interview | Pick role, difficulty and type. One question at a time, scored 0-10 with feedback |
| Performance Report | Overall, technical and communication scores, charts, question-by-question review |
| Career Mentor | 7 pre-written topics in English or Tamil |
| Learning Roadmap | A 7-day plan from your skill gaps, with progress tracking |

Roles: Java, Python, Full Stack, Data Analyst. Question banks are in `data.py`.

## How the scoring works (no AI)

Each answer gets up to 10 points:
- **6 points**: how many key concepts for that question appear in your answer
- **2 points**: level of detail (word count)
- **2 points**: structure (an example, plus linking words like "because")

Grammar and accent are not scored. This is a keyword-based check, so a correct answer in unusual words can score lower than it deserves.

## Data and honesty

- Everything marked **Sample demo data** is made up for the demo.
- Resume details are only what is found in the text. Missing sections stay empty.
- Nothing is saved to disk. Data lives in the browser session and is lost on refresh.

## Files

```
app.py          the Streamlit app (all 6 pages)
data.py         question banks, mentor content (English and Tamil), sample data
utils.py        resume parsing, scoring, report and roadmap logic
styles.css      the dark theme
tests/          pytest tests
```

## Tests

```bash
pip install pytest
python -m pytest -q
```
`tests/test_app_smoke.py` uses a fake Streamlit module to click through every page and flow without a browser.
It checks logic and flow, not the visual look.
=======
# interview-thozan
AI-powered interview preparation companion
>>>>>>> a592f2a21d41448ad2779fc158a7019de9ccc0fd
