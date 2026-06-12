from pathlib import Path
import sqlite3

import streamlit as st
import pandas as pd


# =========================================================
# 1. 페이지 설정
# =========================================================
st.set_page_config(
    page_title="합격했는데, 왜 떠나는가?",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# 2. DB 경로
# =========================================================
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "YouthJobInsight.db"


# =========================================================
# 3. DB 존재 여부 확인
# =========================================================
if not DB_PATH.exists():
    st.error("YouthJobInsight.db 파일을 찾을 수 없습니다.")
    st.warning(
        "app.py와 YouthJobInsight.db가 "
        "같은 폴더에 있는지 확인해 주세요."
    )
    st.stop()


# =========================================================
# 4. SQL 실행 함수
# =========================================================
@st.cache_data
def run_query(query: str) -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(query, conn)


# =========================================================
# 5. 제목
# =========================================================
st.title("합격했는데, 왜 떠나는가?")
with st.sidebar:
    st.header("목차")

    section = st.radio(
        "분석 내용",
        [
            "프로젝트 소개",
            "문제제기",
            "Q1. 얼마나, 언제, 누가 이탈하는가?",
            "Q2. 왜 이탈하는가?",
            "Q3. 떠난 뒤 더 나아졌는가?",
            "결론 및 정책 제언",
        ],
    )

    st.divider()

    st.caption(
        """
        데이터 출처

        - 한국노동패널조사
        - 경제활동인구조사 청년층 부가조사
        - 근로환경조사
        """
    )
st.subheader("청년 첫 일자리 조기이탈의 원인과 이후 이동 분석")

st.write(
    """
    청년의 첫 일자리 이탈 규모와 원인을 살펴보고,
    이탈 이후 더 나은 일자리로 이동했는지를 분석합니다.
    """
)

st.success("데이터베이스 연결이 완료되었습니다.")