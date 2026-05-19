# 🎬 한국 대표 예능 3사 댓글 감성분석 비교 대시보드
> YouTube Comment Sentiment Analysis Dashboard
> 유퀴즈 on the Block vs 런닝맨 vs 놀면뭐하니

---

## 📌 프로젝트 개요
한국 대표 예능 프로그램 3개의 YouTube 댓글 데이터를 수집하여
프로그램별 시청자 반응과 감성을 비교 분석하고 대시보드로 시각화합니다.

---

## 🎯 분석 목표
- 3개 예능 프로그램 YouTube 댓글 데이터 수집 및 비교
- 프로그램별 긍정 / 부정 / 중립 감성 비율 분석
- 프로그램별 주요 키워드 및 Word Cloud 시각화
- Hugging Face 한국어 모델을 활용한 댓글 감성 분류
- Streamlit 대시보드로 결과 시각화

---

## 🛠️ 기술 스택
| 분류 | 기술 |
|------|------|
| 데이터 수집 | YouTube Data API v3 |
| 전처리 | Pandas, 한국어 텍스트 정제 |
| 텍스트 분석 | Word Cloud, 키워드 빈도 분석 |
| 감성 분석 | Hugging Face 한국어 모델 |
| 시각화 | Matplotlib, Seaborn |
| 대시보드 | Streamlit |
| 협업 | GitHub, Notion |

---

## 👥 팀 구성
| 이름 | 역할 | 담당 업무 |
|------|------|-----------|
| 호주 | 데이터 수집 | YouTube API 크롤링 |
| 박지은 | 데이터 전처리 | 한국어 텍스트 정제, 토큰화 |
| 박채연 | 감성 분석 | Hugging Face 모델 적용 |
| 이석현 | 시각화/대시보드 | Word Cloud, Streamlit 제작 |
| 수광 | EDA + PPT | 탐색적 분석, PPT 제작 |
| 유동건 | PPT + 발표 | PPT 디자인, 최종 발표 |

---

## 📅 진행 일정
| 기간 | 내용 |
|------|------|
| 5/18 ~ 5/23 | 데이터 수집 & 전처리 |
| 5/24 ~ 5/28 | EDA 분석, Word Cloud |
| 5/29 ~ 6/01 | 감성 분석 모델링 |
| 6/02 ~ 6/05 | 대시보드 제작 & 코드 통합 |
| 6/06 ~ 6/07 | PPT 제작, 최종 리허설 |
| 6/08 | 최종 발표 |

---

## ⚙️ 설치 방법
```bash
# 레포 클론
git clone https://github.com/hoju-spe/youtube-sentiment-analysis.git
cd youtube-sentiment-analysis

# 라이브러리 설치
pip install google-api-python-client python-dotenv pandas

# .env 파일 생성 후 API 키 입력
YOUTUBE_API_KEY=여기에_API키_입력
```

---

## ⚠️ 주의사항
- `.env` 파일은 절대 GitHub에 올리지 마세요!
- YouTube API 하루 할당량: 10,000 유닛
