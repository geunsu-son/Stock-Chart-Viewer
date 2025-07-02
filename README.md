# Index and ETF Trend Viewer


이 프로젝트는 나스닥, S&P 500 지수 및 ETF의 20일, 60일, 120일, 200일 이동평균선 그래프와 RSI(Relative Strength Index) 지표를 시각화하고, 이동평균선과의 가격 비교 알림을 제공하는 Streamlit 기반 웹앱입니다.


## 주요 기능
- 나스닥, S&P 500, QLD 등 주요 지수 및 ETF의 일별 가격 데이터 시각화
- 20일, 60일, 120일, 200일 이동평균선 표시
- RSI(Relative Strength Index) 지표 및 그래프 제공
- 최근 거래가격이 이동평균선과 근접하거나 하회할 경우 사이드바에 알림 표시
- 기간(1~36개월) 슬라이더로 원하는 기간만큼 데이터 필터링
- 최근 3일간의 가격 및 이동평균선과의 차이, % 변동 정보 제공
- Altair 기반 캔들스틱 차트, 이동평균선, RSI 시각화

## 사용 방법
1. 필요한 패키지 설치
   ```bash
   pip install -r requirements.txt
   ```
2. 앱 실행
   ```bash
   streamlit run streamlit_app.py
   ```
3. 웹 브라우저에서 안내에 따라 지수/ETF 차트와 알림을 확인


## 주요 라이브러리
- streamlit
- pandas
- yfinance
- altair

## RSI(Relative Strength Index) 소개 및 계산 방법
RSI(상대강도지수)는 주가의 상승과 하락의 강도를 비교하여 과매수(overbought) 또는 과매도(oversold) 상태를 판단하는 데 사용되는 기술적 지표입니다. 일반적으로 0~100 사이의 값을 가지며, 70 이상이면 과매수, 30 이하이면 과매도로 해석합니다.

**RSI 계산 방법(14일 기준):**
1. 각 거래일의 종가 변동분(전일 대비 상승분: Gain, 하락분: Loss)을 계산합니다.
2. 14일 동안의 평균 상승분(Average Gain)과 평균 하락분(Average Loss)을 구합니다.
3. RS(Relative Strength) = Average Gain / Average Loss
4. RSI = 100 - (100 / (1 + RS))

본 프로젝트에서는 RSI를 차트와 함께 시각화하여, 투자자가 과매수/과매도 구간을 쉽게 파악할 수 있도록 하였습니다.

## 참고
- E-mail: gnsu0705@gmail.com
- Blog: [Super-Son](https://super-son.tistory.com/)

---

본 프로젝트는 개인적인 투자 참고용으로 제작되었습니다. 투자 판단의 최종 책임은 본인에게 있습니다.
