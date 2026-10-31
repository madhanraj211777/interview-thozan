import itertools

import pytest

import data
import utils


def test_every_question_is_well_formed():
    ids = [q["id"] for q in data.QUESTIONS]
    assert len(ids) == len(set(ids))
    for q in data.QUESTIONS:
        assert q["concepts"] and q["example"] and q["question"]
        # the model example answer must score well with the checker itself
        assert utils.evaluate_answer(q, q["example"])["score"] >= 7.5, q["id"]


def test_empty_and_weak_answers_score_low_and_differ_from_strong():
    q = data.QUESTIONS[0]
    assert utils.evaluate_answer(q, "")["score"] <= 2
    assert utils.evaluate_answer(q, "I do not know")["score"] < 3
    weak = utils.evaluate_answer(q, "Abstract class is a class.")
    strong = utils.evaluate_answer(q, q["example"])
    assert weak["score"] < strong["score"]
    assert weak["missing"] and not strong["missing"]


def test_feedback_is_question_specific():
    a = utils.evaluate_answer(data.QUESTIONS[0], "something short")
    b = utils.evaluate_answer(data.QUESTIONS[7], "something short")
    assert a["missing"] != b["missing"]


@pytest.mark.parametrize("role,diff,itype", list(itertools.product(data.ROLES, data.DIFFICULTIES, data.INTERVIEW_TYPES)))
def test_select_questions_all_combinations(role, diff, itype):
    qs = utils.select_questions(role, diff, itype, seed=1)
    assert len(qs) == 5 and len({q["id"] for q in qs}) == 5
    if itype == "Technical":
        assert all(q["role"] == role for q in qs)
    elif itype == "HR":
        assert all(q["role"] == "HR" for q in qs)
    else:
        assert {q["role"] for q in qs} == {role, "HR"}


def test_difficulty_prefers_matching_level():
    qs = utils.select_questions("Java Developer", "Advanced", "Technical", seed=3)
    assert sum(q["level"] == 3 for q in qs) == 2  # all level-3 java questions are included


def test_select_questions_rejects_bad_input():
    with pytest.raises(ValueError):
        utils.select_questions("Chef", "Beginner", "Technical")


def test_detect_skills_is_exact():
    assert "Java" in utils.detect_skills("I know Java and SQL")
    assert "Java" not in utils.detect_skills("I know JavaScript only")
    assert "SQL" in utils.detect_skills("MySQL projects")
    assert utils.detect_skills("") == []


def test_resume_sections_not_invented():
    a = utils.analyze_resume(data.SAMPLE_RESUME)
    assert "Python" in a["skills"] and "Docker" not in a["skills"]
    assert any("B.E." in line for line in a["sections"]["education"])
    empty = utils.analyze_resume("Just a random paragraph with no headings.")
    assert all(not v for v in empty["sections"].values())


def test_job_match():
    a = utils.analyze_resume(data.SAMPLE_RESUME)
    m = utils.match_job(a["skills"], data.SAMPLE_JD)
    assert "Docker" in m["missing"] and "Python" in m["matching"]
    assert m["percent"] == round(100 * len(m["matching"]) / len(m["jd_skills"]))
    assert utils.match_job(a["skills"], "no known skills here") is None
    assert utils.recommendations(m)


def test_pdf_validation_errors():
    assert utils.extract_pdf_text(b"")[1]
    assert utils.extract_pdf_text(b"hello not a pdf")[1]
    assert utils.extract_pdf_text(b"%PDF-1.4" + b"0" * (6 * 1024 * 1024))[1]


def test_report_and_demo_report():
    r = utils.build_demo_report()
    assert r["count"] == 5 and 0 <= r["overall"] <= 10
    assert r["strongest"] and r["weakest"] and r["strongest"] != r["weakest"]
    assert 0 <= r["quality"] <= 100
    assert utils.build_report([]) is None


def test_readiness():
    assert utils.readiness([]) is None
    assert utils.readiness([{"score": 5.0}, {"score": 7.0}]) == 60


def test_roadmap_has_seven_days_and_uses_gaps():
    days = utils.generate_roadmap("Python Developer", ["Docker", "REST API"])
    assert [d["day"] for d in days] == list(range(1, 8))
    assert "Docker" in days[1]["objective"] and "REST API" in days[2]["objective"]
    assert all(d["task"] and d["objective"] for d in days)
    assert len(utils.generate_roadmap("Data Analyst", [])) == 7
