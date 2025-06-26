import streamlit as st
import pandas as pd
import yfinance as yf
import altair as alt

st.set_page_config(
    page_title="Index and ETF Trend Viewer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

with st.sidebar:
    st.write(
        """
    ### 연락처
    📞 Tel. 010-4430-2279  
    📩 E-mail. [gnsu0705@gmail.com](gnsu0705@gmail.com)  
    💻 Blog. [Super-Son](https://super-son.tistory.com/)  
    😎 Resume. [Super-Son](https://super-son-resume.streamlit.app)
    """
    )
    st.divider()
    # Slider for selecting time period in months
    months = st.slider("Select Time Period (months)", 1, 36, 24)

st.title("Index and ETF Trend Viewer")
st.write(
    """
나스닥, S&P 500 지수의 20일 이동평균 선 그래프를 제공하는 사이트를 찾지 못해 제가 사용하기 위해 직접 제작했습니다.  
보고 싶은 지수나 상품에 대한 그래프를 그리도록 제작했으며, 20일, 60일, 120일 이동평균 선을 기준으로 거래가격이 맞춰지면 사이드바에 알림이 표시됩니다.
"""
)
st.divider()

# Calculate the date for 1 year and 6 months ago from today
end_date = pd.Timestamp.today()
start_date = end_date - pd.DateOffset(months=14)


st.sidebar.error(
    f"""
**Last Updated Day**  
{str(end_date)[:10]}
"""
)

# Fetch data
def fetch_data(ticker):
    with st.spinner(f"Please wait...Loading Data"):
        # Retrieve stock data
        stock = yf.Ticker(ticker)
        history = stock.history(period="3y", interval="1d")
        data = pd.DataFrame(history)
        data.reset_index(inplace=True)
        data["Date"] = data["Date"].dt.strftime(
            "%Y-%m-%d"
        )  # Convert date to string format
        return data


# Function to create moving average
def add_moving_averages(data):
    data["MA_20"] = data["Close"].rolling(window=20).mean()
    data["MA_60"] = data["Close"].rolling(window=60).mean()
    data["MA_120"] = data["Close"].rolling(window=120).mean()
    data["MA_200"] = data["Close"].rolling(window=200).mean()
    return data


# Sidebar with last day 'Low' price comparison
def check_low_vs_moving_averages(data, name):
    last_row = data.iloc[-1]
    low_price = last_row["Low"]
    ma20 = last_row["MA_20"]
    ma60 = last_row["MA_60"]
    ma120 = last_row["MA_120"]
    ma200 = last_row["MA_200"]

    if low_price < ma120:
        st.sidebar.info(
            f"""
**{name}**  
##### 120일 이동평균보다 낮은 가격에 거래한 기록이 있어요!
"""
        )
    elif low_price < ma60:
        st.sidebar.info(
            f"""
**{name}**  
##### 60일 이동평균보다 낮은 가격에 거래한 기록이 있어요!
"""
        )
    elif low_price < ma20:
        st.sidebar.info(
            f"""
**{name}**  
##### 20일 이동평균보다 낮은 가격에 거래한 기록이 있어요!
"""
        )
    elif low_price * 0.99 < ma20:
        st.sidebar.info(
            f"""
**{name}**  
##### 가격이 1% 낮아지면 20일 이동평균보다 가격이 낮아져요!
"""
        )

# Function to filter data based on the selected period
def filter_data(data, months):
    start_filter_date = end_date - pd.DateOffset(months=months)
    filtered_data = data[data["Date"] >= start_filter_date.strftime("%Y-%m-%d")]
    return filtered_data


# Function to View Last 5 Days Dataframe and create candlestick chart with moving averages
def create_candlestick_chart(data):
    last_ma20 = data.iloc[-1]["MA_20"]
    last_ma60 = data.iloc[-1]["MA_60"]
    last_ma120 = data.iloc[-1]["MA_120"]
    last_ma200 = data.iloc[-1]["MA_200"]

    # =============== 최근 주가 그리기 ===============
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"Last Close = %.2f" % data.iloc[-1]["Close"])

    view_data = data[["Date", "Low", "High", "Close"]][-3:]

    view_data["Close_Diff"] = data["Close"] - last_ma20
    view_data["Close_Diff%"] = view_data["Close_Diff"] / data["Close"] * 100
    view_data["Close_Diff%"] = view_data["Close_Diff%"].apply(
        lambda x: str("%.2f" % (x)) + "%" if x > 1 else str("%.2f" % (x)) + "% 💡" if x > 0 else str("%.2f" % (x)) + "% 🔥"
    )

    view_data["Close_Diff_60"] = data["Close"] - last_ma60
    view_data["Close_Diff_120"] = data["Close"] - last_ma120
    view_data["Close_Diff_200"] = data["Close"] - last_ma200

    if len(view_data[view_data["Close_Diff_120"] < 0]) > 0:
        with col2:
            st.info(f"MA_120 = %.2f" % last_ma120)
        with col3:
            st.error(
                "120일선 터치 : {}".format(
                    view_data[view_data["Close_Diff_120"] < 0].reset_index().iloc[-1, 1]
                )
            )
    elif len(view_data[view_data["Close_Diff_60"] < 0]) > 0:
        with col2:
            st.info(f"MA_60 = %.2f" % last_ma60)
        with col3:
            st.error(
                "60일선 터치 : {}".format(
                    view_data[view_data["Close_Diff_60"] < 0].reset_index().iloc[-1, 1]
                )
            )
    elif len(view_data[view_data["Close_Diff"] < 0]) > 0:
        with col2:
            st.info(f"MA_20 = %.2f" % last_ma20)
        with col3:
            st.error(
                "20일선 터치 : {}".format(
                    view_data[view_data["Close_Diff"] < 0].reset_index().iloc[-1, 1]
                )
            )
    else:
        with col2:
            st.info(f"MA_20 = %.2f" % last_ma20)

    st.dataframe(
        view_data[
            [
                "Date",
                "Low",
                "High",
                "Close",
                "Close_Diff",
                "Close_Diff%",
            ]
        ],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Close": st.column_config.NumberColumn("Close Price", format="%.2f")
        },
    )

    # =============== 일봉차트 그리기 ===============
    base = alt.Chart(data).encode(
        alt.X("Date:N", title="Date")  # Date column is now in string format
    )

    open_close_color = alt.condition(
        "datum.Open <= datum.Close",
        alt.value("#FF0000"),  # Red for increasing
        alt.value("#0000FF"),  # Blue for decreasing
    )

    rule = base.mark_rule().encode(
        alt.Y("Low:Q", scale=alt.Scale(zero=False)),
        alt.Y2("High:Q"),
        color=open_close_color,
    )

    bar = base.mark_bar().encode(
        alt.Y("Open:Q"), alt.Y2("Close:Q"), color=open_close_color
    )

    ma20 = base.mark_line(color="orange").encode(alt.Y("MA_20:Q"))
    ma60 = base.mark_line(color="green").encode(alt.Y("MA_60:Q"))
    ma120 = base.mark_line(color="brown").encode(alt.Y("MA_120:Q"))
    ma200 = base.mark_line(color="gray").encode(alt.Y("MA_200:Q"))

    chart = (rule + bar + ma20 + ma60 + ma120 + ma200).properties(
        width=800,
        height=400,
    )

    return chart


