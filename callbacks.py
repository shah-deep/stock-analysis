import dash
from dash import dcc, Input, Output, State, html
import pandas as pd
from layouts import create_sentiment_card, create_performance_plot_layout
from data_manager import fetch_stock_data
from sentiment_analysis import fetch_news, analyze_sentiment
import plotly.graph_objs as go

def register_callbacks(app):
    """Register all callbacks for the application."""
    
    @app.callback(
        Output("performance-plot", "children"),
        [Input("asset-dropdown", "value"), Input("year-dropdown", "value")]
    )
    def update_performance_plot(selected_assets, selected_year):
        if not selected_assets:
            return html.Div("Please select at least one asset", className="alert alert-warning")

        # Calculate start and end dates based on the selected year
        start_date = f"{selected_year}-01-01"
        end_date = f"{selected_year}-12-31"

        # Fetch stock data for selected assets within the selected year
        data = fetch_stock_data(selected_assets, start_date, end_date)

        # Generate the plot
        fig = go.Figure()
        for asset in selected_assets:
            fig.add_trace(go.Scatter(x=data.index, y=data[asset], mode="lines", name=asset))

        fig.update_layout(
            title=f"Stock Performance in {selected_year}",
            xaxis_title="Date",
            yaxis_title="Adjusted Closing Price",
            template="plotly_white"
        )

        return create_performance_plot_layout(fig)
    
    
    @app.callback(
        [Output("sentiment-results", "children"),
         Output("error-display", "children"),
         Output("error-display", "style")],
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
