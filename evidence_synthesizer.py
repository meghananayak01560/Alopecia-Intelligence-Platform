# evidence_synthesizer.py

TREATMENT_TERMS = [
    "ritlecitinib",
    "minoxidil",
    "baricitinib",
    "tofacitinib",
    "corticosteroid",
    "steroid",
    "jak inhibitor",
    "janus kinase inhibitor",
    "immunotherapy",
    "homeopathic",
    "homeopathy",
    "herbal",
    "natural",
    "ayurvedic"
]

POPULATION_TERMS = [
    "adolescent",
    "adolescents",
    "teen",
    "teenage",
    "children",
    "pediatric",
    "women",
    "female",
    "girls"
]

OUTCOME_TERMS = [
    "hair regrowth",
    "improvement",
    "significant improvement",
    "well tolerated",
    "safe",
    "adverse effects",
    "relapse",
    "quality of life",
    "efficacy",
    "effectiveness"
]


def extract_terms(text, term_list):
    text_lower = text.lower()
    return [term for term in term_list if term in text_lower]


def summarize_evidence_row(row, query):
    snippet = row.get("snippet", "")
    pubmed_id = row.get("pubmed_id", "Unknown")
    relevance = row.get("relevance_score", 0)
    direction = row.get("direction", "Unclear")

    treatments = extract_terms(snippet, TREATMENT_TERMS)
    populations = extract_terms(snippet, POPULATION_TERMS)
    outcomes = extract_terms(snippet, OUTCOME_TERMS)

    if treatments:
        treatment_summary = ", ".join(treatments)
    else:
        treatment_summary = "No specific treatment clearly identified"

    if populations:
        population_summary = ", ".join(populations)
    else:
        population_summary = "Population not clearly specified"

    if outcomes:
        outcome_summary = ", ".join(outcomes)
    else:
        outcome_summary = "No clear outcome terms detected"

    return {
        "pubmed_id": pubmed_id,
        "relevance_score": relevance,
        "evidence_direction": direction,
        "treatments_detected": treatment_summary,
        "population_detected": population_summary,
        "outcomes_detected": outcome_summary,
        "study_takeaway": (
            f"This source appears to discuss {treatment_summary}. "
            f"The population focus appears to include: {population_summary}. "
            f"Relevant outcomes mentioned include: {outcome_summary}. "
            f"Source relevance score: {relevance}."
        )
    }


def synthesize_across_studies(query, study_summaries):
    query_lower = query.lower()

    all_treatments = []
    all_populations = []
    all_outcomes = []

    for study in study_summaries:
        all_treatments.extend(study["treatments_detected"].split(", "))
        all_populations.extend(study["population_detected"].split(", "))
        all_outcomes.extend(study["outcomes_detected"].split(", "))

    all_treatments = sorted(set([x for x in all_treatments if x and x != "No specific treatment clearly identified"]))
    all_populations = sorted(set([x for x in all_populations if x and x != "Population not clearly specified"]))
    all_outcomes = sorted(set([x for x in all_outcomes if x and x != "No clear outcome terms detected"]))

    asks_homeopathy = any(term in query_lower for term in ["homeopathic", "homeopathy", "natural", "herbal", "ayurvedic", "holistic"])
    asks_teen = any(term in query_lower for term in ["teen", "teenage", "adolescent", "13", "14", "15", "girls"])
    asks_women = any(term in query_lower for term in ["women", "female", "woman", "girls"])

    direct_homeopathy_found = any(term in all_treatments for term in ["homeopathic", "homeopathy", "herbal", "natural", "ayurvedic"])

    if asks_homeopathy and not direct_homeopathy_found:
        final_conclusion = (
            "The retrieved evidence does not directly support a conclusion that homeopathic treatments are effective for alopecia. "
            "The retrieved studies appear to focus more on biomedical or pharmaceutical treatments rather than homeopathic interventions. "
            "This means the evidence gap itself is important: the system found alopecia-related research, but not direct homeopathy-specific evidence. "
            "A strong conclusion would require studies that specifically test homeopathic treatments and measure hair regrowth, safety, and relapse outcomes."
        )
    elif all_treatments:
        final_conclusion = (
            f"Across the retrieved evidence, the main treatments identified were: {', '.join(all_treatments)}. "
            "The evidence should be interpreted according to alopecia type, disease severity, patient age, and study quality. "
            "The system should not treat one retrieved medication as universally best without clinician review."
        )
    else:
        final_conclusion = (
            "The retrieved evidence is not specific enough to identify a clear treatment conclusion. "
            "More targeted studies are needed for this question."
        )

    evidence_gaps = []

    if asks_homeopathy and not direct_homeopathy_found:
        evidence_gaps.append("No directly retrieved studies on homeopathic treatments were identified.")

    if asks_teen and not any(pop in all_populations for pop in ["adolescent", "adolescents", "teen", "teenage", "children", "pediatric", "girls"]):
        evidence_gaps.append("The retrieved evidence may not sufficiently focus on adolescents or teenage girls.")

    if asks_women and not any(pop in all_populations for pop in ["women", "female", "girls"]):
        evidence_gaps.append("The retrieved evidence may not sufficiently focus on women or girls.")

    if not evidence_gaps:
        evidence_gaps.append("No major evidence gap was automatically detected, but clinical interpretation is still required.")

    return {
        "final_conclusion": final_conclusion,
        "treatments_found": all_treatments,
        "populations_found": all_populations,
        "outcomes_found": all_outcomes,
        "evidence_gaps": evidence_gaps
    }


def build_evidence_synthesis(query, evidence_rows):
    study_summaries = [
        summarize_evidence_row(row, query)
        for row in evidence_rows
    ]

    synthesis = synthesize_across_studies(query, study_summaries)

    return {
        "study_summaries": study_summaries,
        "synthesis": synthesis
    }