nasdaq_data = fetch_data("^IXIC")
sp500_data = fetch_data("^GSPC")


company_code = ["QLD"]

# Create a list to hold the filtered stock data
filtered_data = []

for code in company_code:
    stock_data = fetch_data(code)
    stock_data = add_moving_averages(stock_data)
    check_low_vs_moving_averages(stock_data, code)
    stock_data_filtered = filter_data(stock_data, months)
    filtered_data.append((code.replace('^IXIC','NASDAQ').replace('^GSPC','S&P 500'), stock_data_filtered))

for i in range(len(filtered_data)):
    st.subheader(filtered_data[i][0] + " Chart")
    chart = create_candlestick_chart(filtered_data[i][1])
    st.altair_chart(chart, use_container_width=True)

# # Create and display charts in pairs
# for i in range(0, len(filtered_data), 2):
#     col1, col2 = st.columns(2, gap="large")
    
#     with col1:
#         st.subheader(filtered_data[i][0] + " Chart")
#         chart = create_candlestick_chart(filtered_data[i][1])
#         st.altair_chart(chart, use_container_width=True)

#     if i + 1 < len(filtered_data):  # Check if there is a second column
#         with col2:
#             st.subheader(filtered_data[i + 1][0] + " Chart")
#             chart = create_candlestick_chart(filtered_data[i + 1][1])
#             st.altair_chart(chart, use_container_width=True)

st.divider()