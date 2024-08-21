import streamlit as st
import openai

# OpenAI API 키 설정 (여기에 실제 API 키를 입력하세요)
openai.api_key = ''

# Streamlit 애플리케이션의 제목
st.title('보도자료 생성기')

# 사용자가 입력할 필드 정의
st.subheader('보도자료 정보 입력')
topic = st.text_input('주제', placeholder='예: 새로운 제품 출시')
main_content = st.text_area('주요 내용', placeholder='예: 당사의 새로운 제품은 시장을 혁신할 것입니다...')
release_date = st.date_input('발표 날짜')
company_info = st.text_input('회사 정보', placeholder='예: 당사는 기술 혁신을 선도하는 기업입니다.')

# 버튼을 누르면 보도자료 생성
if st.button('보도자료 생성'):
    if not topic or not main_content or not release_date or not company_info:
        st.error('모든 필드를 입력해주세요.')
    else:
        # OpenAI GPT-3.5-turbo 모델을 사용해 보도자료 생성
        try:
            # 입력된 내용을 기반으로 GPT-3.5 모델에 전달할 프롬프트 구성
            prompt = (
                f"다음 정보를 바탕으로 설득력 있고 전문적인 보도자료를 작성해 주세요.\n\n"
                f"주제: {topic}\n"
                f"주요 내용: {main_content}\n"
                f"발표 날짜: {release_date}\n"
                f"회사 정보: {company_info}\n\n"
                f"보도자료:"
            )
            
            # GPT-3.5-turbo 모델에 요청 보내기
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional press release writer."},
                    {"role": "user", "content": prompt}
                ]
            )

            # 보도자료 생성 결과 추출
            press_release = response['choices'][0]['message']['content']

            # 보도자료 출력
            st.subheader('생성된 보도자료')
            st.write(press_release)
        
        except Exception as e:
            # 오류가 발생한 경우 오류 메시지 출력
            st.error(f'보도자료 생성 중 오류가 발생했습니다: {str(e)}')

