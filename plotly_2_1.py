import pandas as pd
import dash
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots

# code and plot setup
# settings
pd.options.plotting.backend = "plotly"
countdown = 20
# global df

# sample dataframe of a wide format
np.random.seed(4);

df = pd.read_csv('data.csv')
# plotly figure
fig1 = px.line(df, x='Time', y='x_value', template='plotly_dark', text='x_value')
fig2 = px.line(df, x='Time', y='total_1', template='plotly_dark', text='total_1')
fig3 = px.line(df, x='Time', y='total_2', template='plotly_dark', text='total_2')

fig = make_subplots(rows=1, cols=3,
                    specs=[
                        [{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}],

                    ])
fig.add_trace(go.Indicator(mode="number", value=df['x_value'].sum(), title="Confirmed Cases"), row=1, col=1)
fig.add_trace(go.Indicator(mode="number", value=df['total_1'].sum(), title="Recovered Cases"), row=1, col=2)
fig.add_trace(go.Indicator(mode="number", value=df['total_2'].sum(), title="Deaths Cases"), row=1, col=3)

app = dash.Dash(__name__, )
app.layout = html.Div([
    html.H1("Streaming of random data"),
    dcc.Interval(
        id='interval-component',
        interval=1000,  # in milliseconds
        n_intervals=0
    ),
    dcc.Graph(id='graph_text_1'),
    dcc.Graph(id='graph1'),
    dcc.Graph(id='graph2'),
    dcc.Graph(id='graph3'),

])


# Define callback to update graph
@app.callback(Output('graph1', 'figure'), [Input('interval-component', "n_intervals")])
def streamFig1(value):
    df1 = pd.read_csv('data.csv', usecols=[0, 1], index_col=None)
    fig1 = px.line(df, x='Time', y='x_value', template='plotly_dark', text='x_value')
    fig1.update_xaxes(nticks=30)
    return fig1


# Define callback to update graph
@app.callback(Output('graph2', 'figure'), [Input('interval-component', "n_intervals")])
def streamFig1(value):
    df2 = pd.read_csv('data.csv', usecols=[0, 2], index_col=None)
    x_axis = df2.index.values[-30:]
    fig2 = px.line(df, x='Time', y='total_1', template='plotly_dark', text='total_1')
    fig2.update_xaxes(nticks=30)
    return fig2


# Define callback to update graph
@app.callback(Output('graph3', 'figure'), [Input('interval-component', "n_intervals")])
def streamFig1(value):
    df3 = pd.read_csv('data.csv', usecols=[0, 3], index_col=None)
    fig3 = px.line(df3, x='Time', y='total_2', template='plotly_dark', text='total_2')
    fig3.update_xaxes(nticks=30)
    return fig3


# Define callback to update graph
@app.callback(Output('graph_text_1', 'figure'), [Input('interval-component', "n_intervals")])
def streamFig1(value):
    df = pd.read_csv('data.csv')
    fig.add_trace(go.Indicator(mode="number", value=df['x_value'].sum(), title="Confirmed Cases"), row=1, col=1)
    fig.add_trace(go.Indicator(mode="number", value=df['total_1'].sum(), title="Recovered Cases"), row=1, col=2)
    fig.add_trace(go.Indicator(mode="number", value=df['total_2'].sum(), title="Deaths Cases"), row=1, col=3)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=5000)
