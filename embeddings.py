from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from textUtils import prepare_code_chunks

model = SentenceTransformer("all-MiniLM-L6-v2")

def create_embeddings(chunks):
    return model.encode(chunks,convert_to_numpy=True)

def build_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    faiss.normalize_L2(embeddings)
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)
    return index

def search_faiss(index, query_embedding, k=5):
    query_embedding = query_embedding.reshape(1,-1)
    distances, indices = index.search(query_embedding, k)
    return distances, indices

def process_files(uploaded_files):

    #prepare chunks from uploaded files
    all_chunks = prepare_code_chunks(uploaded_files)

    #keep parallel meta data list
    metadata = all_chunks

    #create_embeddings for all chunk texts
    embeddings = create_embeddings([c["text"] for c in all_chunks])

    #build Faiss index
    index = build_faiss_index(embeddings)

    return index, embeddings, metadata

def query_index(index, metadata, query_text, k = 5):
    #embed the query
    query_embedding = create_embeddings([query_text])

    #search Faiss
    distances, indices = search_faiss(index, query_embedding, k)

    #map indices to meta data
    top_chunks = [metadata[i] for i in indices[0]]

    return top_chunks, distances[0]
