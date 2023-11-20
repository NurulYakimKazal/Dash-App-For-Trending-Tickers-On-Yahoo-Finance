# Required Libraries

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, html, dcc
from dash.exceptions import PreventUpdate
import yfinance as yf
from yahoofinancials import YahooFinancials
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from bs4 import BeautifulSoup

# Side Content

current_header = dbc.CardHeader(
    'Current Price',
    className='border-bottom border-light d-flex align-items-center justify-content-center',
    style={'height': '15%', 'textAlign': 'left', 'fontSize': '13px', 'fontWeight': 500, 'color': 'white'}
)

min_max_header = dbc.CardHeader(
    'Current Price Vs 52 Week Range',
    className='border-bottom border-light d-flex align-items-center justify-content-center',
    style={'height': '15%', 'textAlign': 'left', 'fontSize': '13px', 'fontWeight': 500, 'color': 'white'}
)

market_cap_header = dbc.CardHeader(
    'Market Capitalization',
    className='border-bottom border-light d-flex align-items-center justify-content-center',
    style={'height': '15%', 'textAlign': 'left', 'fontSize': '13px', 'fontWeight': 500, 'color': 'white'}
)

current_body = dbc.CardBody([
    dcc.Graph(
        id='current',
        className='d-flex align-items-center justify-content-center',
        style={'height': '100%', 'width': '100%'}
    )
], className='bg-opacity-10 m-0 pt-1 pb-1 d-flex align-items-center justify-content-center', style={'height': '85%'})

min_max_body = dbc.CardBody([
    dcc.Graph(
        id='min-max',
        className='d-flex align-items-center justify-content-center',
        style={'height': '100%', 'width': '100%'}
    )
], className='bg-opacity-10 m-0 pt-1 pb-1 d-flex align-items-center justify-content-center', style={'height': '85%'})

market_cap_body = dbc.CardBody([
    dcc.Graph(
        id='market',
        className='d-flex align-items-center justify-content-center',
        style={'height': '100%', 'width': '100%'}
    )
], className='bg-opacity-10 m-0 pt-1 pb-1 d-flex align-items-center justify-content-center', style={'height': '85%'})

# Main Content

candlestick_body = dbc.CardBody([
    dcc.Graph(
        id='candlestick-body',
        className='d-flex align-items-center justify-content-center',
        style={'height': '100%', 'width': '100%'}
    ),
    html.P()
], className='bg-opacity-10 m-0 p-2 d-flex align-items-center justify-content-center', style={'height': '95%'})

candlestick_footer = dbc.CardFooter(
    children=['Data Source:',
              html.A(
                  children=['Yahoo Finance'],
                  href='https://finance.yahoo.com/',
                  style={'textDecoration': 'none'}
              )],
    className='border-top border-light d-flex align-items-center justify-content-center',
    style={'height': '5%', 'textAlign': 'left', 'fontSize': '10px', 'fontWeight': 500, 'color': 'white'}
)

# App Initialization

plotly_logo = 'https://images.plot.ly/logo/new-branding/plotly-logomark.png'

app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG],
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}])

app.title = 'Trending Tickers'

# Navbar

navbar = dbc.Navbar([
    dbc.Container([
        html.A([
            dbc.Row([
                dbc.Col(
                    html.Img(
                        src=plotly_logo,
                        height='25px'
                    )
                ),
                dbc.Col(
                    dbc.NavbarBrand(
                        'Trending Tickers Dashboard',
                        className='ms-2',
                        style={'fontWeight': 500, 'color': 'white'}
                    )
                )
            ], align='center', className='g-0')
        ], href='https://plotly.com', style={'textDecoration': 'none'})
    ])
], color='secondary')

# App Layout

