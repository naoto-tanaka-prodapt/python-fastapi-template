from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from config import settings
from qdrant_client.http.models import Distance, VectorParams
from langchain_core.documents import Document

from utils import extract_text_from_pdf_bytes

def get_vector_store():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=settings.OPENAI_API_KEY)
    vector_store = QdrantVectorStore.from_existing_collection(embedding=embeddings, collection_name="resumes", path="qdrant_store")
    return vector_store

def inmemory_vector_store():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=settings.OPENAI_API_KEY)
    client = QdrantClient(":memory:")
    client.create_collection(collection_name="resumes", vectors_config=VectorParams(size=3072, distance=Distance.COSINE))
    vector_store = QdrantVectorStore(client=client, collection_name="resumes", embedding=embeddings)
    
    try:
        yield vector_store
    finally:
        client.close()

def ingest_resume(resume_text: str, resume_url: str, resume_id: int, vector_store: QdrantVectorStore):
    doc = Document(page_content=resume_text, metadata={"url": resume_url})
    vector_store.add_documents(documents=[doc], ids=[resume_id])

def ingest_resume_for_recommendataions(resume, filename, resume_id, vector_store):
    resume_raw_text = extract_text_from_pdf_bytes(resume)
    ingest_resume(resume_raw_text, filename, resume_id, vector_store)

def get_recommendation(description: str, vector_store: QdrantVectorStore):
    retriever = vector_store.as_retriever(search_kwargs={"k": 1})
    recommend_applicant = retriever.invoke(description)
    return recommend_applicant[0]