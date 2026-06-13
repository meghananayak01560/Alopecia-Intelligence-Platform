import chromadb
from sentence_transformers import SentenceTransformer
chroma_path="Data/chroma_db"
collection_name="AR_chunks"
model=SentenceTransformer('all-MiniLM-L6-v2')

def search_research_chunks(query, top_k=5):
    client = chromadb.PersistentClient(path=chroma_path)
    collection = client.get_collection(name=collection_name)

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    retrieved_chunks = []

    for i in range(len(results["documents"][0])):
        metadata = results["metadatas"][0][i] or {}

        pubmed_id = (
            metadata.get("pubmed_id")
            or metadata.get("pmid")
            or metadata.get("PMID")
            or metadata.get("id")
            or metadata.get("source")
            or "Unknown"
        )

        distance = results["distances"][0][i]

        relevance_score = round(max(0, 1 - distance) * 100, 2)

        retrieved_chunks.append({
            "text": results["documents"][0][i],
            "metadata": metadata,
            "pubmed_id": pubmed_id,
            "distance": distance,
            "relevance_score": relevance_score
        })

    return retrieved_chunks
if __name__ == "__main__":
  query = "What does research say about minoxidil for young women with alopecia?"
  results = search_research_chunks(query)
  
  for i, result in enumerate(results, start=1):
        print(f"\nResult {i}")
        print("Distance:", result["distance"])
        print("Metadata:", result["metadata"])
        print(result["text"][:500])