import pandas as pd
from transformers import pipeline
from tqdm import tqdm

# 모델 로드
sentiment_pipe = pipeline(
    "text-classification",
    model="hun3359/klue-bert-base-sentiment",
    device=-1
)

# 60가지 감정 → 긍정/중립/부정 매핑
POSITIVE_LABELS = {
    '기쁨', '감사하는', '신뢰하는', '편안한', '만족스러운',
    '흥분', '느긋', '안도', '신이 난', '자신하는'
}

NEGATIVE_LABELS = {
    # 분노
    '분노', '툴툴대는', '좌절한', '짜증내는', '방어적인',
    '악의적인', '안달하는', '구역질 나는', '노여워하는', '성가신',
    # 슬픔
    '슬픔', '실망한', '비통한', '후회되는', '우울한',
    '마비된', '염세적인', '눈물이 나는', '낙담한', '환멸을 느끼는',
    # 불안
    '불안', '두려운', '스트레스 받는', '취약한', '혼란스러운',
    '당혹스러운', '회의적인', '걱정스러운', '조심스러운', '초조한',
    # 상처
    '상처', '질투하는', '배신당한', '고립된', '충격 받은',
    '가난한 불우한', '희생된', '억울한', '괴로워하는', '버려진',
    # 당황
    '당황', '고립된(당황한)', '남의 시선을 의식하는', '외로운', '열등감',
    '죄책감의', '부끄러운', '혐오스러운', '한심한', '혼란스러운(당황한)'
}

def map_label(label, score):
    # 모델 확신도가 낮으면 중립으로 처리
    if score < 0.25:
        return "중립"
    
    if label in POSITIVE_LABELS:
        return "긍정"
    elif label in NEGATIVE_LABELS:
        return "부정"
    else:
        return "중립"

def analyze_sentiment(text):
    try:
        text = str(text).strip()[:200]
        if not text:
            return "중립", 0.0
        result = sentiment_pipe(text)[0]
        label = map_label(result["label"], result["score"])  # ← score도 넘김
        return label, round(result["score"], 4)
    except:
        return "중립", 0.0

df = pd.read_csv("./data/cleaned_comments.csv")

sentiments, scores = [], []

for comment in tqdm(df["comment"].fillna(""), desc="감성 분석 중"):
    label, score = analyze_sentiment(comment)
    sentiments.append(label)
    scores.append(score)

df["sentiment"] = sentiments
df["sentiment_score"] = scores

# 결과 저장
df.to_csv("./data/cleaned_comments_sentiment.csv", index=False, encoding="utf-8-sig")
print("✅ 저장 완료: data/cleaned_comments_sentiment.csv")
print(df.groupby("program")["sentiment"].value_counts())