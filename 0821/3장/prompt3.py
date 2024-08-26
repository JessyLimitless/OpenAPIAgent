import streamlit as st
from langchain import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import openai

# OpenAI API 설정
openai.api_key = ""  # 하드코딩된 API 키
MODEL_NAME = "gpt-3.5-turbo"
TEMPERATURE = 0.99

# OpenAI 모델 호출 함수
def get_openai_response(prompt, conversation_history):
    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=conversation_history + [{"role": "user", "content": prompt}],
        temperature=TEMPERATURE,
    )
    return response['choices'][0]['message']['content']

# LangChain ConversationChain 설정
memory = ConversationBufferMemory()
conversation_chain = ConversationChain(llm=OpenAI(model=MODEL_NAME, temperature=TEMPERATURE), memory=memory)

# Streamlit UI 구성
st.title("GPT-3.5-turbo 챗봇 애플리케이션")
st.write("질문을 입력해 보세요. 챗봇이 응답합니다.")

# 대화 기록 관리
if "messages" not in st.session_state:
    st.session_state.messages = []  # 대화 기록 초기화

# 사용자 입력 처리
user_input = st.text_input("질문을 입력해 주세요:")

if user_input:
    # 사용자의 질문을 대화 기록에 추가
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 챗봇 응답 생성
    response = get_openai_response(user_input, st.session_state.messages)
    
    # 챗봇의 응답을 대화 기록에 추가
    st.session_state.messages.append({"role": "assistant", "content": response})

# 대화 기록을 st.chat_message로 출력
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").write(msg["content"])
