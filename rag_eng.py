# rag_eng.py
from evidence_synthesizer import build_evidence_synthesis
from advanced_aiengine import build_advanced_outputs
# from transformers import pipeline
from reranker import rerank_results
from retrieval import search_research_chunks
from contradiction_detector import analyze_evidence_direction

# generator = pipeline(
#     "text2text-generation",
#     model="google/flan-t5-base"
# )

def clean_answer(raw_answer, query, context, sources):
    if not raw_answer:
        raw_answer = ""

    query_lower = query.lower()
    context_lower = context.lower()
    answer = raw_answer.strip()

    source_text = ", ".join(str(source) for source in sources if source != "Unknown")

    asks_homeopathic = any(term in query_lower for term in [
        "homeopathic", "homeopathy", "natural", "holistic", "herbal", "ayurvedic"
    ])

    asks_women = any(term in query_lower for term in [
        "women", "woman", "female", "girls", "girl"
    ])

    asks_teen = any(term in query_lower for term in [
        "teen", "teenage", "adolescent", "14", "15", "13"
    ])

    mentioned_treatments = []

    for treatment in ["ritlecitinib", "minoxidil", "baricitinib", "tofacitinib", "corticosteroids", "jak inhibitors"]:
        if treatment in context_lower:
            mentioned_treatments.append(treatment)

    mentioned_treatments = list(dict.fromkeys(mentioned_treatments))

    # If the model gives a weak/title-only answer, synthesize one ourselves
    if len(answer.split()) < 25 or "be cautious for children" in answer.lower():
        if asks_homeopathic:
            treatment_text = (
                f"The retrieved evidence mainly discusses {', '.join(mentioned_treatments)}"
                if mentioned_treatments else
                "The retrieved evidence does not clearly identify specific homeopathic treatments"
            )

            population_text = "women"
            if asks_teen:
                population_text = "adolescent girls"
            elif asks_women:
                population_text = "women"

            return (
                f"For {population_text}, the retrieved literature does not provide strong direct evidence "
                f"that homeopathic treatments are effective for alopecia. {treatment_text}, which means the current "
                "retrieved evidence is not well matched to the homeopathic part of the question. "
                "A more confident answer would require studies specifically testing homeopathic treatments, with outcomes "
                "such as hair regrowth, relapse rate, safety, and quality of life. Based on the current retrieved context, "
                "the safest conclusion is that evidence for homeopathic treatment is insufficient rather than supportive."
            )

        if "ritlecitinib" in context_lower:
            return (
                "Based on the retrieved evidence, ritlecitinib appears to have supportive evidence for severe alopecia areata, "
                "including in adolescents age 12 and older. However, this does not mean it is the best medication for every patient. "
                "Treatment choice depends on alopecia type, severity, age, medical history, side effects, and dermatologist evaluation. "
                f"The relevant PubMed sources include: {source_text}."
            )

        if "minoxidil" in context_lower:
            return (
                "Based on the retrieved evidence, topical minoxidil appears relevant for female pattern hair loss, "
                "but it may not apply to every type of alopecia. For women or adolescent girls, the diagnosis matters because "
                "alopecia areata, female pattern hair loss, telogen effluvium, and scarring alopecias are treated differently. "
                f"The relevant PubMed sources include: {source_text}."
            )

        return (
            "The retrieved literature does not provide enough directly matched evidence to give a confident treatment answer. "
            "The question may require more specific studies based on alopecia type, patient age, sex, treatment category, and outcomes. "
            f"The retrieved PubMed sources include: {source_text}."
        )

    return answer

def build_prompt(query, context, sources):
    source_text = ", ".join(str(s) for s in sources)

    return f"""
You are a biomedical research assistant analyzing alopecia treatment literature.

Use ONLY the retrieved context below.

Write a useful answer for a non-expert user.

Your answer must:
- Directly answer the question
- Avoid saying any medication is the guaranteed best option
- Mention that treatment depends on dermatologist evaluation
- Be cautious for children and teenagers
- Summarize the evidence in 4 to 6 sentences
- Mention the PubMed IDs used

Question:
{query}

Retrieved context:
{context}

PubMed IDs:
{source_text}

Answer:
"""

def generate_research_insights(evidence_rows):
    insights = []

    supportive = sum(row["supportive_count"] for row in evidence_rows)
    limiting = sum(row["limiting_count"] for row in evidence_rows)

    medications = []

    for row in evidence_rows:
        text = row["snippet"].lower()

        if "ritlecitinib" in text:
            medications.append("ritlecitinib")
        if "minoxidil" in text:
            medications.append("minoxidil")
        if "jak inhibitor" in text or "janus kinase" in text:
            medications.append("JAK inhibitors")

    medications = list(set(medications))

    if medications:
        insights.append(f"Treatments mentioned: {', '.join(medications)}.")

    if supportive > limiting:
        insights.append("Retrieved evidence leans supportive overall.")
    elif limiting > supportive:
        insights.append("Retrieved evidence includes more limiting or negative language.")
    else:
        insights.append("Retrieved evidence is mixed or unclear.")

    if any("adolescent" in row["snippet"].lower() or "12 years" in row["snippet"].lower() for row in evidence_rows):
        insights.append("Some retrieved evidence includes adolescent patients.")

    if any("limited" in row["snippet"].lower() for row in evidence_rows):
        insights.append("At least one source notes limited real-world evidence.")

    return insights

