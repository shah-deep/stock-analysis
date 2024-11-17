from dash import html, dcc
import datetime

def create_app_layout():
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    year_options = [{"label": str(year), "value": year} for year in range(current_year-5, current_year+1)]
    month_options = [{"label": datetime.datetime(current_year, month, 1).strftime("%B"), "value": month} for month in range(1, current_month+1)]

    tickers = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "NFLX", "NVDA"]
    default_tickers = ["AAPL", "AMZN", "GOOGL"]
    
    return html.Div(className="container py-4", children=[
        html.H1("StockSense AI", className="mb-4"),
        
        html.Div(className="row mb-4", children=[
            html.Div(className="col-md-4", children=[
                html.Label("Select Assets", className="form-label"),
                dcc.Dropdown(
                    id="asset-dropdown",
                    options=[{"label": ticker, "value": ticker} for ticker in tickers],
                    value=default_tickers,
                    multi=True,
                    className="mb-3"
                )
            ]),
            html.Div(className="col-md-4", children=[
                html.Label("Select Year", className="form-label"),
                dcc.Dropdown(
                    id="year-dropdown",
                    options=year_options,
                    value=current_year,
                    className="mb-3",
                    clearable=False
                )
            ]),
            html.Div(className="col-md-4", children=[
                html.Label("Select Month", className="form-label"),
                dcc.Dropdown(
                    id="month-dropdown",
                    options=month_options,
                    value=current_month,
                    className="mb-3"
                )
            ])
        ]),
        
        
        html.Div(className="row mb-4", children=[
            html.Div(className="col-md-6", children=[
                html.Button(
                    "Analyze Sentiment",
                    id="sentiment-button",
                    n_clicks=0,
                    className="btn btn-secondary"
                )
            ])
        ]),
        
        html.Div(id="performance-plot", className="mb-4"),
        html.Div(id="sentiment-results"),
        html.Div(id="error-display", className="alert alert-danger", style={"display": "none"})
    ])

def create_sentiment_card(asset, sentiment_counts, article_count):
    """Generate a sentiment card for a given asset with sentiment breakdown and article count."""
    return html.Div(className="card mb-3", children=[
        html.Div(className="card-header", children=[
            html.H5(f"{asset} Sentiment Analysis", className="mb-0")
        ]),
        html.Div(className="card-body", children=[
            html.Div(className="row", children=[
                html.Div(className="col-sm-4", children=[
                    html.Div(className="alert alert-success", children=[
                        html.Strong("Positive: "),
                        html.Span(f"{sentiment_counts.get('positive', 0):.1f}%")
                    ])
                ]),
                html.Div(className="col-sm-4", children=[
                    html.Div(className="alert alert-secondary", children=[
                        html.Strong("Neutral: "),
                        html.Span(f"{sentiment_counts.get('neutral', 0):.1f}%")
                    ])
                ]),
                html.Div(className="col-sm-4", children=[
                    html.Div(className="alert alert-danger", children=[
                        html.Strong("Negative: "),
                        html.Span(f"{sentiment_counts.get('negative', 0):.1f}%")
                    ])
                ])
            ]),
            html.Div(className="mt-3 text-muted", children=[
                f"Based on analysis of {article_count} recent news articles"
            ])
        ])
    ])

def create_performance_plot_layout(fig, selected_year, selected_month):
    """Generate layout for displaying performance plot."""
    return html.Div([
        html.H4(f"Performance Visualization for {selected_month}{selected_year}", className="mb-3"),
        dcc.Graph(figure=fig)
    ])
