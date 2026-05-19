import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

st.title("전처리 이전 워드클라우드 테스트")

files = {
    "유퀴즈": "./data/yuquiz.csv",
    "런닝맨": "./data/runningman.csv",
    "놀면뭐하니": "./data/nolmyun.csv"
}

program = st.selectbox("프로그램 선택", list(files.keys()))

df = pd.read_csv(files[program])

text = " ".join(df["comment"].dropna().astype(str))

wc = WordCloud(
    font_path="C:/Windows/Fonts/malgun.ttf",
    width=1000,
    height=500,
    background_color="white"
).generate(text)

fig, ax = plt.subplots(figsize=(12, 6))
ax.imshow(wc)
ax.axis("off")

st.pyplot(fig)