import streamlit as st
from embeddings import process_files
from queryHandler import handle_query
import ollama

st.set_page_config(page_title = "Code Rag Assistant")
st.title("Code RAG Assistant")
st.write("Upload your project files and ask questions about your code.")

uploaded_files = st.file_uploader(
    "upload your project files",
    accept_multiple_files = True
)

if uploaded_files:
    index, embeddings, metadata = process_files(uploaded_files)
    st.success("Files Processed. You can now ask questions about yoyur code.")

    query = st.text_input("Ask a question about your code")

    if query:
        results = handle_query(index, metadata, query)

        if results:
            context = "\n\n".join([res["text"] for res in results])

            prompt = f"""
            you are a code assistant. Answer the question based on the code below.

            code:
            {context}
            
            Question:
            {query}
            """

            response = ollama.chat(
                model = "llama3",
                messages=[{"role":"user","content":prompt}]
            )
            llm_response = response["message"]["content"]

            st.subheader("Answer")
            st.text_area("Answer",llm_response, height = 400)
            
