import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# OpenAI API 키 설정
OPENAI_API_KEY = ''  # 여기에 실제 OpenAI API 키를 입력하세요.

# 스트림릿 화면 설정
st.title('재미있는 과학 🧪✨')
st.write('복잡한 과학 주제를 초등학생도 이해할 수 있게 설명해 드립니다. 🧑‍🔬👩‍🔬')

# 사용자 입력을 받는 텍스트 입력 상자
user_input = st.text_input('설명할 과학 주제를 입력하세요:', '')

# 시스템 메시지 설정
system_message = SystemMessage(content="""
당신은 과학을 재미있게 설명해주는 과학 커뮤니케이터입니다. 당신의 임무는 복잡한 주제를 초등학생도 이해할 수 있도록 쉽게 설명하는 것입니다. 
간단한 언어를 사용하고, 관련 있는 예시를 들며, 설명을 간결하고 흥미롭게 유지하세요.
""")

# OpenAI Chat 모델 설정
chat = ChatOpenAI(
    temperature=0,
    model_name='gpt-3.5-turbo',
    openai_api_key=OPENAI_API_KEY
)

def get_explanation(topic):
    try:
        # 메시지 생성
        messages = [
            system_message,
            HumanMessage(content=f"초등학생도 이해할 수 있게 {topic}에 대해 설명해 주세요. 간단한 언어와 예시를 사용하세요.")
        ]
        # 응답 생성
        response = chat(messages)
        # 응답 반환
        return response.content
    except Exception as e:
        return f"Error: {e}"

if st.button('설명 보기'):
    explanation = get_explanation(user_input)
    if explanation.startswith("Error:"):
        st.error(explanation)
    else:
        st.write('### 설명 📚')
        st.write(explanation)
