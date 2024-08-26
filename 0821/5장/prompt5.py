import streamlit as st
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

# OpenAI API 키
OPENAI_API_KEY = ''

# Streamlit 화면 구성
st.title("📄 텍스트 문서 기반 챗봇")
st.write("업로드한 텍스트 문서를 기반으로 질문에 답변하는 챗봇입니다.")

# 파일 업로드
uploaded_file = st.file_uploader("텍스트 파일을 업로드하세요", type=["txt"])

if uploaded_file is not None:
    # 파일 내용 읽기
    document = uploaded_file.read().decode("utf-8")
    
    # 문서 벡터화 및 임베딩 처리
    documents = [{"text": document}]
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    
    # FAISS 벡터 저장소 생성
    vector_store = FAISS.from_texts([doc["text"] for doc in documents], embeddings)
    
    # OpenAI GPT 모델 설정
    llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=vector_store.as_retriever(), chain_type="stuff")
    
    st.write("문서 처리가 완료되었습니다. 질문을 입력하세요!")
    
    # 질문 입력받기
    question = st.text_input("질문을 입력하세요:")
    
    # 질문에 대한 답변 출력
    if question:
        answer = qa_chain({"query": question})
        st.write("### 질문:")
        st.write(question)
        st.write("### 답변:")
        st.write(answer['result'])
