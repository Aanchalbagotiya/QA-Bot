import streamlit as st
import pdfplumber
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from rouge_score import rouge_scorer
import time

# Pre-trained Models
@st.cache_resource
def load_model():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    qa_model = pipeline("text2text-generation", model="google/flan-t5-base")
    return model, qa_model

model, qa_model = load_model()

# Custom CSS for UI Enhancements
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #4CAF50;
        margin-bottom: 20px;
    }
    .success-message {
        font-size: 1.2rem;
        color: #4CAF50;
    }
    .question-box {
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .answer-box {
        background-color: #e8f5e9;
        border-left: 5px solid #4CAF50;
        padding: 10px;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# App Title
st.markdown('<h1 class="main-header"> PDF QA Bot</h1>', unsafe_allow_html=True)

# File Upload Section - Multiple Files
uploaded_files = st.file_uploader("Upload PDF documents:", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    with st.spinner("Processing the uploaded PDFs..."):
        extracted_texts = []
        for uploaded_file in uploaded_files:
            try:
                # Extract Text from each PDF
                with pdfplumber.open(uploaded_file) as pdf:
                    extracted_text = " ".join(line.strip() for page in pdf.pages for line in page.extract_text().split("\n") if line.strip())
                    extracted_texts.append(extracted_text)
                st.markdown(f'<p class="success-message">File "{uploaded_file.name}" uploaded and processed successfully!</p>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error processing PDF '{uploaded_file.name}': {e}")
                extracted_texts.append("")

        # Combine all extracted texts into one corpus
        combined_text = " ".join(extracted_texts)
        
        # Text Preprocessing
        sentences = [combined_text[i:i+512] for i in range(0, len(combined_text), 512)]
        embeddings = model.encode(sentences)
        embeddings_array = np.array(embeddings).astype('float32')

        # Create FAISS Index
        dimension = embeddings_array.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings_array)

        # Save FAISS Index for Scalability
        faiss.write_index(index, "faiss_index.index")
        st.info("Content indexed. You can now ask questions.")

        # Query Input
        query = st.text_input("Enter your question:")

        if query:
            start_time = time.time()
            with st.spinner("Generating an answer..."):
                try:
                    # Embed the Query
                    query_embedding = model.encode([query]).astype('float32')
                    distances, indices = index.search(query_embedding, 5)

                    # Retrieve Context
                    retrieved_context = ". ".join([sentences[idx] for idx in indices[0]])

                    # Generate Answer
                    input_text = f"Context: {retrieved_context}\n\nQuestion: {query}\n\nAnswer:"
                    response = qa_model(input_text, max_length=100, do_sample=False)
                    generated_answer = response[0]["generated_text"]
                except Exception as e:
                    st.error(f"Error in generating answer: {e}")
                    generated_answer = ""
            
            end_time = time.time()

            # Display Generated Answer
            if generated_answer:
                st.markdown('<div class="answer-box"><strong>Answer:</strong></div>', unsafe_allow_html=True)
                st.write(generated_answer)

                # Metrics Section
                with st.expander("Evaluate the Model"):
                    # Response Time
                    st.write(f"Response Time: **{end_time - start_time:.2f} seconds**")

                    # User Rating
                    rating = st.slider("Rate the accuracy of the answer (1-5):", 1, 5)
                    st.write(f"Your rating: {rating}/5")

                    # Optional: Display ROUGE Score with Ground Truth (if available)
                    reference_answer = st.text_area("Enter reference answer for evaluation (optional):")
                    if reference_answer:
                        scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
                        scores = scorer.score(reference_answer, generated_answer)
                        st.write("ROUGE Scores:")
                        st.json(scores)

# Footer
st.markdown("---")
st.caption("Developed with ❤️ by Aanchal")