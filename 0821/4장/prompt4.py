import streamlit as st
from langchain import OpenAI
from langchain.prompts import PromptTemplate

# OpenAI API 키 하드코딩
openai_api_key = ""

# GPT 모델 초기화 (temperature를 0.99로 설정)
llm = OpenAI(temperature=0.99, api_key=openai_api_key)

# Streamlit UI 구성
st.title("과학 주제 설명 앱")
st.write("복잡한 과학 주제를 초등학생이 이해할 수 있도록 설명해 드립니다.")

# 사용자 입력
topic = st.text_input("설명하고 싶은 과학 주제를 입력하세요:")

# 설명 생성 함수
def generate_simple_explanation(topic):
    prompt_template = PromptTemplate(
        input_variables=["topic"],
        template=(
            "주제: {topic}\n\n"
            "이 주제를 초등학생이 쉽게 이해할 수 있도록 간단한 문장과 일상적인 예시를 사용해 설명해 주세요."
        )
    )
    
    # LLM에 Prompt를 입력하여 응답 생성
    prompt = prompt_template.format(topic=topic)
    response = llm(prompt)
    
    return response

# 사용자 입력이 있을 때 GPT 모델 호출
if topic:
    with st.spinner("GPT-3.5가 설명을 생성 중입니다..."):
        explanation = generate_simple_explanation(topic)
    
    # 결과 출력
    st.subheader("초등학생을 위한 설명")
    st.write(explanation)
