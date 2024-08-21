import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# OpenAI API 키 설정 (하드코딩)
OPENAI_API_KEY = ""

# Streamlit 애플리케이션 설정
st.title("GPT-3.5-turbo 질문 생성기")
st.write("GPT-3.5-turbo 모델에게 질문을 입력하고 답변을 받아보세요.")

# 사용자 입력 받기
user_input = st.text_input("질문을 입력하세요:")

# OpenAI GPT-3.5-turbo 모델 호출 설정
llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    model_name="gpt-3.5-turbo",
    temperature=0.99
)

# LangChain에서 사용할 프롬프트 템플릿 (단순 프롬프트)
prompt_template = PromptTemplate(
    input_variables=["question"],
    template="질문: {question}\n답변:"
)

# LLMChain 생성 (입력된 질문을 기반으로 GPT-3.5-turbo 호출)
chain = LLMChain(llm=llm, prompt=prompt_template)

# 사용자가 질문을 제출했을 때 GPT-3.5-turbo 호출
if user_input:
    # 질문을 기반으로 답변 생성
    response = chain.run(question=user_input)
    
    # 답변을 화면에 출력
    st.info(f"GPT-3.5-turbo의 답변: {response}")
