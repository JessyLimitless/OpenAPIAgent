import streamlit as st
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

# OpenAI API 키 입력받기
OPENAI_API_KEY = st.text_input("OpenAI API 키를 입력하세요", type="password")

# 문서 업로드 기능 구현 (인권 관련 문서)
uploaded_file = st.file_uploader("인권 관련 텍스트 파일을 업로드하세요", type=["txt"])

# 문서 처리 상태를 출력
if uploaded_file and OPENAI_API_KEY:
    # 문서를 스트림릿 파일 형식에서 텍스트로 변환
    document = uploaded_file.read().decode("utf-8")
    documents = [{"text": document}]
    
    # 문서 임베딩 생성
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    
    # Faiss 벡터스토어 생성
    vector_store = FAISS.from_texts([doc["text"] for doc in documents], embeddings)
    
    # 질문에 답변하는 체인 생성 (상담사 역할)
    llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=vector_store.as_retriever(), chain_type="stuff")
    
    st.success("문서 처리가 완료되었습니다.")
    
    # 사용자 질문 입력
    st.write("인권 상담사로서 여러분의 질문에 답변해드리겠습니다.")
    question = st.text_input("인권 관련 질문을 입력하세요")
    
    if question:
        # 질문에 답변
        answer = qa_chain({"query": question})
        st.write("질문:", question)
        st.write("상담사의 답변:", answer['result'])
else:
    st.warning("먼저 OpenAI API 키를 입력하고 문서를 업로드해주세요.")
