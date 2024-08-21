import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# OpenAI API 키 설정 (하드코딩)
openai_api_key = ""

# GPT-3.5 터보 모델 설정
llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)

# 메모리 설정
memory = ConversationBufferMemory()

# ConversationChain 생성
conversation = ConversationChain(llm=llm, memory=memory)

# Streamlit 애플리케이션 UI 설정
st.title("Simple Chatbot")
st.write("Type a message and press Enter to chat with the bot.")

# 대화 기록을 저장할 리스트 초기화
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# ConversationChain을 세션 상태에 저장
if 'conversation' not in st.session_state:
    st.session_state.conversation = conversation

# 기존 대화 내역 표시
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 받기
if user_query := st.chat_input("You: "):
    
    # 사용자 질문을 대화 기록에 추가
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    
    with st.chat_message("user"):
        st.markdown(user_query)
    
    # 챗봇 응답 생성
    response = st.session_state.conversation.run(input=user_query)
    
    # 챗봇 응답을 대화 기록에 추가
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    with st.chat_message("assistant"):
        st.markdown(response)
