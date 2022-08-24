import datetime
import random

import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots

# https://dash.plotly.com/live-updates

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.H4('Two random plots'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=25,  # in milliseconds
            n_intervals=0
        )
    ])
)

DATA = {
    'time': [],
    'val0': [],
    'val1_1': [],
    'val1_2': []
}


def update_data():
    DATA['val0'].append(random.randint(0, 50))
    DATA['val1_1'].append(random.randint(0, 50))
    DATA['val1_2'].append(random.randint(0, 50))
    DATA['time'].append(datetime.datetime.now())


@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    update_data()

    # Create the graph with subplots
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.2)
    fig['layout']['margin'] = {'l': 30, 'r': 10, 'b': 30, 't': 10}
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}
    fig['layout']['uirevision'] = 'some-constant'


    fig.add_trace({
        'x': DATA['time'],
        'y': DATA['val0'],
        'name': 'val 0',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)

    fig.add_trace({
        'x': DATA['time'],
        'y': DATA['val1_1'],
        'text': DATA['time'],
        'name': 'val 1.1',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 2, 1)

    fig.add_trace({
        'x': DATA['time'],
        'y': DATA['val1_2'],
        'text': DATA['time'],
        'name': 'val 1.2',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 2, 1)

    return fig


if __name__ == '__main__':
    app.run_server()