app.layout = dbc.Container([
    dcc.Interval(
        id='overall-interval',
        interval=60 * 1000
    ),
    navbar,
    dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([current_header, current_body], className='bg-light',
                                 style={'height': '100%', 'width': '100%'})
                    ], width=12, className='m-0',
                        style={'height': '203.66px', 'paddingTop': '10px', 'paddingBottom': '5px',
                               'paddingLeft': '10px', 'paddingRight': '5px'})
                ], className='m-0 p-0'),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([min_max_header, min_max_body], className='bg-light',
                                 style={'height': '100%', 'width': '100%'})
                    ], width=12, className='m-0',
                        style={'height': '203.66px', 'paddingTop': '5px', 'paddingBottom': '5px', 'paddingLeft': '10px',
                               'paddingRight': '5px'})
                ], className='m-0 p-0'),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([market_cap_header, market_cap_body], className='bg-light',
                                 style={'height': '100%', 'width': '100%'})
                    ], width=12, className='m-0',
                        style={'height': '203.66px', 'paddingTop': '5px', 'paddingBottom': '10px',
                               'paddingLeft': '10px', 'paddingRight': '5px'})
                ], className='m-0 p-0')
            ], width=12, md=3, className='m-0 p-0'),
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Button(
                            'Update Tickers',
                            color='primary',
                            id="button",
                            style={'height': '100%', 'width': '100%'}
                        )
                    ], width=3, className='m-0 d-flex align-items-center justify-content-center',
                        style={'height': '76px', 'paddingTop': '10px', 'paddingBottom': '5px', 'paddingLeft': '5px'}),
                    dbc.Col([
                        html.Label('Ticker', style={'color': 'white'}),
                        dcc.Dropdown(
                            id='ticker',
                            multi=False,
                            clearable=False,
                            maxHeight=140,
                            optionHeight=35
                        )
                    ], width=3, className='v-stack gap-0 m-0',
                        style={'height': '76px', 'paddingTop': '10px', 'paddingBottom': '5px'}),
                    dbc.Col([
                        html.Label('Period', style={'color': 'white'}),
                        dcc.Dropdown(
                            id='period',
                            options=[{'label': '1-Day', 'value': '1d'},
                                     {'label': '5-Days', 'value': '5d'},
                                     {'label': '1-Month', 'value': '1mo'},
                                     {'label': '3-Months', 'value': '3mo'},
                                     {'label': '6-Months', 'value': '6mo'},
                                     {'label': 'Year To Date', 'value': 'ytd'},
                                     {'label': '1-Year', 'value': '1y'},
                                     {'label': '2-Years', 'value': '2y'},
                                     {'label': '5-Years', 'value': '5y'},
                                     {'label': 'Max', 'value': 'max'}],
                            value='1d',
                            multi=False,
                            clearable=False,
                            maxHeight=140,
                            optionHeight=35
                        )
                    ], width=3, className='v-stack gap-0 m-0',
                        style={'height': '76px', 'paddingTop': '10px', 'paddingBottom': '5px'}),
                    dbc.Col([
                        html.Label('Interval', style={'color': 'white'}),
                        dcc.Dropdown(
                            id='interval',
                            multi=False,
                            clearable=False,
                            maxHeight=140,
                            optionHeight=35
                        )
                    ], width=3, className='v-stack gap-0 m-0',
                        style={'height': '76px', 'paddingTop': '10px', 'paddingBottom': '5px'})
                ], className='m-0 p-0'),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([candlestick_body, candlestick_footer], className='bg-light',
                                 style={'height': '100%', 'width': '100%'})
                    ], width=12, className='m-0',
                        style={'height': '535px', 'paddingTop': '5px', 'paddingBottom': '10px', 'paddingLeft': '5px',
                               'paddingRight': '10px'})
                ], className='m-0 p-0')
            ], width=12, md=9, className='m-0 p-0')
        ], className='m-0 p-0'),
        html.Div(
            id='error',
            className='m-0 p-0'
        )
    ], className='m-0 p-0', fluid=True)
], className='m-0 p-0', fluid=True)


# App Callbacks

@app.callback(
    Output('ticker', 'options'),
    Output('ticker', 'value'),
    Input('button', 'n_clicks')
)
def update_ticker_options(n_clicks):
    url = 'https://finance.yahoo.com/lookup'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    table = soup.find('table', {'class': 'trending-table'})
    options = []
    for row in table.tbody.find_all('tr'):
        column_data = row.find('td')
        for i in column_data:
            options.append(i.text)
    value = options[0]
    return options, value


@app.callback(
    Output('interval', 'options'),
    Output('interval', 'value'),
    Input('period', 'value')
)
def update_interval_dropdown(period):
    if period == '1d':
        options = [{'label': f'{x}' + '-Minute', 'value': f'{x}' + 'm'} if x == 1 else {'label': f'{x}' + '-Minutes',
                                                                                        'value': f'{x}' + 'm'} \
                   for x in [1, 2, 5, 15, 30]]
        options.append({'label': '1-Hour', 'value': '60m'})
    elif period == '5d':
        options = [{'label': '1-Hour', 'value': f'{x}' + 'm'} if x == 60 else {'label': f'{x}' + '-Minutes',
                                                                               'value': f'{x}' + 'm'} \
                   for x in [2, 5, 15, 30, 60]]
        options.insert(0, {'label': '1-Minute', 'value': '1m'})
        options.append({'label': '1-Day', 'value': '1d'})
    elif period == '1mo':
        options = [{'label': '1-Hour', 'value': f'{x}' + 'm'} if x == 60 else {'label': f'{x}' + '-Minutes',
                                                                               'value': f'{x}' + 'm'} \
                   for x in [2, 5, 15, 30, 60]]
        options.extend([{'label': '1-Day', 'value': '1d'}, {'label': '1-Week', 'value': '1wk'}])
    elif period == '3mo':
        options = [{'label': '1-Hour', 'value': '60m'},
                   {'label': '1-Day', 'value': '1d'},
                   {'label': '1-Week', 'value': '1wk'}]
    elif period in ('6mo', 'ytd', '1y', '2y'):
        options = [{'label': '1-Hour', 'value': '60m'},
                   {'label': '1-Day', 'value': '1d'},
                   {'label': '1-Week', 'value': '1wk'},
                   {'label': '1-Month', 'value': '1mo'}]
    else:
        options = [{'label': '1-Day', 'value': '1d'},
                   {'label': '1-Week', 'value': '1wk'},
                   {'label': '1-Month', 'value': '1mo'},
                   {'label': '3-Months', 'value': '3mo'}]
    value = options[0]['value']
    return options, value


