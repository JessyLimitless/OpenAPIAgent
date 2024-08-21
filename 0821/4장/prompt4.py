import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

# OpenAI API 설정 (하드 코딩된 API 키)
OPENAI_API_KEY = ""  # 여기에 API 키를 입력하세요.

# GPT-3.5 Turbo 모델 설정 (창의성 설정)
llm = OpenAI(temperature=0.99, openai_api_key=OPENAI_API_KEY)

# 사용자 입력을 받기 위한 Streamlit UI 구성
st.title("과학 주제 설명 도우미")
st.write("초등학생도 이해할 수 있는 과학 설명을 제공해드립니다.")
topic = st.text_input("설명할 과학 주제를 입력하세요:")

# 프롬프트 템플릿 정의
template = """
당신은 초등학생도 쉽게 이해할 수 있는 복잡한 과학 주제를 설명해주는 전문가입니다.
아래 과학 주제를 초등학생이 이해할 수 있는 간단한 문장과 일상적인 예시를 사용하여 설명해 주세요.

과학 주제: {topic}
설명:
"""

# 설명 생성을 위한 함수
def generate_explanation(topic):
    # 프롬프트 생성
    prompt = PromptTemplate(template=template).format(topic=topic)
    
    # GPT 모델을 통해 설명 생성
    explanation = llm(prompt)
    return explanation

# 사용자가 주제를 입력했을 경우 설명 생성 및 출력
if topic:
    explanation = generate_explanation(topic)
    st.subheader("생성된 설명:")
    st.write(explanation)
