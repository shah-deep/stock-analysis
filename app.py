import dash
from flask_caching import Cache
from layouts import create_app_layout
from callbacks import register_callbacks

# Initialize Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=['https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css']
)
app.title = "Individual Stock Sentiment & Performance Analysis"

# Configure caching
cache = Cache(
    app.server,
    config={
        "CACHE_TYPE": "SimpleCache",
        "CACHE_DEFAULT_TIMEOUT": 300
    }
)

# Set up app layout
app.layout = create_app_layout()  # Removed the TICKERS argument

# Register callbacks
register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)
