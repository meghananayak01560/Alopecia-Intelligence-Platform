#creating my papers table
import sqlite3
DATABASE_NAME = 'Data/papers.db'

def create_papers_table():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS papers
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  PubMed_id TEXT UNIQUE,
                  title TEXT,
                  abstract TEXT,
                  journal TEXT,
                  year TEXT,
                  search_query TEXT,
                  url TEXT)''')

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chunks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paper_id INTEGER,
        pubmed_id TEXT,
        chunk_text TEXT,
        chunk_index INTEGER,
        FOREIGN KEY (paper_id) REFERENCES papers(id)
      )
  """)
    conn.commit()
    conn.close()

def insert_paper(PubMed_id, title, abstract, journal, year, url, search_query):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO papers 
        (pubmed_id, title, abstract, journal, year, url, search_query)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (PubMed_id, title, abstract, journal, year, url, search_query))

    conn.commit()
    conn.close()


def insert_chunk(paper_id, pubmed_id, chunk_text, chunk_index):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO chunks 
        (paper_id, pubmed_id, chunk_text, chunk_index)
        VALUES (?, ?, ?, ?)
    """, (paper_id, pubmed_id, chunk_text, chunk_index))

    conn.commit()
    conn.close()

#lets add a helper
def get_papers_with_abstracts():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, pubmed_id, title, abstract, journal, year, url 
        FROM papers 
        WHERE abstract IS NOT NULL AND abstract != ''
    """)
    papers = cursor.fetchall()
    conn.close()
    return papers

#need to take care of the duplicate chunks
def clear_chunks():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM chunks")

    conn.commit()
    conn.close()

def get_all_chunks():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, paper_id, pubmed_id, chunk_text, chunk_index 
        FROM chunks
    """)
    chunks = cursor.fetchall()
    conn.close()
    return chunks
