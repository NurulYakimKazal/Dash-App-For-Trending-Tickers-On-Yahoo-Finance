# Dash-App-For-Trending-Tickers-On-Yahoo-Finance

This project is about building a dashboard, utilizing the python library of Dash by Plotly for watching the trending tickers on Yahoo Finance (Data source: https://finance.yahoo.com/).
Not only is this dasboard able to show historical data of the stock prices, but it is also capable of displaying its real-time data (updated minute-by-minute or every 60 seconds). 
As expected, these stock prices data are exhibited by the candlestick chart, while its volume is given by the bar chart. 

In addition, it also shows few key performance indicators of the shown ticker, like:
1. The current price and its relative change (with respect to the one on previous interval)
2. The current price vs 52-week range
3. The market capitalization

Since the trending tickers on Yahoo Finance are dynamic, the users can always refresh the ticker list provided in the dropdown by clicking the update-ticker button.

For its technical details, the dashboard is built by taking advantage of some Python libraries, including:
1. dash
2. dash-bootstrap-components
3. plotly
4. requests
5. bs4 (BeautifulSoup)
6. yfinance
7. yahoofinancials

The dash and dash-bootstrap-components are used to build the layout and functionality of the dashboard, while plotly is used for creating the graphs displayed on it. 
Moreover, the requests and bs4 (BeautifulSoup) are utilized for scraping the list of trending tickers on Yahoo Finance. 
Lastly, yfinance and yahoofinancials are the libraries used for getting the stock price and fundamental data from the aforementioned website.
