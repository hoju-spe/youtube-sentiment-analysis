import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="유튜브 댓글 감성분석", layout="wide")
st.title("🎬 예능 프로그램 YouTube 댓글 감성분석 대시보드")

@st.cache_data
def load_data():
    df = pd.read_csv("./data/cleaned_comments_sentiment.csv", encoding="utf-8-sig")

    df.columns = df.columns.str.strip()

    df["program"] = (
        df["program"]
        .astype(str)
        .str.strip()
        .str.replace("\ufeff", "", regex=False)
        .str.replace("\u200b", "", regex=False)
    )

    df["sentiment"] = df["sentiment"].astype(str).str.strip()

    # 감성값 정리
    df["sentiment"] = df["sentiment"].replace({
        "0": None,
        "nan": None,
        "": None
    })

    # 정상 감성만 유지
    df = df[df["sentiment"].isin(["긍정", "중립", "부정"])]
    
    df["comment"] = df["comment"].astype(str)

    df["program"] = df["program"].replace({
        "놀면 뭐하니": "놀면뭐하니",
        "놀면 뭐하니?": "놀면뭐하니",
        "놀면뭐하니?": "놀면뭐하니",
        "놀뭐": "놀면뭐하니",
        "유 퀴즈": "유퀴즈",
        "유퀴즈온더블럭": "유퀴즈"
    })

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["likes"] = pd.to_numeric(df["likes"], errors="coerce").fillna(0).astype(int)
    df["sentiment_score"] = pd.to_numeric(df["sentiment_score"], errors="coerce").fillna(0)

    return df

df = load_data()

# =========================
# 파생변수 생성
# =========================

# 댓글 길이
df["comment_length"] = df["comment"].astype(str).str.len()

# 좋아요 구간
df["like_level"] = pd.cut(
    df["likes"],
    bins=[-1, 0, 10, 50, 100, 100000],
    labels=["0", "1~10", "11~50", "51~100", "100+"]
)

# 감성 점수 구간
df["score_level"] = pd.cut(
    df["sentiment_score"],
    bins=[0, 0.4, 0.7, 1.0],
    labels=["낮음", "보통", "높음"]
)

# 인기 댓글 여부
df["popular_comment"] = df["likes"] >= 50

# 댓글 길이 구간
df["length_level"] = pd.cut(
    df["comment_length"],
    bins=[0, 10, 30, 50, 1000],
    labels=["짧음", "보통", "김", "매우 김"]
)

# 사이드바
st.sidebar.header("필터")

if st.sidebar.button("캐시 초기화"):
    st.cache_data.clear()
    st.rerun()

program_options = sorted(df["program"].dropna().unique())
sentiment_order = ["긍정", "중립", "부정"]
sentiment_options = [s for s in sentiment_order if s in df["sentiment"].unique()]

programs = st.sidebar.multiselect(
    "프로그램 선택",
    options=program_options,
    default=program_options
)

sentiments = st.sidebar.multiselect(
    "감성 선택",
    options=sentiment_options,
    default=sentiment_options
)

keyword = st.sidebar.text_input("댓글 키워드 검색")

filtered = df[
    (df["program"].isin(programs)) &
    (df["sentiment"].isin(sentiments))
].copy()

if keyword:
    filtered = filtered[
        filtered["comment"].str.contains(keyword, case=False, na=False)
    ]

# 확인용
with st.expander("데이터 확인"):
    st.write("프로그램별 댓글 수")
    st.dataframe(df["program"].value_counts().reset_index())
    st.write("감성값")
    st.write(df["sentiment"].unique())

# KPI
st.subheader("📌 전체 요약")

col1, col2, col3, col4 = st.columns(4)

col1.metric("총 댓글 수", f"{len(filtered):,}")
col2.metric("분석 프로그램 수", filtered["program"].nunique())
col3.metric("분석 영상 수", filtered["video_id"].nunique())

positive_rate = (
    len(filtered[filtered["sentiment"] == "긍정"]) / len(filtered) * 100
    if len(filtered) > 0 else 0
)
col4.metric("긍정 댓글 비율", f"{positive_rate:.1f}%")

st.divider()

# 프로그램별 감성 비율
st.subheader("📊 프로그램별 긍정 / 부정 / 중립 감성 비율")

sentiment_ratio = (
    filtered.groupby(["program", "sentiment"])
    .size()
    .reset_index(name="count")
)