def detect_query_scope(query, results):
    query_lower = query.lower()

    alternative_terms = [
        "homeopathic",
        "homeopathy",
        "natural",
        "herbal",
        "ayurvedic",
        "holistic",
        "essential oil",
        "supplement",
        "vitamin",
        "diet"
    ]

    medication_terms = [
        "ritlecitinib",
        "minoxidil",
        "jak inhibitor",
        "janus kinase",
        "baricitinib",
        "tofacitinib",
        "corticosteroid",
        "steroid",
        "immunotherapy"
    ]

    retrieved_text = " ".join(result.get("text", "").lower() for result in results)

    query_mentions_alternative = any(term in query_lower for term in alternative_terms)
    retrieved_mentions_alternative = any(term in retrieved_text for term in alternative_terms)

    retrieved_mentions_medication = any(term in retrieved_text for term in medication_terms)

    if query_mentions_alternative and not retrieved_mentions_alternative:
        return {
            "status": "low_direct_evidence",
            "message": (
                "The query asks about homeopathic, natural, or alternative treatments, but the retrieved literature "
                "does not appear to directly study those treatments. The answer should explain that evidence is insufficient "
                "rather than using unrelated medication studies as support."
            )
        }

    if len(results) == 0:
        return {
            "status": "no_results",
            "message": "No relevant research chunks were retrieved for this question."
        }

    if not retrieved_mentions_medication and not retrieved_mentions_alternative:
        return {
            "status": "low_confidence",
            "message": (
                "The retrieved evidence may not be specific enough to answer this question confidently."
            )
        }

    return {
        "status": "in_scope",
        "message": "The retrieved evidence appears relevant enough for a source-grounded answer."
    }

def answer_question(query, top_k=5):
    results = search_research_chunks(query, top_k=max(top_k * 3, 10))
    results = rerank_results(query, results)
    results = results[:top_k]
    query_scope = detect_query_scope(query, results)
    #each paper appear only 1x
    seen_pmids = set()
    unique_results = []

    for result in results:
        pmid = result.get("pubmed_id", "Unknown")

        if pmid not in seen_pmids:
            unique_results.append(result)
            seen_pmids.add(pmid)

    results = unique_results

    if query_scope["status"] == "in_scope":
        evidence_direction = analyze_evidence_direction(results)
    else:
        evidence_direction = {
            "supportive_count": 0,
            "limiting_count": 0,
            "neutral_count": len(results),
            "conclusion": "Evidence not directly applicable"
        }

    evidence_rows = []

    for i, result in enumerate(results, start=1):
        text = result.get("text", "")
        pubmed_id = (
            result.get("pubmed_id")
            or result.get("pmid")
            or result.get("id")
            or result.get("source")
            or "Unknown"
        )

        row_direction = analyze_evidence_direction([result])

        evidence_rows.append({
            "rank": i,
            "pubmed_id": pubmed_id,
            "pubmed_link": f"https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/" if pubmed_id != "Unknown" else "",
            "relevance_score": result.get("relevance_score", 0),
            "snippet": text[:600] + "..." if len(text) > 600 else text,
            "direction": row_direction.get("conclusion", "Unclear"),
            "supportive_count": row_direction.get("supportive_count", 0),
            "limiting_count": row_direction.get("limiting_count", 0),
            "neutral_count": row_direction.get("neutral_count", 0),
            "rerank_score": result.get("rerank_score",0)
        })

    advanced_outputs = build_advanced_outputs(query, evidence_rows, evidence_direction)
    answer = advanced_outputs["answer"]
    evidence_synthesis = build_evidence_synthesis(query, evidence_rows)
    research_insights = generate_research_insights(evidence_rows)
    

    sources = [row["pubmed_id"] for row in evidence_rows]
    context = "\n\n".join(row["snippet"] for row in evidence_rows)

    return {
        "answer": answer,
        "sources": sources,
        "retrieved_context": context,
        "evidence_direction": evidence_direction,
        "evidence_table": evidence_rows,
        "research_insights": research_insights,
        "query_scope": query_scope,
        "evidence_synthesis": evidence_synthesis,
        "advanced_outputs": advanced_outputs
    }

    # Otherwise generate AI answer normally
    prompt = build_prompt(query, context, sources)

    output = generator(
        prompt,
        max_new_tokens=220,
        do_sample=False
    )

    answer = clean_answer(output[0]["generated_text"], query, context, sources)

    return {
        "answer": answer,
        "sources": sources,
        "retrieved_context": context,
        "evidence_direction": evidence_direction,
        "evidence_table": evidence_rows,
        "research_insights": research_insights,
        "query_scope": query_scope
    }


if __name__ == "__main__":
    question = "What is the best medication for alopecia in teenage girls?"
    output = answer_question(question)

    print("\nANSWER:")
    print(output["answer"])

    print("\nSOURCES:")
    print(output["sources"])

    print("\nEVIDENCE DIRECTION:")
    print(output["evidence_direction"])

    print("\nEVIDENCE TABLE:")
    for row in output["evidence_table"]:
        print(row)