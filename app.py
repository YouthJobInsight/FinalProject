from pathlib import Path

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# =========================================================
# 1. 페이지 설정
# =========================================================
st.set_page_config(
    page_title="합격했는데, 왜 떠나는가?",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# 2. 공통 경로
# =========================================================
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "processed"


# =========================================================
# 3. 스타일 설정
# =========================================================
st.markdown(
    """
    <style>
        .main-title {
            font-size: 3.2rem;
            font-weight: 800;
            line-height: 1.25;
            margin-bottom: 0.3rem;
        }

        .orange-text {
            color: #f57c00;
        }

        .subtitle {
            font-size: 1.2rem;
            color: #555555;
            margin-bottom: 2rem;
        }

        .insight-box {
            background-color: #fff4e8;
            border-left: 6px solid #f57c00;
            padding: 18px 20px;
            border-radius: 8px;
            font-size: 1.08rem;
            font-weight: 600;
            margin-top: 15px;
            margin-bottom: 25px;
        }

        .question-box {
            background-color: #fafafa;
            padding: 22px;
            border-radius: 12px;
            border: 1px solid #eeeeee;
            margin-bottom: 12px;
        }

        .policy-card {
            background-color: #fff7ef;
            border: 1px solid #ffd7b0;
            padding: 22px;
            border-radius: 15px;
            min-height: 190px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 4. 데이터 불러오기 함수
# =========================================================
@st.cache_data
def load_csv(file_name: str) -> pd.DataFrame:
    file_path = DATA_DIR / file_name

    if not file_path.exists():
        st.error(f"데이터 파일을 찾을 수 없습니다: {file_path}")
        st.stop()

    return pd.read_csv(file_path)


# 필요할 때 아래 주석을 해제하세요.
# survival_df = load_csv("survival_data.csv")
# employment_df = load_csv("employment_status.csv")
# reason_df = load_csv("turnover_reasons.csv")
# logistic_df = load_csv("logistic_result.csv")
# reemployment_df = load_csv("reemployment_rate.csv")
# job_quality_df = load_csv("job_quality_change.csv")


# =========================================================
# 5. 사이드바
# =========================================================
with st.sidebar:
    st.title("목차")

    section = st.radio(
        "이동할 섹션",
        [
            "프로젝트 소개",
            "Q1. 얼마나, 언제, 누가 이탈하는가?",
            "Q2. 왜 이탈하는가?",
            "Q3. 떠난 뒤 더 나아졌는가?",
            "결론 및 정책 제언",
        ],
    )

    st.divider()

    st.caption(
        """
        한국노동패널조사, 경제활동인구조사 청년층 부가조사,
        근로환경조사 자료를 활용한 청년 첫 일자리 조기이탈 분석
        """
    )


# =========================================================
# 6. 표지
# =========================================================
st.markdown(
    """
    <div class="main-title">
        합격했는데, <span class="orange-text">왜 떠나는가?</span>
    </div>
    <div class="subtitle">
        청년 일자리 조기 이탈의 원인 분석 및 정책적 시사점 도출
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()


# =========================================================
# 7. 프로젝트 소개
# =========================================================
if section == "프로젝트 소개":

    st.header("청년 문제는 단순히 취업이 어려운 것일까?")

    st.write(
        """
        최근 청년층의 취업률과 임금 수준이 개선되고 있음에도,
        상당수 청년은 첫 직장을 비교적 짧은 기간 안에 떠나고 있습니다.

        따라서 본 프로젝트는 청년의 조기이탈을 개인의 단순한 선택으로 보기보다,
        첫 일자리의 고용 안정성, 근로여건, 경력개발 가능성 등
        구조적 요인과 함께 분석했습니다.
        """
    )

    st.subheader("문제제기 1. 취업 이후에도 지속되는 불안정성")

    # -----------------------------------------------------
    # [그래프 코드 삽입 위치 1]
    # 첫 직장 이탈률 또는 청년 첫 직장 유지율 추이 그래프 코드
    #
    # 예시:
    # fig, ax = plt.subplots(figsize=(9, 5))
    # ...
    # st.pyplot(fig)
    # -----------------------------------------------------

    st.info("여기에 첫 직장 이탈률 추이 그래프를 삽입하세요.")

    st.markdown(
        """
        <div class="insight-box">
        청년층은 첫 직장 진입에 성공한 이후에도 높은 이탈률을 보이며,
        취업 자체보다 안정적인 일자리 유지가 중요한 문제로 나타났다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("그래프 분석 코드 보기"):
        st.code(
            """
# 여기에 첫 직장 이탈률 그래프를 만든
# 데이터 전처리 및 시각화 코드를 붙여 넣으세요.
            """,
            language="python",
        )

    st.subheader("문제제기 2. 청년은 임금 때문에 이탈하는가?")

    # -----------------------------------------------------
    # [그래프 코드 삽입 위치 2]
    # 실질임금 추이 + 첫 직장 이탈률 추이
    # -----------------------------------------------------

    st.info("여기에 임금 수준과 첫 직장 이탈률을 비교한 그래프를 삽입하세요.")

    st.markdown(
        """
        <div class="insight-box">
        임금 수준이 개선되는 동안에도 첫 직장 이탈률은 높은 수준을 유지해,
        청년의 이탈을 임금만으로 설명하기 어렵다는 점을 보여준다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("그래프 분석 코드 보기"):
        st.code(
            """
# 여기에 실질임금과 첫 직장 이탈률을
# 비교한 분석 코드를 붙여 넣으세요.
            """,
            language="python",
        )

    st.subheader("연구 질문")

    st.markdown(
        """
        <div class="question-box">
            <b>Q1. 얼마나, 언제, 누가 이탈하는가?</b><br>
            이탈 규모와 시기, 고용형태별 차이를 분석합니다.
        </div>

        <div class="question-box">
            <b>Q2. 왜 이탈하는가?</b><br>
            청년이 응답한 퇴직 사유와 실제 이탈 의향 영향요인을 분석합니다.
        </div>

        <div class="question-box">
            <b>Q3. 조기이탈은 정말 실패인가?</b><br>
            이탈 이후 재취업 여부와 다음 일자리의 질을 분석합니다.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# 8. Q1
# =========================================================
elif section == "Q1. 얼마나, 언제, 누가 이탈하는가?":

    st.header("Q1. 얼마나, 언제, 누가 이탈하는가?")

    st.write(
        """
        한국노동패널조사 개인·직업력 자료를 결합해
        청년층의 첫 일자리 근속기간과 고용형태별 차이를 분석했습니다.
        """
    )

    st.subheader("1. 고용형태별 첫 직장 생존곡선")

    # -----------------------------------------------------
    # [그래프 코드 삽입 위치 3]
    # Kaplan-Meier 생존곡선
    # 정규직 / 비정규직 비교
    # -----------------------------------------------------

    st.info("여기에 Kaplan-Meier 생존곡선을 삽입하세요.")

    st.markdown(
        """
        <div class="insight-box">
        비정규직 청년은 입직 초기부터 정규직보다 빠르게 이탈하며,
        청년 조기이탈은 초기 고용불안정성과 밀접하게 연결되어 있다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Kaplan-Meier 분석 코드 보기"):
        st.code(
            """
# 이 위치에 lifelines의 KaplanMeierFitter를 사용한
# 생존분석 코드를 붙여 넣으세요.

# 예시 구조
# kmf_regular = KaplanMeierFitter()
# kmf_irregular = KaplanMeierFitter()
# ...
            """,
            language="python",
        )

    st.subheader("2. 연도별·집단별 조기이탈 특성")

    # -----------------------------------------------------
    # [그래프 코드 삽입 위치 4]
    # 교육수준 또는 고용형태별 히트맵
    # -----------------------------------------------------

    st.info("여기에 연도별·집단별 히트맵을 삽입하세요.")

    st.markdown(
        """
        <div class="insight-box">
        청년의 첫 일자리 안정성은 개인의 학력만으로 결정되기보다,
        고용형태와 직무 적합성에 따라 차이가 나타날 가능성이 크다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("히트맵 분석 코드 보기"):
        st.code(
            """
# 여기에 pivot_table 또는 groupby를 사용한
# 히트맵 전처리 및 시각화 코드를 붙여 넣으세요.
            """,
            language="python",
        )


# =========================================================
# 9. Q2
# =========================================================
elif section == "Q2. 왜 이탈하는가?":

    st.header("Q2. 왜 이탈하는가?")

    st.write(
        """
        먼저 청년이 직접 응답한 첫 일자리 퇴직 사유를 확인한 뒤,
        근로환경조사 데이터를 활용해 이탈 의향에 영향을 미치는 요인을 분석했습니다.
        """
    )

    st.subheader("1. 청년의 첫 일자리 퇴직 사유")

    # -----------------------------------------------------
    # [그래프 코드 삽입 위치 5]
    # 퇴직 사유 가로막대그래프
    # -----------------------------------------------------

    st.info("여기에 퇴직 사유 가로막대그래프를 삽입하세요.")

    st.markdown(
        """
        <div class="insight-box">
        청년이 직접 응답한 주된 퇴직 사유는 근로여건 불만족이며,
        임금뿐 아니라 직무환경과 성장 가능성이 중요한 이탈 요인으로 나타났다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("퇴직 사유 분석 코드 보기"):
        st.code(
            """
# 여기에 퇴직 사유 대분류 생성,
# 빈도 및 비율 계산,
# 가로막대그래프 코드를 붙여 넣으세요.
            """,
            language="python",
        )

    st.subheader("2. 최근 3년간 퇴직 사유 변화")

    # -----------------------------------------------------
    # [그래프 코드 삽입 위치 6]
    # 2023~2025년 퇴직 사유 100% 누적막대그래프
    # -----------------------------------------------------

    st.info("여기에 최근 3년간 퇴직 사유 누적막대그래프를 삽입하세요.")

    st.markdown(
        """
        <div class="insight-box">
        퇴직 사유의 구성은 최근 3년간 큰 변화 없이 유지되어,
        청년 조기이탈 문제가 일시적 현상보다 구조적 문제일 가능성을 보여준다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("연도별 퇴직 사유 분석 코드 보기"):
        st.code(
            """
# 여기에 연도별 퇴직 사유 비율 계산 및
# 100% 누적막대그래프 코드를 붙여 넣으세요.
            """,
            language="python",
        )

    st.subheader("3. 실제 이탈 의향에 영향을 미치는 요인")

    # -----------------------------------------------------
    # [그래프 코드 삽입 위치 7]
    # 로지스틱 회귀계수 또는 오즈비 그래프
    # -----------------------------------------------------

    st.info("여기에 로지스틱 회귀분석 결과 그래프를 삽입하세요.")

    st.markdown(
        """
        <div class="insight-box">
        청년의 이탈 의향에는 임금보다 경력개발 기회와
        보상의 공정성에 대한 인식이 더 중요한 영향을 미쳤다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("로지스틱 회귀분석 코드 보기"):
        st.code(
            """
# 여기에 종속변수·독립변수 생성,
# 로지스틱 회귀모형 적합,
# 계수 또는 오즈비 시각화 코드를 붙여 넣으세요.
            """,
            language="python",
        )


# =========================================================
# 10. Q3
# =========================================================
elif section == "Q3. 떠난 뒤 더 나아졌는가?":

    st.header("Q3. 떠난 뒤 더 나아졌는가?")

    st.write(
        """
        조기이탈을 무조건 실패로 규정하기보다,
        이탈 이후 재취업 여부와 다음 일자리의 질을 함께 살펴보았습니다.
        """
    )

    st.subheader("1. 첫 직장 이탈 후 12개월 이내 재취업률")

    # -----------------------------------------------------
    # [그래프 코드 삽입 위치 8]
    # 비조기이탈 / 조기이탈 집단 재취업률 비교
    # -----------------------------------------------------

    st.info("여기에 12개월 이내 재취업률 비교 그래프를 삽입하세요.")

    st.markdown(
        """
        <div class="insight-box">
        조기이탈 청년은 비교집단보다 12개월 내 재취업률이 높아,
        조기이탈이 반드시 장기 실업으로 이어지는 것은 아니었다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("재취업률 분석 코드 보기"):
        st.code(
            """
# 여기에 첫 직장 종료일,
# 다음 일자리 시작일,
# 12개월 이내 재취업 여부 계산 코드를 붙여 넣으세요.
            """,
            language="python",
        )

    st.subheader("2. 다음 일자리의 질은 개선되었는가?")

    # -----------------------------------------------------
    # [그래프 코드 삽입 위치 9]
    # 평균 임금 및 정규직/비정규직 비율 비교
    # -----------------------------------------------------

    st.info("여기에 다음 일자리 질 비교 그래프를 삽입하세요.")

    st.markdown(
        """
        <div class="insight-box">
        조기이탈 이후 재취업은 활발했지만 다음 일자리의 질이
        일관되게 개선되지는 않아, 일부 청년에게는 더 나은 일자리를
        탐색하기 위한 이동 과정으로 해석될 수 있다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("다음 일자리 질 분석 코드 보기"):
        st.code(
            """
# 여기에 첫 직장과 다음 일자리의
# 임금, 고용형태, 직무 특성을 비교한 코드를 붙여 넣으세요.
            """,
            language="python",
        )


# =========================================================
# 11. 결론 및 정책 제언
# =========================================================
elif section == "결론 및 정책 제언":

    st.header("결론 및 정책 제언")

    st.markdown(
        """
        <div class="insight-box">
        청년 조기이탈은 개인의 인내심 부족만으로 설명되는 현상이 아니라,
        첫 일자리의 고용 안정성, 성장 가능성, 보상 공정성 및
        노동시장 이동 구조가 함께 작용한 결과이다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="policy-card">
                <h3>① 입직 초기 적응 지원</h3>
                <p>
                온보딩, 직무교육, 멘토링 및 초기 경력상담을 통해
                청년이 첫 직장에 안정적으로 적응하도록 지원합니다.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="policy-card">
                <h3>② 임금 외 일자리 질 개선</h3>
                <p>
                직무 재설계, 공정한 보상 체계, 경력개발 경로 제시 등
                청년이 조직 안에서 성장할 수 있는 기반을 마련합니다.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    col3, col4 = st.columns(2)

    with col3:
        st.markdown(
            """
            <div class="policy-card">
                <h3>③ 이탈 이후 이동 지원</h3>
                <p>
                재취업 공백 최소화, 직무·경력 상담, 전직 지원과
                일자리 매칭을 강화합니다.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            """
            <div class="policy-card">
                <h3>④ 장기근속 중심 정책 재검토</h3>
                <p>
                장기근속 자체만을 목표로 하기보다,
                청년의 원활한 노동시장 이동과 경력 축적을 지원합니다.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("최종 메시지")

    st.success(
        """
        조기이탈 자체를 막는 데만 집중하기보다,
        청년이 자신에게 적합한 일자리로 이동하고 경력을 지속적으로
        축적할 수 있도록 지원하는 정책 전환이 필요합니다.
        """
    )


# =========================================================
# 12. 하단 정보
# =========================================================
st.divider()

st.caption(
    """
    데이터 출처: 한국노동패널조사, 경제활동인구조사 청년층 부가조사,
    산업안전보건연구원 근로환경조사
    """
)