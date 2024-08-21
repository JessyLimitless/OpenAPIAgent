import streamlit as st
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import openai

# OpenAI API 키 설정
OPENAI_API_KEY = ''
openai.api_key = OPENAI_API_KEY

# 텍스트 파일 로드 함수
def load_text(uploaded_file):
    text = uploaded_file.read().decode('utf-8')
    return text

# Streamlit UI 설정
st.title("내부 문서 Q&A 시스템")

# 텍스트 파일 업로드
uploaded_file = st.file_uploader("텍스트 파일을 업로드하세요", type=["txt"])
if uploaded_file is not None:
    # 텍스트 파일 로드
    document = load_text(uploaded_file)
    # 문서를 Langchain 형식으로 로드
    documents = [{"text": document}]
    
    # 문서 임베딩 생성
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    
    # Faiss 벡터스토어 생성
    vector_store = FAISS.from_texts([doc["text"] for doc in documents], embeddings)
    
    # 질문에 답변하는 체인 생성
    llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")
    retriever = vector_store.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=retriever, chain_type="stuff")
    
    # 질문 입력 및 처리
    question = st.text_input("질문을 입력하세요:", key="question")
    
    if question:
        # 역할을 부여하여 시스템 메시지 생성
        system_message = "당신은 인권위원회 담당관입니다. 인권침해 여부를 들어주고 상담해주는 역할을 합니다."
        prompt = f"{system_message}\n\nUser: {question}\n\nAssistant:"
        
        # 답변 생성
        answer = qa_chain({"query": prompt})["result"]
        
        st.write("답변:", answer)
