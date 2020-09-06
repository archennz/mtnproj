import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# load data
data = pd.read_csv('names.csv', index_col= 'id')

# making graphics
fig = px.density_mapbox(data, 
                        lat = 'latitude', lon = 'longitude', z = 'stars', radius = 15,
                        center=dict(lat=34.012, lon=-116.168), zoom=10,
                        mapbox_style="stamen-terrain"
                       )


# or plotly.express as px
#fig = go.Figure() # or any Plotly Express function e.g. px.bar(...)
# fig.add_trace( ... )
# fig.update_layout( ... )


markdown_text = '''
# Title
## Subtitle
### etc

'''

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# app.layout = html.Div([
# 	dcc.Markdown(markdown_text),
#     dcc.Graph(figure=fig)
# ])




#app.run_server(debug=True, use_reloader=False)


app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),

    dcc.RangeSlider(
        id='grade-slider',
        min=data['grade'].min(),
        max=data['grade'].max(),
        marks={str(grade): ('5.'+str(grade)) for grade in range(data['grade'].min(), data['grade'].max()+1)},
        step=None,
        allowCross = False,
        value = [data['grade'].min(), data['grade'].max()]
    )
])

# @app.callback(
#     dash.dependencies.Output('slider-output-container', 'children'),
#     [dash.dependencies.Input('grade-slider', 'value')])


if __name__ == '__main__':
    app.run_server(debug=True)

