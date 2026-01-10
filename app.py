import streamlit as st
from google import genai
import PIL.Image

# 1. 화면 설정
st.set_page_config(page_title="현장 사진 분석기", layout="wide") # 가로 표를 보기 좋게 'wide'로 변경
st.title("🏗️ 콘크리트 시험결과 엑셀 변환기")

# 2. 본인의 API 키를 입력하세요
API_KEY = "AIzaSyDZ6AIfQso53Gul5WhC2GC4JpNxfUd2HOE" # 실제 사용 시 보안에 주의하세요
client = genai.Client(api_key=API_KEY)

# 3. 데이터 추출을 위한 상세 지시어 (프롬프트) 설정
SYSTEM_PROMPT = """
당신은 건설 현장 데이터 정리 전문가입니다. 
이미지에서 추출한 정보를 반드시 '엑셀에 바로 붙여넣기 좋은 가로 한 줄의 마크다운 표' 형식으로 출력하세요.

반드시 아래 컬럼 순서를 지켜주세요:
구조물명 | 타설일자 | 타설부위 | 설계량 | 타설량 | 규격 | 납품회사 | 타설방법 | 시작시간 | 종료시간 | 슬럼프(mm) | 공기량(%) | 염화물 | 온도(°C) | 단위수량

[주의사항]
1. 세로 목록 형식이 아닌, 반드시 가로로 긴 표(Flat Table) 한 행으로 작성하세요.
2. 사진에 정보가 없는 항목(예: 시작시간, 설계량 등)은 공란으로 비워두거나 '-'로 표시하세요.
3. 숫자는 단위 없이 숫자만 추출하여 정확히 기입하세요.
"""

# 4. 사진 업로드
uploaded_file = st.file_uploader("분석할 보드판 사진을 선택하세요", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    image = PIL.Image.open(uploaded_file)
    st.image(image, caption='업로드 완료', width=500)
    
    if st.button("AI 분석 및 엑셀 양식 생성"):
        with st.spinner('AI가 엑셀 데이터를 생성 중입니다...'):
            try:
                # 모델 설정 및 분석 요청
                # 모델명은 사용 가능한 최신 모델(예: gemini-2.0-flash)을 권장하나, 
                # 기존에 사용하시던 코드를 유지합니다.
                response = client.models.generate_content(
                    model='gemini-3-flash-preview', # 혹은 'gemini-1.5-flash'
                    contents=[
                        SYSTEM_PROMPT,
                        image
                    ]
                )
                
                st.success("분석 완료!")
                st.subheader("📌 엑셀 붙여넣기용 데이터")
                st.markdown(response.text)
                
                st.info("💡 위 표를 드래그해서 복사(Ctrl+C)한 뒤 엑셀에 붙여넣기(Ctrl+V) 하세요.")
                
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")