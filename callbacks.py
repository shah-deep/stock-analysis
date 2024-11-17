import dash
from dash import dcc, Input, Output, State, html
import pandas as pd
import calendar
from layouts import create_sentiment_card, create_performance_plot_layout
from data_manager import fetch_stock_data
from sentiment_analysis import fetch_news, analyze_sentiment
import plotly.express as px

def register_callbacks(app):
    
    @app.callback(
        Output("performance-plot", "children"),
        [Input("asset-dropdown", "value"), Input("year-dropdown", "value"), Input("month-dropdown", "value")]
    )
    def update_performance_plot(selected_assets, selected_year, selected_month):
        if not selected_assets:
            return html.Div("Please select at least one asset", className="alert alert-warning")

        # Calculate start and end dates
        if(selected_month):
            last_day = calendar.monthrange(selected_year, selected_month)[1]
            start_date = f"{selected_year}-{selected_month:02d}-01"
            end_date = f"{selected_year}-{selected_month:02d}-{last_day}"
        else:
            start_date = f"{selected_year}-01-01"
            end_date = f"{selected_year}-12-31"

        # Fetch stock data for selected assets within the selected year
        data = fetch_stock_data(selected_assets, start_date, end_date)

        # Generate the plot
        fig = px.line(data, x=data.index, y=selected_assets, 
                      labels={"value": "Closing Price", "Date": "Time", "variable": ""},
                      template="plotly_white")
        if(selected_month):
            month_str = calendar.month_name[selected_month] + " "
        else:
            month_str = ""
        return create_performance_plot_layout(fig, selected_year, month_str)
    
    

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
            print(f"Error in sentiment analysis: {e}")
            return "", str(e), {"display": "block"}
