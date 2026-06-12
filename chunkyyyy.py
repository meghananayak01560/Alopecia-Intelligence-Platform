from database import get_papers_with_abstracts, insert_chunk, clear_chunks

def split_text_into_chunks(text, max_words=120, overlap=25):
  """This def splits long texts into overlapping word chunks for optimal processing.
  max_words: max number of words in each chunk
  overlap: number of words that overlap between consecutive chunks
  
  """
  words=text.split()
  if len(words) <= max_words:
    return [text]
  chunks=[]
  start=0
  while start < len(words):
    end = start + max_words
    chunk = " ".join(words[start:end])
    chunks.append(chunk)
    start += max_words - overlap
  return chunks

def chunk_all_abstracts():
    clear_chunks()  # Clear existing chunks to avoid duplicates
    papers = get_papers_with_abstracts()
    total_chunks = 0
        
    # The *_ takes the remaining 3 columns so Python doesn't crash
    for paper_id, pubmed_id, title, abstract, *_ in papers:
        full_text = f"{title}. {abstract}"

        chunks = split_text_into_chunks(full_text)

        for index, chunk_text in enumerate(chunks):
            insert_chunk(
                paper_id=paper_id,
                pubmed_id=pubmed_id,
                chunk_text=chunk_text,
                chunk_index=index
            )

            total_chunks += 1

    print(f"Successfully created {total_chunks} text chunks!")
