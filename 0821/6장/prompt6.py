import streamlit as st
from PyPDF2 import PdfReader
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

# OpenAI API Key
OPENAI_API_KEY = ""

# Function to extract text from the uploaded PDF
def get_pdf_text(pdf_file):
    text = ""
    pdf_reader = PdfReader(pdf_file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to split the extracted text into manageable chunks
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n"],
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

# Function to convert text chunks into a vector store using FAISS
def get_vectorstore(text_chunks):
    embeddings = SentenceTransformerEmbeddings(model_name='all-MiniLM-L6-v2')
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

# Function to create a conversational chain using Langchain
def get_conversation_chain(vectorstore):
    memory = ConversationBufferWindowMemory(memory_key='chat_history', return_messages=True, window_size=10)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo', openai_api_key=OPENAI_API_KEY),
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

# Streamlit App Design
st.title("PDF 기반 챗봇")
st.write("PDF 파일을 업로드하고 질문을 통해 챗봇과 상호작용하세요.")

# File uploader for PDF
pdf_file = st.file_uploader("PDF 파일을 업로드하세요", type="pdf")

if pdf_file is not None:
    # Extract text from PDF
    raw_text = get_pdf_text(pdf_file)
    
    # Process text and create vectorstore
    text_chunks = get_text_chunks(raw_text)
    vectorstore = get_vectorstore(text_chunks)
    conversation = get_conversation_chain(vectorstore)
    
    # Initialize chat history
    chat_history = []

    # Input for user questions
    user_question = st.text_input("질문을 입력하세요:", key="input_text")

    if st.button("질문 제출"):
        # Process user question and display response
        if user_question:
            chat_history.append({"role": "user", "content": user_question})
            result = conversation({"question": user_question, "chat_history": chat_history})
            response = result["answer"]
            chat_history.append({"role": "assistant", "content": response})
            
            # Display the chatbot's response
            st.write(f"**챗봇 응답:** {response}")
