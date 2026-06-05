# AI Inbound Marketing Priority Recommender

## 프로젝트 개요
국가별 방한 외국인 데이터와 SNS 관심도 데이터를 결합하여
마케팅 우선순위(High/Medium/Low)를 추천하는 AI 의사결정 지원 시스템

## 데이터 출처
- 한국관광데이터랩 (https://datalab.visitkorea.or.kr)
- 분석 대상 국가: 중국, 일본, 대만, 미국, 홍콩 (2015~2026년 누적 방문객 Top 5)
- 분석 기간: 2018.11 ~ 2026.04

## 실행 방법
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 파일 구조
- app.py: Streamlit 웹앱
- feature_engineering.py: 데이터 전처리 및 Feature Engineering
- train_model.py: 모델 학습
- model/: 학습된 모델 파일
- full_dataset.csv: 전체 데이터셋
- model_dataset.csv: 모델 학습용 데이터셋
