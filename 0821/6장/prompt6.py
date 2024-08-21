import streamlit as st
from PyPDF2 import PdfReader
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tempfile  # 임시 파일을 다루기 위한 모듈

# OpenAI API Key 설정 (직접 입력)
OPENAI_API_KEY = ""

# PDF 파일에서 텍스트 추출
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# 텍스트를 청크로 분할
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n"],  
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

# 텍스트 청크를 벡터 스토어로 변환
def get_vectorstore(text_chunks):
    embeddings = SentenceTransformerEmbeddings(model_name='all-MiniLM-L6-v2')
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

# 대화 체인 생성
def get_conversation_chain(vectorstore):
    memory = ConversationBufferWindowMemory(memory_key='chat_history', return_messages=True, window_size=10)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo', openai_api_key=OPENAI_API_KEY),
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

# 스트림릿 앱 실행
def main():
    st.title("PDF 기반 챗봇")

    # 파일 업로드
    pdf_file = st.file_uploader("PDF 파일을 업로드하세요", type=["pdf"])

    if pdf_file is not None:
        # 임시 파일로 저장
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(pdf_file.read())
            tmp_file_path = tmp_file.name

        # PDF 텍스트 추출 및 벡터화
        raw_text = get_pdf_text([tmp_file_path])  # 임시 파일 경로 사용
        text_chunks = get_text_chunks(raw_text)
        vectorstore = get_vectorstore(text_chunks)
        conversation = get_conversation_chain(vectorstore)

        # 대화 저장소 초기화
        chat_history = []

        # 질문 입력 및 처리
        question = st.text_input("질문을 입력하세요:")

        if st.button("질문하기") and question:
            chat_history.append({"role": "user", "content": question})
            result = conversation({
                "question": question,
                "chat_history": chat_history
            })
            response = result["answer"]
            chat_history.append({"role": "assistant", "content": response})
            st.write(f"응답: {response}")

    else:
        st.write("PDF 파일을 업로드하세요.")

if __name__ == "__main__":
    main()
