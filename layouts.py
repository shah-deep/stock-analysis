from dash import html, dcc
import plotly.graph_objs as go

def create_app_layout(tickers):
    """Create the main application layout."""
    return html.Div(className="container py-4", children=[
        html.H1("AI-Powered Financial Portfolio Optimizer", className="mb-4"),
        
        html.Div(className="row mb-4", children=[
            html.Div(className="col-md-6", children=[
                html.Label("Select Assets", className="form-label"),
                dcc.Dropdown(
                    id="asset-dropdown",
                    options=[{"label": ticker, "value": ticker} for ticker in tickers],
                    value=tickers,
                    multi=True,
                    className="mb-3"
                )
            ])
        ]),
        
        html.Div(id="weight-sliders", className="mb-4"),
        
        html.Div(className="row mb-4", children=[
            html.Div(className="col-md-6", children=[
                html.Button(
                    "Calculate Portfolio Performance",
                    id="calc-button",
                    n_clicks=0,
                    className="btn btn-primary me-2"
                ),
                html.Button(
                    "Analyze Sentiment",
                    id="sentiment-button",
                    n_clicks=0,
                    className="btn btn-secondary"
                )
            ])
        ]),
        
        html.Div(id="performance-metrics", className="mb-4"),
        html.Div(id="performance-plot", className="mb-4"),
        html.Div(id="sentiment-results"),
        html.Div(id="error-display", className="alert alert-danger", style={"display": "none"})
    ])


def create_performance_metrics_layout(port_return, port_volatility, sharpe_ratio):
    """Generate layout for displaying portfolio performance metrics."""
    return html.Div([
        html.H3("Portfolio Metrics", className="mb-3"),
        html.Div(className="row", children=[
            html.Div(className="col-md-4", children=[
                html.Div(className="card", children=[
                    html.Div(className="card-body", children=[
                        html.H5("Expected Annual Return", className="card-title"),
                        html.P(f"{port_return:.2%}", className="card-text")
                    ])
                ])
            ]),
            html.Div(className="col-md-4", children=[
                html.Div(className="card", children=[
                    html.Div(className="card-body", children=[
                        html.H5("Annual Volatility", className="card-title"),
                        html.P(f"{port_volatility:.2%}", className="card-text")
                    ])
                ])
            ]),
            html.Div(className="col-md-4", children=[
                html.Div(className="card", children=[
                    html.Div(className="card-body", children=[
                        html.H5("Sharpe Ratio", className="card-title"),
                        html.P(f"{sharpe_ratio:.2f}", className="card-text")
                    ])
                ])
            ])
        ])
    ])



def create_sentiment_card(asset, sentiment_counts, article_count):
    """Generate a sentiment card for a given asset with sentiment breakdown and article count."""
    return html.Div(className="card mb-3", children=[
        html.Div(className="card-header", children=[
            html.H4(f"{asset} Sentiment Analysis", className="mb-0")
        ]),
        html.Div(className="card-body", children=[
            html.Div(className="row", children=[
                html.Div(className="col-md-4", children=[
                    html.Div(className="alert alert-success", children=[
                        html.Strong("Positive: "),
                        html.Span(f"{sentiment_counts.get('positive', 0):.1f}%")
                    ])
                ]),
                html.Div(className="col-md-4", children=[
                    html.Div(className="alert alert-secondary", children=[
                        html.Strong("Neutral: "),
                        html.Span(f"{sentiment_counts.get('neutral', 0):.1f}%")
                    ])
                ]),
                html.Div(className="col-md-4", children=[
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



def create_performance_plot_layout(fig):
    """Generate layout for displaying performance plot."""
    return html.Div([
        html.H3("Performance Visualization", className="mb-3"),
        dcc.Graph(figure=fig)
    ])