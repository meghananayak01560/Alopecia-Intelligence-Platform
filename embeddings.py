import chromadb
from sentence_transformers import SentenceTransformer
from database import get_all_chunks

chroma_path="data/chroma_db"
collection_name="AR_chunks"

def build_vector_database():
  """Converts text chunks into embeddings, stores in ChromaDB vector database for efficient retrieval."""
  print("Now loading the embedding model...")
  model = SentenceTransformer('all-MiniLM-L6-v2')
  print("Connecting to ChromaDB...")
  client = chromadb.PersistentClient(path=chroma_path)
  
  try:
    client.delete_collection(collection_name)
  except Exception:
    pass

  collection=client.get_or_create_collection(name=collection_name)

  chunks=get_all_chunks()
  if not chunks:
    print("No chunks found in the database. Please run the ingestion and chunking steps first.")
    return
  
  ids=[]
  embeddings=[]
  metadatas=[]
  documents=[]
  print(f"Processing {len(chunks)} text chunks to create embeddings...")
  for chunk_id, paper_id, pubmed_id, chunk_text, chunk_index in chunks:
    embedding=model.encode(chunk_text).tolist()
    ids.append(str(chunk_id))
    embeddings.append(embedding)
    documents.append(chunk_text)
    metadatas.append({
        "paper_id": paper_id,
        "pubmed_id": pubmed_id,
        "chunk_index": chunk_index
    })
  collection.add(
    ids=ids, documents=documents, metadatas=metadatas, embeddings=embeddings
  )

  print(f"Successfully stored {len(chunks)} text chunks in the ChromaDB!")