import math
from datetime import datetime
CURRENT_YEAR = datetime.now().year

STUDY_DESIGN_WEIGHTS={
  "meta-analysis": 1.0,
  "systematic review": 0.9,
  "randomized controlled trial": 0.8,
  "cohort study": 0.7,
  "case-control study": 0.6,
  "clinical trial": 0.8,
  "case series": 0.45,
  "case report": 0.3,
  "review": 0.5,
  "unknown": 0.40
}



def normalize_sample_size(sample_size, max_sample_size=10000):
    if not sample_size or sample_size <= 0:
        return 0.25

    return math.log(1 + sample_size) / math.log(1 + max_sample_size)


def recency_score(year, decay_rate=0.08):
    if not year:
        return 0.50

    age = max(CURRENT_YEAR - int(year), 0)
    return math.exp(-decay_rate * age)


def study_design_score(study_type):
    if not study_type:
        return STUDY_DESIGN_WEIGHTS["unknown"]

    study_type = study_type.lower()

    for key, score in STUDY_DESIGN_WEIGHTS.items():
        if key in study_type:
            return score

    return STUDY_DESIGN_WEIGHTS["unknown"]


def credibility_score(
    sample_size=None,
    year=None,
    study_type=None,
    citation_score=0.50,
    outcome_clarity=0.60
):
    """
    Weighted geometric mean credibility score.

    Components:
    S = log-normalized sample size
    D = study design quality
    R = exponential recency score
    C = citation / impact proxy
    Q = outcome clarity score
    """

    S = normalize_sample_size(sample_size)
    D = study_design_score(study_type)
    R = recency_score(year)
    C = citation_score
    Q = outcome_clarity

    weights = {
        "S": 0.25,
        "D": 0.30,
        "R": 0.15,
        "C": 0.15,
        "Q": 0.15
    }

    raw_score = (
        (S ** weights["S"]) *
        (D ** weights["D"]) *
        (R ** weights["R"]) *
        (C ** weights["C"]) *
        (Q ** weights["Q"])
    )

    return round(raw_score * 100, 2)