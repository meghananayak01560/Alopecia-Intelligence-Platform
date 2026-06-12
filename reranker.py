#to help the ai generated response to be more specific
def keyword_overlap_score(query,text):
  query_terms=set(query.lower().split())
  text_terms=set(text.lower().split())
  if not query_terms:
    return 0
  overlap=query_terms.intersection(text_terms)
  return len(overlap)/len(query_terms)

def med_score(query,text):
  q=query.lower()
  t=text.lower()
  score=0

  important_terms = [
  "alopecia areata",
  "female pattern",
  "androgenetic alopecia",
  "adolescent",
  "adolescents",
  "teen",
  "teenage",
  "pediatric",
  "women",
  "female",
  "hair loss",
  "girls",
  "ritlecitinib",
  "minoxidil",
  "baricitinib",
  "tofacitinib",
  "jak inhibitor",
  "homeopathic",
  "homeopathy",
  "natural",
  "herbal"]

  for term in important_terms:
    if term in q and term in t:
      score += 2
    elif term in t:
      score += 0.2
  
  return score



def rerank_results(query, results):
    reranked = []

    for result in results:
        text = result.get("text", "")

        vector_score = result.get("relevance_score", 0) / 100
        overlap = keyword_overlap_score(query, text)
        entity = med_score(query, text)

        final_score = (
            0.35 * vector_score +
            0.2 * overlap +
            0.45 * entity
        )

        result["rerank_score"] = round(final_score, 4)
        reranked.append(result)

    reranked = sorted(
        reranked,
        key=lambda x: x.get("rerank_score", 0),
        reverse=True
    )

    return reranked