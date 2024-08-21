import streamlit as st
import openai

# OpenAI API 키 설정
openai.api_key = ''

def generate_press_release(topic, content, date, company_info):
    # 보다 구체적인 프롬프트를 사용하여 설득력 있는 홍보 문구 생성
    prompt = f"""
    다음 정보에 기반하여 설득력 있고 전문적인 보도자료를 작성하십시오. :
    주제: {topic}
    주요 내용: {content}
    발표 날짜: {date}
    회사 정보: {company_info}

    혜택을 강조하고, 잠재 고객의 우려를 해결하며, 강력한 행동 유도 문구를 포함하십시오.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Specify the correct GPT-4 model designed for chat
            messages=[
                {"role": "system", "content": "전문적인 보도자료를 생성하십시오."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )
        return response['choices'][0]['message']['content']
    except openai.error.OpenAIError as e:
        st.error(f"An error occurred: {e}")
        return None

def main():
    st.title('보도자료 생성기')

    with st.form("press_release_form"):
        st.subheader("보도자료 작성 양식")
        topic = st.text_input("주제")
        content = st.text_area("주요 내용", height=150)
        release_date = st.date_input("발표 날짜")
        company_info = st.text_input("회사 정보")
        submit_button = st.form_submit_button("보도자료 생성")

        if submit_button and topic and content and company_info:
            generated_press_release = generate_press_release(topic, content, release_date, company_info)
            if generated_press_release:
                st.success("보도자료가 성공적으로 생성되었습니다!")
                st.subheader("보도자료")
                st.write(generated_press_release)

if __name__ == "__main__":
    main()
