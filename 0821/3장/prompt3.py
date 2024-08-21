import openai
import streamlit as st
from langchain import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# 1. OpenAI 호출 설정 (v1/chat/completions 엔드포인트)
# OpenAI API 키를 하드코딩하여 설정합니다 (실제 배포 시 환경변수를 사용하는 것이 더 안전합니다)
OPENAI_API_KEY = ""  # OpenAI API 키를 여기에 넣으세요
TEMPERATURE = 0.99  # 모델의 창의성 설정

# OpenAI 모델을 직접 호출하는 함수
def openai_chat(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt}],
        temperature=TEMPERATURE,
    )
    return response['choices'][0]['message']['content']

# OpenAI 라이브러리 초기화
openai.api_key = OPENAI_API_KEY

# 2. ConversationChain 생성 및 메모리 설정
memory = ConversationBufferMemory()
conversation_chain = ConversationChain(llm=OpenAI(openai_api_key=OPENAI_API_KEY, temperature=TEMPERATURE), memory=memory)

# 4. Streamlit UI 구성
st.title("GPT-3.5 Chatbot")
st.write("GPT-3.5-turbo 모델과 대화를 나눠보세요. 아래 입력란에 질문을 입력하세요.")

# 5. 대화 기록 관리 및 표시 (세션 상태 사용)
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# 6. 사용자 입력 처리
user_input = st.text_input("당신의 질문을 입력하세요:")

if user_input:
    # GPT-3.5-turbo 모델에 사용자 입력을 보내고 응답을 받음
    bot_response = openai_chat(user_input)

    # 대화 기록에 사용자 입력과 봇의 응답 추가
    st.session_state['chat_history'].append({"role": "user", "content": user_input})
    st.session_state['chat_history'].append({"role": "assistant", "content": bot_response})

# 대화 기록을 화면에 표시 (st.chat_message 사용)
for message in st.session_state['chat_history']:
    with st.chat_message(message["role"]):
        st.write(message["content"])
