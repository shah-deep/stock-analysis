import dash
from layouts import create_app_layout
from callbacks import register_callbacks

app = dash.Dash(
    __name__,
    external_stylesheets=['https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css']
)
app.title = "Stock Analysis"

# Set up app layout
app.layout = create_app_layout()

# Register callbacks
register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=False)
