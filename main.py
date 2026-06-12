#main function for the projectttt <3

from database import create_papers_table
from data_ing import ingest_papers
from chunkyyyy import chunk_all_abstracts
from embeddings import build_vector_database

def Main():
    create_papers_table()
    ingest_papers()
    chunk_all_abstracts()
    build_vector_database()
    print("done")

if __name__ == "__main__":
    Main()