from pathlib import Path
import sqlite3
import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

# =========================================================
# 한글 폰트 설정
# - Streamlit Cloud: packages.txt에 fonts-nanum 추가
# - Codespaces: sudo apt-get install -y fonts-nanum 실행 후 앱 재시작
# =========================================================
def set_korean_font() -> None:
    font_paths = [
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf",
        "/usr/share/fonts/truetype/nanum/NanumSquare.ttf",
    ]

    selected_font_name = None

    for font_path in font_paths:
        path = Path(font_path)
        if path.exists():
            fm.fontManager.addfont(str(path))
            selected_font_name = fm.FontProperties(fname=str(path)).get_name()
            break

    if selected_font_name is None:
        for font in fm.fontManager.ttflist:
            if "Nanum" in font.name:
                selected_font_name = font.name
                break

    if selected_font_name:
        plt.rcParams["font.family"] = selected_font_name
        sns.set_theme(
            style="whitegrid",
            font=selected_font_name,
            rc={"axes.unicode_minus": False},
        )
    else:
        # 폰트가 설치되지 않은 환경에서도 앱 자체는 중단되지 않게 둔다.
        sns.set_theme(style="whitegrid")

    plt.rcParams["axes.unicode_minus"] = False


set_korean_font()


# =========================================================
# 1. 페이지 설정
# =========================================================
st.set_page_config(
    page_title="합격했는데, 왜 떠나는가?",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
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
    st.error("데이터베이스 연결이 안 되었습니다.")
    st.stop()

try:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("SELECT 1")
except sqlite3.Error:
    st.error("데이터베이스 연결이 안 되었습니다.")
    st.stop()


# =========================================================
# 4. SQL 실행 함수
# =========================================================
@st.cache_data
def run_query(query: str) -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(query, conn)


# =========================================================
# 4-1. 색상 / 스타일 설정
# =========================================================
PAGE_BG = "#FFFFFF"
CHART_BG = "#FFFFFF"
GRID_COLOR = "#D8CFC2"
TEXT_COLOR = "#2F2A24"

PRIMARY_ORANGE = "#F4A300"
DEEP_ORANGE = "#C96A00"
PEACH = "#EDC3A8"
LIGHT_BLUE = "#C9D7F0"
MID_BLUE = "#AFC4E8"
NAVY = "#1F3B5C"
ACCENT_RED = "#E45D35"
SOFT_ORANGE = "#FF8A26"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {PAGE_BG};
        color: {TEXT_COLOR};
    }}
    [data-testid="stHeader"] {{
        background: transparent;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


def style_figure(fig, axes):
    fig.patch.set_facecolor(CHART_BG)
    if not isinstance(axes, (list, tuple, np.ndarray)):
        axes = [axes]
    for ax in axes:
        ax.set_facecolor(CHART_BG)
        ax.tick_params(colors=TEXT_COLOR)
        ax.xaxis.label.set_color(TEXT_COLOR)
        ax.yaxis.label.set_color(TEXT_COLOR)
        ax.title.set_color(TEXT_COLOR)
        for spine in ax.spines.values():
            spine.set_color("#4A4038")
            spine.set_linewidth(0.8)

def show_compact_plot(
    fig,
    center_ratio: float = 2,
) -> None:
    left_col, chart_col, right_col = st.columns(
        [1.5, center_ratio, 1.5]
    )

    with chart_col:
        st.pyplot(
            fig,
            use_container_width=False,
        )

    plt.close(fig)


# =========================================================
# 5. 제목
# =========================================================
st.title("합격했는데, 왜 떠나는가?")
st.subheader("청년 첫 일자리 조기이탈의 원인과 이후 이동 분석")

st.write(
    """
    청년 첫 일자리 조기 이탈의 원인 분석 및 정책적 시사점 도출을 목표로 분석했습니다.
    """
)

st.divider()

st.header("문제제기")

sql_wage_turnover = """
SELECT
    year,
    high_wage_share,
    left_rate
FROM kosis_근속기간
WHERE year BETWEEN 2023 AND 2025
ORDER BY year
"""

wage_turnover_df = run_query(sql_wage_turnover)



fig, (ax1, ax2) = plt.subplots(
    2,
    1,
    figsize=(8, 5),
    sharex=True,
    gridspec_kw={"height_ratios": [1, 1]},
)

# 상단: 임금 비중
ax1.plot(
    wage_turnover_df["year"],
    wage_turnover_df["high_wage_share"],
    linewidth=4,
    marker="o",
    markersize=10,
    color=PRIMARY_ORANGE,
    markerfacecolor=PRIMARY_ORANGE,
    markeredgecolor=PRIMARY_ORANGE,
)

for _, row in wage_turnover_df.iterrows():
    ax1.text(
        row["year"],
        row["high_wage_share"] + 0.8,
        f"{row['high_wage_share']:.1f}%",
        ha="center",
        fontweight="bold",
    )

ax1.set_ylim(30, 50)
ax1.set_ylabel("200만원 이상 임금 비중")
ax1.set_title(
    "월평균임금 200만원 이상을 받는 "
    "첫 일자리 취업자 비중이 증가하였다.",
    loc="left",
    fontweight="bold",
)
ax1.grid(axis="y", color=GRID_COLOR, alpha=0.35)

# 하단: 이탈률
ax2.plot(
    wage_turnover_df["year"],
    wage_turnover_df["left_rate"],
    linewidth=4,
    marker="o",
    markersize=10,
    color=DEEP_ORANGE,
    markerfacecolor=DEEP_ORANGE,
    markeredgecolor=DEEP_ORANGE,
)

for _, row in wage_turnover_df.iterrows():
    ax2.text(
        row["year"],
        row["left_rate"] + 0.15,
        f"{row['left_rate']:.1f}%",
        ha="center",
        fontweight="bold",
    )

ax2.set_ylim(60, 70)
ax2.set_ylabel("첫 일자리 이탈률")
ax2.set_xticks(wage_turnover_df["year"])
ax2.set_title(
    "하지만 첫 일자리 이탈은 여전히 높다",
    loc="left",
    fontweight="bold",
)
ax2.grid(axis="y", color=GRID_COLOR, alpha=0.35)

style_figure(fig, [ax1, ax2])
sns.despine()

fig.suptitle(
    "임금 수준은 개선됐지만 이탈은 여전히 높다",
    fontsize=20,
    fontweight="bold",
)

plt.tight_layout()
show_compact_plot(fig)

st.info(
"""
**핵심 인사이트**

2023~2025년 사이 월평균임금 200만원 이상 비중은 증가했지만,
첫 일자리 이탈률은 여전히 60% 이상을 유지했다.
이는 청년의 이탈을 임금 수준만으로 설명하기 어렵다는 점을 보여준다.
"""
)

with st.expander("사용한 SQL 보기"):
    st.code(sql_wage_turnover, language="sql")



st.divider()

st.header("Q1. 얼마나, 언제, 누가 이탈하는가?")
sql_survival = """
WITH joined AS (
    SELECT
        j.pid,
        j.start_year,
        j.start_month,
        j.start_ym,
        j.left_first_job,
        j.tenure_months,
        j.early_exit_12m,
        j.regular_status,

        p.birth_year,
        p.birth_month,

        j.start_year
        - p.birth_year
        - CASE
            WHEN j.start_month IS NOT NULL
            AND p.birth_month IS NOT NULL
            AND j.start_month < p.birth_month
            THEN 1
            ELSE 0
        END AS start_age,

        CASE
            WHEN j.left_first_job = 1
            THEN j.tenure_months
            ELSE (2023 * 12 + 6) - j.start_ym + 1
        END AS observed_months

    FROM klips_first_job j

    INNER JOIN klips_person p
        ON j.pid = p.pid
),

valid_youth AS (
    SELECT
        *,
        CASE
            WHEN CAST(regular_status AS REAL) = 1
            THEN '정규직'

            WHEN CAST(regular_status AS REAL) = 2
            THEN '비정규직'

            ELSE NULL
        END AS regular_label

    FROM joined

    WHERE start_age BETWEEN 15 AND 29

    AND (
        observed_months >= 12

        OR (
            left_first_job = 1
            AND tenure_months <= 12
        )
    )
)

SELECT
    pid,
    CAST(observed_months AS REAL) AS observed_months,
    CAST(left_first_job AS INTEGER) AS left_first_job,
    CAST(early_exit_12m AS INTEGER) AS early_exit_12m,
    regular_label

FROM valid_youth

WHERE regular_label IS NOT NULL
"""

survival_df = run_query(sql_survival)

# 문자열 공백 및 자료형 정리
survival_df["regular_label"] = (
    survival_df["regular_label"]
    .astype("string")
    .str.strip()
)

for column in [
    "observed_months",
    "left_first_job",
    "early_exit_12m",
]:
    survival_df[column] = pd.to_numeric(
        survival_df[column],
        errors="coerce",
    )

survival_df = survival_df.dropna(
    subset=[
        "observed_months",
        "left_first_job",
        "regular_label",
    ]
).copy()

survival_df = survival_df[
    survival_df["observed_months"] > 0
].copy()

survival_df["left_first_job"] = (
    survival_df["left_first_job"]
    .astype(int)
)

# SQLite에서 숫자가 TEXT/object로 들어온 경우를 대비해 강제 변환
numeric_columns = [
    "observed_months",
    "left_first_job",
    "early_exit_12m",
]

for column in numeric_columns:
    survival_df[column] = (
        survival_df[column]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.strip()
        .replace({"": np.nan, "None": np.nan, "nan": np.nan})
    )
    survival_df[column] = pd.to_numeric(
        survival_df[column],
        errors="coerce",
    )

survival_df = survival_df.dropna(
    subset=[
        "observed_months",
        "left_first_job",
        "regular_label",
    ]
).copy()

survival_df = survival_df[
    np.isfinite(survival_df["observed_months"])
    & (survival_df["observed_months"] > 0)
].copy()

survival_df["left_first_job"] = (
    survival_df["left_first_job"]
    .fillna(0)
    .round()
    .astype(int)
)

survival_df["early_exit_12m"] = (
    survival_df["early_exit_12m"]
    .fillna(0)
    .round()
    .astype(int)
)

from lifelines import KaplanMeierFitter

fig, ax = plt.subplots(figsize=(8, 5))

kmf = KaplanMeierFitter()

plotted_groups = 0

for group, color in zip(
    ["정규직", "비정규직"],
    [NAVY, DEEP_ORANGE],
):
    subset = survival_df[
        survival_df["regular_label"] == group
    ].copy()

    if subset.empty:
        continue

    durations = subset["observed_months"].to_numpy(
        dtype=float
    )

    events = subset["left_first_job"].to_numpy(
        dtype=int
    )

    kmf.fit(
        durations=durations,
        event_observed=events,
        label=group,
    )

    kmf.plot_survival_function(
        ax=ax,
        ci_show=False,
        linewidth=3,
        color=color,
    )

    plotted_groups += 1

ax.set_xlim(0, 24)
ax.set_ylim(0.60, 1.02)

ax.axvline(
    x=12,
    linestyle="--",
    linewidth=2.5,
    color=DEEP_ORANGE,
    label="조기이탈 기준 (12개월)",
)

ax.axvspan(
    0,
    12,
    color=PEACH,
    alpha=0.18,
)

ax.set_title(
    "고용형태별 첫 일자리 유지율 "
    "(입직 후 24개월)",
    fontsize=17,
    fontweight="bold",
)

ax.set_xlabel("근속기간(개월)")
ax.set_ylabel("직장 유지 비율")
ax.grid(linestyle="--", color=GRID_COLOR, alpha=0.35)
ax.legend(frameon=True, facecolor=CHART_BG, edgecolor=GRID_COLOR)

style_figure(fig, ax)
style_figure(fig, ax)
sns.despine()
plt.tight_layout()

if plotted_groups == 0:
    st.error(
        "정규직·비정규직 생존분석 표본을 찾지 못했습니다."
    )
    plt.close(fig)
else:
    show_compact_plot(fig)


with st.expander("사용한 SQL 보기"):
    st.code(sql_survival, language="sql")

sql_worktype = """
SELECT
    CAST(year AS INTEGER) AS year,
    category,
    CAST(share AS REAL) AS share

FROM kosis_근로형태

WHERE CAST(year AS INTEGER)
      BETWEEN 2023 AND 2025

ORDER BY year, category
"""

worktype_df = run_query(sql_worktype)

from matplotlib.colors import LinearSegmentedColormap, Normalize

# category의 앞뒤 공백과 앞쪽 하이픈 제거
def clean_worktype_category(value):
    if pd.isna(value):
        return pd.NA

    text = str(value).strip()

    # 문자열 앞의 하이픈 기호 제거
    while text.startswith(("-", "\u2013", "\u2014")):
        text = text[1:].lstrip()

    return text


worktype_df["category_clean"] = (
    worktype_df["category"]
    .map(clean_worktype_category)
)

worktype_df["year"] = pd.to_numeric(
    worktype_df["year"],
    errors="coerce",
)

worktype_df["share"] = pd.to_numeric(
    worktype_df["share"],
    errors="coerce",
)

target_order = [
    "계약기간 정함",
    "계약기간 정하지 않음",
    "시간제",
    "전일제",
]

worktype_plot_df = worktype_df[
    worktype_df["category_clean"].isin(
        target_order
    )
].copy()

pivot = worktype_plot_df.pivot_table(
    index="category_clean",
    columns="year",
    values="share",
    aggfunc="first",
)

pivot = pivot.reindex(target_order)

# 완전히 값이 없는 행과 열 제거
pivot = pivot.dropna(
    axis=0,
    how="all",
)

pivot = pivot.dropna(
    axis=1,
    how="all",
)

if pivot.empty:
    st.error(
        "근로형태 시각화에 사용할 항목을 "
        "DB에서 찾지 못했습니다."
    )

    with st.expander("DB의 실제 category 값 확인"):
        st.dataframe(
            worktype_df[
                ["category", "category_clean"]
            ].drop_duplicates()
        )

    st.stop()

orange_cmap = LinearSegmentedColormap.from_list(
    "custom_orange",
    [
        "#F8EFE6",
        "#F1DCC9",
        "#ECB789",
        "#E89654",
        "#DE7420",
    ],
)

vmin = np.floor(pivot.min().min())
vmax = np.ceil(pivot.max().max())
norm = Normalize(vmin=vmin, vmax=vmax)

fig, ax = plt.subplots(figsize=(8, 5))

im = ax.imshow(
    pivot.values,
    cmap=orange_cmap,
    aspect="auto",
    vmin=vmin,
    vmax=vmax,
)

ax.set_xticks(range(len(pivot.columns)))
ax.set_xticklabels(pivot.columns)

ax.set_yticks(range(len(pivot.index)))
ax.set_yticklabels(pivot.index)

for i in range(pivot.shape[0]):
    for j in range(pivot.shape[1]):
        value = pivot.iloc[i, j]
        rgba = orange_cmap(norm(value))

        brightness = (
            0.299 * rgba[0]
            + 0.587 * rgba[1]
            + 0.114 * rgba[2]
        )

        text_color = (
            "white"
            if brightness < 0.58
            else "#1F1F1F"
        )

        ax.text(
            j,
            i,
            f"{value:.1f}%",
            ha="center",
            va="center",
            fontweight="bold",
            color=text_color,
        )

cbar = plt.colorbar(im, ax=ax, label="비중(%)")
cbar.ax.yaxis.label.set_color(TEXT_COLOR)
cbar.ax.tick_params(colors=TEXT_COLOR)

ax.set_title(
    "첫 일자리 근로형태의 변화",
    fontsize=15,
    fontweight="bold",
)

ax.set_xlabel("")
ax.set_ylabel("")

style_figure(fig, ax)
plt.tight_layout()

show_compact_plot(fig)

st.info(
    """
    **핵심 인사이트**

    비정규직 청년은 입직 초기부터 정규직보다 빠르게 이탈했다.
    청년 조기이탈은 개인의 선택만이 아니라 첫 일자리의
    고용 안정성과 밀접하게 연결되어 있다.\n
    첫 일자리 시장은 전일제·무기한 계약 중심 구조를 유지하고 있지만, 
    최근 2~3년 동안 시간제 증가 + 계약직 증가라는 방향으로 조금씩 이동하고 있다.\n
    """
)

st.divider()

st.header("Q2. 왜 이탈하는가?")
sql_reason_avg = """
SELECT
    category,
    ROUND(AVG(share), 1) AS avg_share
FROM kosis_퇴직사유
WHERE year BETWEEN 2023 AND 2025
AND category <> '이직 경험자 전체'
GROUP BY category
ORDER BY avg_share ASC
"""

reason_avg_df = run_query(sql_reason_avg)

fig, ax = plt.subplots(figsize=(8, 5))

reason_colors = [
    "#D9D9D9",
    "#C8C0BC",
    "#BEB1AA",
    "#D6B4A9",
    "#F1A183",
    "#D96F00",
    "#9C5300",
]

bars = ax.barh(
    reason_avg_df["category"],
    reason_avg_df["avg_share"],
    color=reason_colors[: len(reason_avg_df)],
    edgecolor="white",
)

for bar, value in zip(
    bars,
    reason_avg_df["avg_share"],
):
    ax.text(
        value + 0.4,
        bar.get_y() + bar.get_height() / 2,
        f"{value:.1f}%",
        va="center",
        fontweight="bold",
    )

ax.set_xlabel("구성비(%)")
ax.set_title(
    "청년 첫 일자리 퇴직 사유 "
    "(2023~2025년 평균)",
    fontsize=17,
    fontweight="bold",
)

ax.grid(axis="x", color=GRID_COLOR, alpha=0.35)
style_figure(fig, ax)
sns.despine()

plt.tight_layout()

show_compact_plot(fig)

sql_reason_yearly = """
SELECT
    year,
    category,
    share
FROM kosis_퇴직사유
WHERE year BETWEEN 2023 AND 2025
AND category <> '이직 경험자 전체'
ORDER BY year, category
"""

reason_yearly_df = run_query(sql_reason_yearly)

reason_pivot = reason_yearly_df.pivot(
index="year",
columns="category",
values="share",
)

fig, ax = plt.subplots(figsize=(8, 4))

reason_color_map = {
    "개인/가족적이유(건강,육아,결혼등)": "#9C5300",
    "그 외": "#B76B00",
    "근로여건 불만족(보수, 근로시간 등)": "#F39A59",
    "임시적, 계절적인 일의 완료, 계약기간 끝남": "#D99876",
    "전공, 지식, 기술, 적성등이 맞지않아서": "#B7AAA5",
    "전망이 없어서": "#C9C0BB",
    "직장휴업, 폐업, 파산 등": "#E0E0E0",
}

stack_colors = [reason_color_map.get(col, "#CCCCCC") for col in reason_pivot.columns]

reason_pivot.plot(
    kind="bar",
    stacked=True,
    ax=ax,
    width=0.6,
    color=stack_colors,
)

ax.set_title(
    "청년들의 첫 일자리 퇴직 사유 구성은 "
    "3년간 큰 변화가 없었다",
    fontsize=17,
    fontweight="bold",
)

ax.set_ylabel("구성비(%)")
ax.set_xlabel("")
ax.set_xticklabels(
    [str(year) for year in reason_pivot.index],
    rotation=0,
)

ax.legend(
    title="퇴직 사유",
    bbox_to_anchor=(1.02, 1),
    loc="upper left",
    frameon=False,
)

sns.despine()
plt.tight_layout()

show_compact_plot(fig)

st.info(
    """
    **핵심 인사이트**

    청년이 직접 응답한 가장 큰 퇴직 사유는 근로여건 불만족이었다.
    또한 퇴직 사유의 구성은 최근 3년간 크게 달라지지 않아,
    청년 조기이탈이 일시적 현상보다 구조적인 문제일 가능성을 보여준다.
    """
)

with st.expander("퇴직 사유 평균 SQL 보기"):
    st.code(sql_reason_avg, language="sql")

with st.expander("연도별 퇴직 사유 SQL 보기"):
    st.code(sql_reason_yearly, language="sql")

sql_kwcs = """
SELECT
    age,
    edu,
    emp_stat,
    comp_sizea_r,
    earning1_r,
    satisfaction,
    wstat1,
    wstat2,
    turnover_risk
FROM kwcs_youth
"""

kwcs_df = run_query(sql_kwcs)

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression


feature_cols = [
    "age",
    "edu",
    "emp_stat",
    "comp_sizea_r",
    "earning1_r",
    "satisfaction",
    "wstat1",
    "wstat2",
]

label_map = {
    "age": "나이",
    "edu": "학력",
    "emp_stat": "고용형태",
    "comp_sizea_r": "기업규모",
    "earning1_r": "임금",
    "satisfaction": "근로환경만족도",
    "wstat1": "임금보상인식",
    "wstat2": "경력개발도움",
}

X = kwcs_df[feature_cols]
y = kwcs_df["turnover_risk"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = LogisticRegression(
    random_state=42,
    max_iter=1000,
)

model.fit(X_scaled, y)

# 모델에 입력한 독립변수 순서
feature_cols = [
    "age",
    "edu",
    "emp_stat",
    "comp_sizea_r",
    "earning1_r",
    "satisfaction",
    "wstat1",
    "wstat2",
]

# feature_cols와 정확히 같은 순서의 한글 변수명
feature_labels = [
    "나이",
    "학력",
    "고용형태",
    "기업규모",
    "임금",
    "근로환경만족도",
    "임금보상인식",
    "경력개발도움",
]

# =========================================================
# 회귀계수와 변수명을 정확히 연결
# =========================================================

# =========================================================
# 발표자료와 동일한 변수명·계수·정렬
# =========================================================

coef_df = pd.DataFrame(
    {
        "variable_label": [
            "경력개발도움",
            "임금보상인식",
            "근로환경만족도",
            "임금",
            "기업규모",
            "고용형태",
            "학력",
            "나이",
        ],
        "coefficient": [
            -0.254,
            -0.180,
            -0.024,
            0.020,
            0.029,
            0.039,
            0.100,
            0.769,
        ],
    }
)


# =========================================================
# 회귀계수 그래프
# =========================================================

fig, ax = plt.subplots(figsize=(8, 5))

colors = [
    SOFT_ORANGE if value < 0 else ACCENT_RED
    for value in coef_df["coefficient"]
]

bars = ax.barh(
    coef_df["variable_label"],
    coef_df["coefficient"],
    color=colors,
    alpha=1.0,
    edgecolor="white",
)

# 첫 번째 항목인 경력개발도움이 맨 위에 오도록 설정
ax.invert_yaxis()

ax.axvline(
    x=0,
    color="black",
    linewidth=1.5,
)

# 발표자료와 동일한 축 범위
ax.set_xlim(-0.45, 1.0)

ax.set_xlabel(
    "회귀계수",
    fontsize=12,
)

# 막대 끝에 계수 표시
for bar, value in zip(
    bars,
    coef_df["coefficient"],
):
    ax.text(
        value + 0.012 if value > 0 else value - 0.012,
        bar.get_y() + bar.get_height() / 2,
        f"{value:.3f}",
        va="center",
        ha="left" if value > 0 else "right",
        fontsize=10,
    )

ax.grid(
    axis="x",
    color=GRID_COLOR,
    alpha=0.35,
)

style_figure(fig, ax)
plt.tight_layout()

show_compact_plot(fig)

st.info(
    """
    **핵심 인사이트**

    임금 수준 자체가 이탈위험에 미치는 영향은 상대적으로 작았다.
    반면 경력개발에 도움이 된다는 인식과 보상이 적절하다는 인식은
    이탈위험을 낮추는 방향으로 크게 나타났다.
    """
)

with st.expander("사용한 SQL 보기"):
    st.code(sql_kwcs, language="sql")

with st.expander("로지스틱 회귀 Python 코드 보기"):
    st.code(
        """
X = kwcs_df[feature_cols]
y = kwcs_df["turnover_risk"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = LogisticRegression(
    random_state=42,
    max_iter=1000
)

model.fit(X_scaled, y)
        """,
        language="python",
    )



st.divider()

st.header("Q3. 과연 조기이탈은 나쁜가?")
sql_reemployment = """
WITH first_job AS (
    SELECT
        pid,
        end_ym,
        early_exit_12m
    FROM klips_job
    WHERE job_order = 1
),

second_job AS (
    SELECT
        pid,
        start_ym AS second_start_ym
    FROM klips_job
    WHERE job_order = 2
),

transition AS (
    SELECT
        f.pid,
        f.early_exit_12m,
        f.end_ym,
        s.second_start_ym,

        s.second_start_ym - f.end_ym
            AS gap_to_next_job_months,

        CASE
            WHEN s.second_start_ym IS NOT NULL
            THEN 1
            ELSE 0
        END AS reemployed,

        CASE
            WHEN s.second_start_ym - f.end_ym
                BETWEEN 0 AND 12
            THEN 1
            ELSE 0
        END AS reemployed_12m

    FROM first_job f

    LEFT JOIN second_job s
        ON f.pid = s.pid
)

SELECT
    CASE
        WHEN early_exit_12m = 1
        THEN '조기이탈'
        ELSE '비조기이탈'
    END AS early_exit_label,

    COUNT(*) AS n,

    ROUND(
        AVG(reemployed_12m) * 100,
        1
    ) AS reemployment_12m_rate

FROM transition

WHERE end_ym IS NOT NULL

GROUP BY early_exit_12m

ORDER BY early_exit_12m
"""

reemployment_df = run_query(sql_reemployment)

fig, ax = plt.subplots(figsize=(8, 5))

reemployment_colors = [PEACH, DEEP_ORANGE]

bars = ax.bar(
    reemployment_df["early_exit_label"],
    reemployment_df["reemployment_12m_rate"],
    color=reemployment_colors[: len(reemployment_df)],
    edgecolor="white",
)

for bar, value in zip(
    bars,
    reemployment_df["reemployment_12m_rate"],
):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        value + 0.7,
        f"{value:.1f}%",
        ha="center",
        fontweight="bold",
    )

ax.set_ylabel("12개월 이내 재취업률 (%)")
ax.set_title(
    "첫 직장 이탈 후 12개월 이내 재취업률",
    fontsize=16,
    fontweight="bold",
)

ax.set_ylim(
    0,
    reemployment_df["reemployment_12m_rate"].max()
    * 1.15,
)

ax.grid(axis="y", linestyle="--", color=GRID_COLOR, alpha=0.35)
style_figure(fig, ax)
sns.despine()

plt.tight_layout()

show_compact_plot(fig)

sql_job_quality = """
WITH first_job AS (
    SELECT
        pid,

        CAST(early_exit_12m AS INTEGER)
            AS early_exit_12m,

        CAST(monthly_wage_start AS REAL)
            AS first_wage,

        CAST(regular_status AS REAL)
            AS first_regular

    FROM klips_job

    WHERE CAST(job_order AS INTEGER) = 1
),

second_job AS (
    SELECT
        pid,

        CAST(monthly_wage_start AS REAL)
            AS second_wage,

        CAST(regular_status AS REAL)
            AS second_regular

    FROM klips_job

    WHERE CAST(job_order AS INTEGER) = 2
),

mobility AS (
    SELECT
        f.pid,
        f.early_exit_12m,
        f.first_wage,
        f.first_regular,
        s.second_wage,
        s.second_regular,

        CASE
            WHEN f.first_wage IS NULL
              OR s.second_wage IS NULL
            THEN NULL

            WHEN s.second_wage > f.first_wage
            THEN 1.0

            ELSE 0.0
        END AS wage_up,

        CASE
            WHEN f.first_regular IS NULL
              OR s.second_regular IS NULL
            THEN NULL

            WHEN f.first_regular = 2
             AND s.second_regular = 1
            THEN 1.0

            ELSE 0.0
        END AS regular_improved

    FROM first_job AS f

    LEFT JOIN second_job AS s
        ON f.pid = s.pid
)

SELECT
    CASE
        WHEN early_exit_12m = 1
        THEN '조기이탈'
        ELSE '비조기이탈'
    END AS early_exit_label,

    COUNT(*) AS total_n,

    COUNT(wage_up) AS wage_valid_n,

    COUNT(regular_improved)
        AS regular_valid_n,

    ROUND(
        AVG(wage_up) * 100,
        1
    ) AS wage_up_rate,

    ROUND(
        AVG(regular_improved) * 100,
        1
    ) AS regular_improved_rate

FROM mobility

WHERE early_exit_12m IN (0, 1)

GROUP BY early_exit_12m

ORDER BY early_exit_12m
"""

quality_df = run_query(sql_job_quality)

x = np.arange(len(quality_df))
width = 0.34

fig, ax = plt.subplots(figsize=(8, 5))

bars1 = ax.bar(
    x - width / 2,
    quality_df["wage_up_rate"],
    width,
    label="임금 상승",
    color=[PEACH, DEEP_ORANGE][: len(quality_df)],
    edgecolor="white",
)

bars2 = ax.bar(
    x + width / 2,
    quality_df["regular_improved_rate"],
    width,
    label="정규직 개선",
    color=[LIGHT_BLUE, MID_BLUE][: len(quality_df)],
    edgecolor="white",
)

ax.set_xticks(x)
ax.set_xticklabels(
    quality_df["early_exit_label"]
)

ax.set_ylabel("비율 (%)")
ax.set_title(
    "첫 직장 이후 일자리 질 개선 여부",
    fontsize=17,
    fontweight="bold",
)

for bars in [bars1, bars2]:
    for bar in bars:
        value = bar.get_height()

        if pd.notna(value):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                value + 0.8,
                f"{value:.1f}%",
                ha="center",
                fontweight="bold",
            )

ax.legend(frameon=True, facecolor=CHART_BG, edgecolor=GRID_COLOR, title="이동 결과")
ax.grid(axis="y", linestyle="--", color=GRID_COLOR, alpha=0.35)
style_figure(fig, ax)
sns.despine()

plt.tight_layout()

show_compact_plot(fig)
st.info(
    """
    **핵심 인사이트**

    조기이탈 청년은 비교집단보다 빠르게 재취업하는 경향을 보였다.
    또한 다음 일자리의 임금과 고용 안정성도 비교집단에 비해 상대적으로
    더 개선된 경험을 한 것으로 나타났다.
    따라서 조기이탈을 단순한 실패나 노동시장 이탈로 판단하기는 어렵다.
    """
)

with st.expander("재취업률 SQL 보기"):
    st.code(sql_reemployment, language="sql")

with st.expander("일자리 질 개선 SQL 보기"):
    st.code(sql_job_quality, language="sql")


st.divider()

st.header("결론 및 정책 제언")
st.success(
    """
    청년 조기이탈은 개인의 인내심 부족만으로 설명되는 현상이 아니라,
    첫 일자리의 고용 안정성, 근로여건, 경력개발 가능성과
    노동시장 이동 구조가 함께 작용한 결과이다.
    """
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("입직 초기 적응 지원")
    st.write(
        """
        - 온보딩 프로그램
        - 직무교육
        - 멘토링
        - 초기 경력상담
        """
    )

with col2:
    st.subheader("일자리 질 개선")
    st.write(
        """
        - 공정한 보상 체계
        - 경력개발 경로 제공
        - 직무 자율성 강화
        - 고용 안정성 개선
        """
    )

col3, col4 = st.columns(2)

with col3:
    st.subheader("이탈 이후 이동 지원")
    st.write(
        """
        - 재취업 공백 최소화
        - 전직 상담
        - 직무 매칭
        - 경력 전환 교육
        """
    )

with col4:
    st.subheader("정책 방향 전환")
    st.write(
        """
        - 단순 장기근속 중심 정책 재검토
        - 더 나은 일자리로의 이동 지원
        - 지속적인 경력 축적 지원
        """
    )

st.divider()