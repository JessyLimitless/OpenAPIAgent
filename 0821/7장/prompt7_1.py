import streamlit as st
import openai

# OpenAI API Key 설정 (코드에 직접 설정)
openai.api_key = ''

# 지원 언어 목록
languages = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Korean": "ko",
    "Japanese": "ja",
    "Chinese (Simplified)": "zh",
}

# 번역 함수
def translate_text(input_text, target_language):
    try:
        # GPT-3.5-turbo 모델을 사용한 번역 요청
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Translate the following text to {target_language}."},
                {"role": "user", "content": input_text}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {e}"

# 세션 상태 초기화
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# UI 구성
st.title("Multilingual Translation App")
st.write("GPT-3.5-turbo를 사용한 다국어 번역 애플리케이션입니다.")

# 텍스트 입력 필드
input_text = st.text_area("번역할 텍스트를 입력하세요", height=150)

# 언어 선택 라디오 버튼
target_language = st.radio("번역할 언어를 선택하세요", list(languages.keys()))

# 번역 버튼 클릭 시 동작
if st.button("번역하기"):
    if input_text.strip():
        # 번역 실행
        translated_text = translate_text(input_text, target_language)
        
        # 대화 기록에 저장
        st.session_state.chat_history.append({"input": input_text, "translation": translated_text})
        
        # 번역 결과 표시
        st.write("## 번역 결과")
        st.markdown(f"<h2 style='color: blue;'>{translated_text}</h2>", unsafe_allow_html=True)
    else:
        st.warning("번역할 텍스트를 입력해주세요.")

# 대화 기록 초기화 버튼
if st.button("대화 기록 초기화"):
    st.session_state.chat_history = []
    st.success("대화 기록이 초기화되었습니다.")

# 대화 기록 표시
if st.session_state.chat_history:
    st.write("## 대화 기록")
    for i, entry in enumerate(st.session_state.chat_history, 1):
        st.write(f"### {i}. 입력된 텍스트")
        st.write(entry["input"])
        st.write("### 번역된 텍스트")
        st.markdown(f"<p style='font-size:18px;'>{entry['translation']}</p>", unsafe_allow_html=True)

# Streamlit 앱 실행 안내
st.write("**참고**: 번역 결과는 GPT 모델에 의해 생성되며, 100% 정확하지 않을 수 있습니다.")