@app.callback(
    Output('candlestick-body', 'figure'),
    Output('current', 'figure'),
    Output('min-max', 'figure'),
    Output('market', 'figure'),
    Output('error', 'children'),
    Input('overall-interval', 'n_intervals'),
    Input('ticker', 'value'),
    Input('period', 'value'),
    Input('interval', 'value')
)
def update_graph(n_intervals, ticker, period, interval):
    if ((ticker is None) or (period is None) or (interval is None)):
        raise PreventUpdate
    else:
        obj = yf.Ticker(ticker)
        df = obj.history(period=period, interval=interval)
        if df.shape[0] == 0:
            warning = dbc.Modal(
                children=[dbc.ModalHeader(dbc.ModalTitle("Warning!")),
                          dbc.ModalBody(
                              f'{ticker}' + ': No data found for this date range, symbol may be delisted. Please reselect!')],
                size="lg",
                is_open=True
            )
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, warning

        yahoo_financials = YahooFinancials(ticker)
        min_low = yahoo_financials.get_summary_data()[ticker]['fiftyTwoWeekLow']
        max_high = yahoo_financials.get_summary_data()[ticker]['fiftyTwoWeekHigh']
        market_capitalization = yahoo_financials.get_summary_data()[ticker]['marketCap']
        candle = make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.075,
            row_width=[0.35, 1.5]
        )

        candle.add_trace(
            go.Candlestick(
                x=df.index,
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"],
                hoverinfo='x+y'
            ),
            row=1,
            col=1
        )

        candle.add_trace(
            go.Bar(
                x=df.index,
                y=df['Volume'],
                marker=dict(
                    color='dodgerblue'
                ),
                hovertemplate=
                'volume: %{y}<br>' +
                '<extra></extra>'
            ),
            row=2,
            col=1
        )

        candle.update_layout(
            xaxis=dict(
                rangeslider_visible=False
            ),
            yaxis=dict(
                side='right'
            ),
            hovermode='x unified',
            showlegend=False,
            template='plotly_dark',
            margin=dict(l=25, r=25, t=15, b=15),
        )

        current = go.Figure()
        current.add_trace(
            go.Indicator(
                mode="number+delta",
                value=df['Close'].iloc[-1],
                number={'valueformat': '.2f'},
                align='center',
                delta={'reference': df['Close'].iloc[-2], 'relative': True, 'position': 'bottom'},
                title={'text': f'{ticker}', 'font': {'size': 30}},
                domain={'x': [0.2, 0.8], 'y': [0.1, 0.65]}
            )
        )
        if df.shape[0] == 1:
            current.update_traces(
                delta={'reference': df['Close'].iloc[-1], 'relative': True, 'position': 'bottom'}
            )
        else:
            current.update_traces(
                delta={'reference': df['Close'].iloc[-2], 'relative': True, 'position': 'bottom'}
            )
        current.update_layout(
            template='plotly_dark',
            margin=dict(l=0, r=0, t=0, b=0),
            transition_duration=500
        )

        min_max = go.Figure()
        min_max.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=df['Close'].iloc[-1],
                number={'valueformat': '.2f'},
                domain={'x': [0.15, 0.85], 'y': [0.1, 0.8]},
                gauge={'axis': {'range': [min_low, max_high], 'tickwidth': 0.005},
                       'bar': {'color': 'dodgerblue', 'thickness': 0.6},
                       'bordercolor': 'white',
                       'borderwidth': 0.65
                       }
            )
        )
        min_max.update_layout(
            template='plotly_dark',
            font={'size': 8},
            margin=dict(l=0, r=0, t=0, b=0),
            transition_duration=500
        )

        market_cap = go.Figure()
        market_cap.add_trace(
            go.Indicator(
                mode="number",
                value=market_capitalization,
                domain={'x': [0.2, 0.8], 'y': [0.25, 0.75]}
            )
        )
        market_cap.update_layout(
            template='plotly_dark',
            margin=dict(l=0, r=0, t=0, b=0),
            transition_duration=500
        )
        return candle, current, min_max, market_cap, dash.no_update

if __name__ == '__main__':
    app.run_server(debug=True)
