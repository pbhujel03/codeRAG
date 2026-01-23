from embeddings import query_index

def handle_query(index, metadata, query_text, k = 5):
    """
    Handles user Queries by searching the Faiss index
    """

    #call embeddings.py query_index_function
    top_chunks, distances = query_index(index, metadata, query_text, k)

    formatted_results = []

    for chunk, dist in zip(top_chunks, distances):
        
        formatted_results.append({
            "file": chunk["source"],
            "chunk_id": chunk["chunk_id"],
            "text": chunk["text"],
            "distance": dist
        })

    return formatted_results
    