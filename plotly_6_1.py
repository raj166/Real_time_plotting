import pandas as pd
import dash
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
from adtk.detector import ThresholdAD
from adtk.detector import LevelShiftAD
from adtk.detector import InterQuartileRangeAD

iqr_ad = InterQuartileRangeAD(c=1.5)

pd.options.plotting.backend = "plotly"
countdown = 20

df = pd.read_csv('airplane_data.csv')
df['Time'] = pd.to_datetime(df['Time'], format='%m/%d/%Y,%H:%M:%S', errors='ignore')
# plotly figure
fig1 = px.line(df, x='Time', y='s1', template='plotly_dark', height=200)
fig2 = px.line(df, x='Time', y='s2', template='plotly_dark', height=200)
fig3 = px.line(df, x='Time', y='s3', template='plotly_dark', height=200)

fig = make_subplots(rows=1, cols=3,
                    specs=[
                        [{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}]])

app = dash.Dash(__name__)
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
    )])


@app.callback(Output('live-update-text', 'children'), Input('interval-component', 'n_intervals'))
def update_metrics(n):
    data = pd.read_csv('airplane_data.csv')
    s1_df = data['s1']
    s2_df = data['s2']
    s3_df = data['s3']
    sensor1, sensor2, sensor3 = s1_df.values[-1], s2_df.values[-1], s3_df.values[-1]
    style = {'padding': '50px', 'fontSize': '27px', 'font-weight': 'bold'}
    return [
        html.Span('Sensor 1 : {:.4f}'.format(sensor1), style=style),
        html.Span('Sensor 2 : {:.4f}'.format(sensor2), style=style),
        html.Span('Sensor 3 : {:.4f}'.format(sensor3), style=style)
    ]


# Define callback to update graph1
@app.callback(Output('graph1', 'figure'), [Input('interval-component', "n_intervals")])
def streamFig1(value):
    df1 = pd.read_csv('airplane_data.csv', usecols=[0, 1], index_col=None, )
    df1 = df1.tail(60)
    df1['Time'] = pd.to_datetime(df1['Time'], format='%m/%d/%Y,%H:%M:%S', errors='ignore')
    fig1 = go.Figure()
    fig1 = px.line(df1, x='Time', y='s1', template='plotly_dark', height=200)
    fig1.add_trace(go.Scatter(x=df1['Time'][-3:], y=df1['s1'][-3:], mode='markers+text', text=df1['s1'][-3:],
                              textposition='top center', fill='none', showlegend=False, texttemplate='%{text:.2f}'))
    fig1.update_xaxes(title=" ", autorange=True, nticks=60, )
    fig1.update_yaxes(title='')
    fig1.update_layout(height=250)
    return fig1


# Define callback to update graph2
@app.callback(Output('graph2', 'figure'), [Input('interval-component', "n_intervals")])
def streamFig1(value):
    df2 = pd.read_csv('airplane_data.csv', usecols=[0, 2], index_col=0)
    df2 = df2.tail(60)
    df2.index = pd.to_datetime(df2.index, format='%m/%d/%Y,%H:%M:%S', errors='ignore')
    anomalies = iqr_ad.fit_detect(df2)
    fig2 = go.Figure()
    fig2 = px.line(df2, x=df2.index, y='s2', template='plotly_dark', height=200)
    fig2.add_trace(go.Scatter(x=df2.index[-3:], y=df2['s2'][-3:], mode='markers+text', text=df2['s2'][-3:],
                              textposition='top center', fill='none', showlegend=False, texttemplate='%{text:.2f}',
                              name='Sensor 2 values'))
    fig2.add_trace(
        go.Scatter(x=anomalies[anomalies['s2'] == True].index, y=df2[anomalies['s2'] == True].s2.values,
                   mode='markers', fill='toself', fillcolor='rgba(255,144,111,0.5)'))

    fig2.update_xaxes(title=" ", autorange=True, nticks=60, )
    fig2.update_yaxes(title='')
    fig2.update_layout(height=250, showlegend=False)
    return fig2


# Define callback to update graph3
@app.callback(Output('graph3', 'figure'), [Input('interval-component', "n_intervals")])
def streamFig1(value):
    df3 = pd.read_csv('airplane_data.csv', usecols=[0, 3], index_col=0)
    df3 = df3.tail(60)
    df3.index = pd.to_datetime(df3.index, format='%m/%d/%Y,%H:%M:%S', errors='ignore')
    threshold_ad = ThresholdAD(high=0.604727, low=0.274730)
    anomalies = threshold_ad.detect(df3)
    fig3 = go.Figure()
    fig3 = px.line(df3, x=df3.index, y='s3', template='plotly_dark', height=200)
    fig3.add_trace(go.Scatter(x=df3.index[-3:], y=df3['s3'][-3:], mode='markers+text', text=df3['s3'][-3:],
                              textposition='top center', fill='none', showlegend=False, texttemplate='%{text:.2f}',
                              name='Sensor 3 values', fillcolor='rgba(255,144,111,0.5)'))
    fig3.add_trace(
        go.Scatter(x=anomalies[anomalies['s3'] == True].index, y=df3[anomalies['s3'] == True].s3.values,
                   mode='markers', fill='toself', fillcolor='rgba(255,144,111,0.5)'))

    fig3.update_xaxes(title=" ", autorange=True, nticks=60, )
    fig3.update_yaxes(title='')
    fig3.update_layout(height=250, showlegend=False)
    return fig3


external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_css:
    app.scripts.append_script({'external_url': js})

if __name__ == '__main__':
    app.run_server(debug=True, port=5000)
