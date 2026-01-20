import os

ALLOWED_EXTENSIONS = {
    ".py",
    ".php",
    ".html",
    ".css",
    ".js",
    ".sql",
    ".txt"
}

def is_supported_file(filename: str)->bool:
    _, ext = os.path.splitext(filename)
    return ext.lower() in ALLOWED_EXTENSIONS

def extract_text(uploaded_files):
    extracted = []

    for file in uploaded_files:
        if not is_supported_file(file.name):
            continue
        
        try:
            content = file.read().decode("utf-8", errors = "ignore")
            extracted.append({
                "filename": file.name,
                "content": content
            })
        except Exception as e :
            print(f"Error reading file{file.name}: {e}")
        
    return extracted

def chunk_text(text, chunk_size=200, overlap= 20):

    lines = text.splitlines()
    chunks = []
    # current_chunk = []
    if overlap >= chunk_size:
        raise ValueError("Overlap must be smaller than chunk size")
    
    else:
        start = 0
        while start < len(lines):
            end = start + chunk_size
            chunk = "\n".join(lines[start:end])
            chunks.append(chunk)
            start = end - overlap

    return chunks

def prepare_code_chunks(uploaded_files):
    all_chunks = []
    extracted_files = extract_text(uploaded_files)

    for file in extracted_files:
        chunks = chunk_text(file["content"])

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "text":chunk,
                "source": file["filename"],
                "chunk_id":i
            })

    return all_chunks


