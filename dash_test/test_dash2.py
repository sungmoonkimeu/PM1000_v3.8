import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from jupyter_dash import JupyterDash
from dash import dcc, html
from dash.dependencies import Input, Output

# code and plot setup
# settings
pd.options.plotting.backend = "plotly"
countdown = 20
# global df

# sample dataframe of a wide format
np.random.seed(4)
cols = list('abc')
X = np.random.randn(50, len(cols))
df = pd.DataFrame(X, columns=cols)
df.iloc[0] = 0

# plotly figure
fig = df.plot(template='plotly_dark')

app = JupyterDash(__name__)
app.layout = html.Div([
    html.H1("Streaming of random data"),
    dcc.Interval(
        id='interval-component',
        interval=1 * 100,  # in milliseconds
        n_intervals=0
    ),
    dcc.Graph(id='graph'),
])


# Define callback to update graph
@app.callback(
    Output('graph', 'figure'),
    [Input('interval-component', "n_intervals")]
)
def streamFig(value):
    global df

    Y = np.random.randn(1, len(cols))
    df2 = pd.DataFrame(Y, columns=cols)
    df = df.append(df2, ignore_index=True)  # .reset_index()
    df.tail()
    df3 = df.copy()
    df3 = df3.cumsum()
    fig = df3.plot(template='plotly_dark')
    # fig.show()
    return (fig)


app.run_server(mode='external', port=8069, dev_tools_ui=True,  # debug=True,
               dev_tools_hot_reload=True, threaded=True)