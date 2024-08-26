import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

# OpenAI API Key (하드코딩)
OPENAI_API_KEY = ""

# OpenAI GPT-3.5-turbo 모델을 호출하는 함수
def get_gpt3_response(question):
    # ChatOpenAI 클래스를 통해 모델을 호출
    chat = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        model="gpt-3.5-turbo",
        temperature=0.99
    )
    
    # 프롬프트 템플릿을 정의 (기본적으로 사용자 질문을 전달)
    prompt_template = ChatPromptTemplate.from_template("Q: {question}\nA:")
    
    # LangChain의 LLMChain을 사용하여 호출 체인을 만듦
    chain = LLMChain(llm=chat, prompt=prompt_template)
    
    # 체인에 사용자 질문을 입력하고 답변 생성
    response = chain.run({"question": question})
    return response

# Streamlit 앱 설정
st.title("GPT-3.5-turbo Q&A")
st.write("GPT-3.5-turbo 모델에게 질문을 입력하고 답변을 받아보세요.")

# 사용자 입력을 받는 텍스트 폼
question = st.text_input("질문을 입력하세요:")

# 질문이 입력되면 GPT-3.5-turbo 모델을 호출
if question:
    with st.spinner("GPT-3.5-turbo 모델이 답변을 생성 중입니다..."):
        answer = get_gpt3_response(question)
        
        # 생성된 답변을 화면에 표시
        st.info(answer)