if not sentiment_ratio.empty:
    total_by_program = sentiment_ratio.groupby("program")["count"].transform("sum")
    sentiment_ratio["ratio"] = sentiment_ratio["count"] / total_by_program * 100

    fig1 = px.bar(
        sentiment_ratio,
        x="program",
        y="ratio",
        color="sentiment",
        text=sentiment_ratio["ratio"].round(1),
        barmode="stack",
        title="프로그램별 감성 비율",
        labels={"ratio": "비율(%)", "program": "프로그램", "sentiment": "감성"}
    )
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.warning("필터 조건에 맞는 데이터가 없습니다.")

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🥧 전체 감성 분포")

    sentiment_count = filtered["sentiment"].value_counts().reset_index()
    sentiment_count.columns = ["sentiment", "count"]

    if not sentiment_count.empty:
        fig2 = px.pie(
            sentiment_count,
            names="sentiment",
            values="count",
            hole=0.4,
            title="전체 댓글 감성 분포"
        )
        st.plotly_chart(fig2, use_container_width=True)


with col_right:
    st.subheader("🎥 영상별 긍정 비율 TOP 10")

    video_sentiment = (
        filtered.groupby(["video_title", "sentiment"])
        .size()
        .unstack(fill_value=0)
    )

    if not video_sentiment.empty and "긍정" in video_sentiment.columns:
        video_sentiment["total"] = video_sentiment.sum(axis=1)
        video_sentiment["positive_ratio"] = video_sentiment["긍정"] / video_sentiment["total"] * 100

        top_video = (
            video_sentiment.sort_values("positive_ratio", ascending=False)
            .head(10)
            .reset_index()
        )

        fig3 = px.bar(
            top_video,
            x="positive_ratio",
            y="video_title",
            orientation="h",
            title="영상별 긍정 댓글 비율 TOP 10",
            labels={"positive_ratio": "긍정 비율(%)", "video_title": "영상 제목"}
        )
        fig3.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("긍정 데이터가 없습니다.")

# =========================
# 댓글 길이 분석
# =========================

st.divider()

st.subheader("📝 프로그램별 댓글 길이 분포")

fig_length = px.box(
    filtered,
    x="program",
    y="comment_length",
    color="program",
    title="프로그램별 댓글 길이 분포"
)

st.plotly_chart(fig_length, use_container_width=True)

# =========================
# 좋아요 구간 분석
# =========================

st.subheader("🔥 좋아요 구간별 댓글 수")

like_count = (
    filtered["like_level"]
    .value_counts()
    .sort_index()
    .reset_index()
)

like_count.columns = ["좋아요 구간", "댓글 수"]

fig_like = px.bar(
    like_count,
    x="좋아요 구간",
    y="댓글 수",
    text="댓글 수",
    title="좋아요 구간별 댓글 분포"
)

st.plotly_chart(fig_like, use_container_width=True)

st.divider()

# 워드클라우드
st.subheader("☁️ 프로그램별 Word Cloud")

if len(filtered) > 0:
    selected_program = st.selectbox(
        "워드클라우드 프로그램 선택",
        options=sorted(filtered["program"].dropna().unique())
    )

    text_data = " ".join(
        filtered[filtered["program"] == selected_program]["comment"]
        .dropna()
        .astype(str)
    )

    if text_data.strip():
        wordcloud = WordCloud(
            font_path="C:/Windows/Fonts/malgun.ttf",
            width=1000,
            height=500,
            background_color="white"
        ).generate(text_data)

        fig_wc, ax = plt.subplots(figsize=(12, 6))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig_wc)
    else:
        st.info("워드클라우드를 만들 댓글이 없습니다.")
else:
    st.info("필터 조건에 맞는 댓글이 없습니다.")

st.divider()

st.subheader("👍 좋아요 많은 댓글 TOP 10")

top_comments = (
    filtered.sort_values("likes", ascending=False)
    [["program", "video_title", "comment", "sentiment", "sentiment_score", "likes"]]
    .head(10)
)

st.dataframe(top_comments, use_container_width=True)

st.divider()

st.subheader("🔍 댓글 데이터 탐색")

st.dataframe(
    filtered[[
        "program",
        "video_title",
        "author",
        "comment",
        "sentiment",
        "sentiment_score",
        "likes",
        "date"
    ]],
    use_container_width=True
)