# we can add more terms as we think of them, but this is a starting point for identifying supportive vs limiting evidence in the retrieved results

SUPPORTIVE_TERMS = [
    "effective", "improved", "significant improvement", "increased hair density",
    "increased hair growth", "beneficial", "positive response", "successful","well tolerated",
"safe",
"major hair regrowth",
"hair regrowth",
"improvements",
"significant improvements",
"worked better",
"promoting hair regrowth",
"approved",
"efficacy"
]

LIMITING_TERMS = [
    "not significant", "no significant", "limited evidence", "mixed results",
    "inconclusive", "no improvement", "adverse effects", "failed", "unclear"
]


def analyze_evidence_direction(retrieved_results):
    supportive_count = 0
    limiting_count = 0
    neutral_count = 0

    for result in retrieved_results:
        text = result["text"].lower()

        has_supportive = any(term in text for term in SUPPORTIVE_TERMS)
        has_limiting = any(term in text for term in LIMITING_TERMS)

        if has_supportive and has_limiting:
            neutral_count += 1
        elif has_supportive:
            supportive_count += 1
        elif has_limiting:
            limiting_count += 1
        else:
            neutral_count += 1

    if supportive_count > 0 and limiting_count > 0:
        conclusion = "Mixed evidence detected"
    elif supportive_count > limiting_count:
        conclusion = "Mostly supportive evidence"
    elif limiting_count > supportive_count:
        conclusion = "Mostly limited or negative evidence"
    else:
        conclusion = "Evidence direction is unclear"

    return {
        "supportive_count": supportive_count,
        "limiting_count": limiting_count,
        "neutral_count": neutral_count,
        "conclusion": conclusion
    }