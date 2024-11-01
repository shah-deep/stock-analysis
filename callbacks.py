import dash
from dash import dcc, Input, Output, State, html
import numpy as np
import pandas as pd
from layouts import create_performance_metrics_layout, create_sentiment_card, create_performance_plot_layout
from data_manager import fetch_stock_data, calculate_portfolio_metrics, portfolio_performance, create_portfolio_performance_plot
from sentiment_analysis import fetch_news, analyze_sentiment

def register_callbacks(app):
    """Register all callbacks for the application."""
    
    @app.callback(
        Output("weight-sliders", "children"),
        Input("asset-dropdown", "value")
    )
    def update_weight_sliders(selected_assets):
        if not selected_assets:
            return html.Div("Please select at least one asset", className="alert alert-warning")
        
        return html.Div(className="row", children=[
            html.Div(className="col-md-6 mb-3", children=[
                html.Label(f"Weight for {asset}", className="form-label"),
                dcc.Slider(
                    id={'type': 'weight-slider', 'index': asset},
                    min=0,
                    max=1,
                    step=0.01,
                    value=1/len(selected_assets),
                    marks={i/10: str(i/10) for i in range(0, 11)},
                    className="mb-3"
                )
            ]) for asset in selected_assets
        ])

    @app.callback(
        [Output("performance-metrics", "children"),
         Output("performance-plot", "children"),
         Output("error-display", "children"),
         Output("error-display", "style")],
        [Input("calc-button", "n_clicks")],
        [State("asset-dropdown", "value"),
         State({"type": "weight-slider", "index": dash.dependencies.ALL}, "value")]
    )
    def display_portfolio_performance(n_clicks, selected_assets, weights):
        if n_clicks == 0:
            return "", "", "", {"display": "none"}
        
        try:
            if not selected_assets or not weights:
                raise ValueError("Please select assets and set weights")
            
            data = fetch_stock_data(selected_assets, 365 * 3)  # 3 years of data
            daily_returns = data.pct_change(fill_method=None).dropna()
            expected_returns, cov_matrix = calculate_portfolio_metrics(daily_returns)
            
            weights = np.array(weights)
            port_return, port_volatility, sharpe_ratio = portfolio_performance(
                weights, expected_returns, cov_matrix
            )
            
            # Create performance plot
            performance_fig = create_portfolio_performance_plot(data, weights)
            
            return (
                create_performance_metrics_layout(port_return, port_volatility, sharpe_ratio), 
                create_performance_plot_layout(performance_fig), 
                "", 
                {"display": "none"}
            )
            
        except Exception as e:
            return "", "", str(e), {"display": "block"}

    @app.callback(
        [Output("sentiment-results", "children"),
         Output("error-display", "children", allow_duplicate=True),
         Output("error-display", "style", allow_duplicate=True)],
        [Input("sentiment-button", "n_clicks")],
        [State("asset-dropdown", "value")],
        prevent_initial_call=True
    )
    def display_sentiment_analysis(n_clicks, selected_assets):
        if n_clicks == 0:
            return "", "", {"display": "none"}
        
        try:
            if not selected_assets:
                raise ValueError("Please select assets for sentiment analysis")
            
            sentiment_output = []
            for asset in selected_assets:
                news = fetch_news(asset)
                if not news:
                    continue
                    
                sentiments = analyze_sentiment(news)
                sentiment_counts = pd.Series(sentiments).value_counts(normalize=True) * 100
                
                sentiment_output.append(create_sentiment_card(asset, sentiment_counts, len(news)))
            
            if not sentiment_output:
                return html.Div(
                    "No news articles found for analysis",
                    className="alert alert-warning"
                ), "", {"display": "none"}
            
            return html.Div(sentiment_output), "", {"display": "none"}
            
        except Exception as e:
            return "", str(e), {"display": "block"}