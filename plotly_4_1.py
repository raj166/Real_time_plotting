import pandas as pd
import dash
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
pd.options.plotting.backend = "plotly"
countdown = 20

# sample dataframe of a wide format
np.random.seed(4);

df = pd.read_csv('data.csv')
df['Time'] = pd.to_datetime(df['Time'], format='%m/%d/%Y %H:%M:%S', errors='ignore')
# plotly figure
fig1 = px.line(df, x='Time', y='x_value', template='plotly_dark', height=400)
fig2 = px.line(df, x='Time', y='total_1', template='plotly_dark', height=400)
fig3 = px.line(df, x='Time', y='total_2', template='plotly_dark', height=400)

fig = make_subplots(rows=1, cols=3,
                    specs=[
                        [{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}],

                    ])
fig.add_trace(go.Indicator(mode="number", value=df['x_value'].sum(), title="Confirmed Cases"), row=1, col=1)
fig.add_trace(go.Indicator(mode="number", value=df['total_1'].sum(), title="Recovered Cases"), row=1, col=2)
fig.add_trace(go.Indicator(mode="number", value=df['total_2'].sum(), title="Deaths Cases"), row=1, col=3)

app = dash.Dash(__name__, )
app.layout = html.Div([
    html.H1("Streaming of Sensors data"),
    html.Div(id='live-update-text'),
    dcc.Graph(id='graph1'),
    dcc.Graph(id='graph2'),
    dcc.Graph(id='graph3'),
    dcc.Interval(
        id='interval-component',
        interval=1000,  # in milliseconds
        n_intervals=0
    ),

])


@app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):
    data = pd.read_csv('data.csv')
    x = data['x_value']
    y1 = data['total_1']
    y2 = data['total_2']

    x_value, Total_1, Total_2 = x.values[-1], y1.values[-1], y2.values[-1]
    style = {'padding': '50px', 'fontSize': '27px'}
    return [
        html.Span('Sensor 1: {}'.format(x_value), style=style),
        html.Span('Sensor 2: {}'.format(Total_1), style=style),
        html.Span('Sensor 3: {}'.format(Total_2), style=style)
    ]


# Define callback to update graph1
@app.callback(Output('graph1', 'figure'), [Input('interval-component', "n_intervals")])
def streamFig1(value):
    global count
    df1 = pd.read_csv('data.csv', usecols=[0, 1], index_col=None,)
    df1 = df1.tail(30)
    df1['Time'] = pd.to_datetime(df1['Time'], format='%m/%d/%Y %H:%M:%S', errors='ignore')
    fig1 = go.Figure()
    fig1 = px.line(df1, x='Time', y='x_value', template='plotly_dark', height=400)
    fig1.add_trace(go.Scatter(x=df1['Time'][-2:], y=df1['x_value'][-2:], mode='markers+text', text=df1['x_value'][-2:],
                              textposition='top center', fill='tonext'))
    fig1.update_xaxes(autorange=True, nticks=30)
    return fig1


# Define callback to update graph2
@app.callback(Output('graph2', 'figure'), [Input('interval-component', "n_intervals")])
def streamFig1(value):
    global count
    df2 = pd.read_csv('data.csv', usecols=[0, 2], index_col=None,)
    df2 = df2.tail(30)
    df2['Time'] = pd.to_datetime(df2['Time'], format='%m/%d/%Y %H:%M:%S', errors='ignore')
    x_axis = df2.index.values[-30:]
    fig2 = go.Figure()
    fig2 = px.line(df2, x='Time', y='total_1', template='plotly_dark', height=400)
    fig2.add_trace(go.Scatter(x=df2['Time'][-2:], y=df2['total_1'][-2:], mode='markers+text', text=df2['total_1'][-2:],
                              textposition='top center', fill='tonext'))
    fig2.update_xaxes(autorange=True, nticks=30)
    return fig2


# Define callback to update graph3
@app.callback(Output('graph3', 'figure'), [Input('interval-component', "n_intervals")])
def streamFig1(value):
    global count
    df3 = pd.read_csv('data.csv', usecols=[0, 3], index_col=None,)
    df3 = df3.tail(30)
    df3['Time'] = pd.to_datetime(df3['Time'], format='%m/%d/%Y %H:%M:%S', errors='ignore')
    fig3 = go.Figure()
    fig3 = px.line(df3, x='Time', y='total_2', template='plotly_dark', height=400)
    fig3.add_trace(go.Scatter(x=df3['Time'][-2:], y=df3['total_2'][-2:], mode='markers+text', text=df3['total_2'][-2:],
                              textposition='top center', fill='tonext'))
    fig3.update_xaxes(autorange=True, nticks=30)
    return fig3


external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_css:
    app.scripts.append_script({'external_url': js})

if __name__ == '__main__':
    app.run_server(debug=True, port=5000)
