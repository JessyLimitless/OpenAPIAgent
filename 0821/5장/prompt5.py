import streamlit as st
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

# OpenAI API Key 입력
OPENAI_API_KEY = ''

# 텍스트 파일 로드 함수
def load_text(file):
    text = file.read().decode("utf-8")
    return text

# Streamlit UI 구성
st.title("문서 기반 챗봇")
st.write("텍스트 문서를 업로드하고, 질문을 입력하면 문서에 기반한 답변을 받을 수 있습니다.")

# 텍스트 파일 업로드
uploaded_file = st.file_uploader("텍스트 파일을 업로드하세요", type=["txt"])

if uploaded_file is not None:
    # 파일 로드 및 문서 처리
    document = load_text(uploaded_file)
    documents = [{"text": document}]
    
    # 문서 임베딩 생성
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    
    # Faiss 벡터스토어 생성
    vector_store = FAISS.from_texts([doc["text"] for doc in documents], embeddings)
    
    # 질문에 답변하는 체인 생성
    llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=vector_store.as_retriever(), chain_type="stuff")
    
    st.success("문서 처리가 완료되었습니다. 질문을 입력해보세요.")
    
    # 질문 입력 및 답변 처리
    question = st.text_input("질문을 입력하세요:")
    
    if question:
        answer = qa_chain({"query": question})
        st.write("**질문:**", question)
        st.write("**답변:**", answer['result'])
