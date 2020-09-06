import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# load data
data = pd.read_csv('names.csv', index_col= 'id')

# making graphics



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
    html.H1('Where to climb? A visualization of better crags to hit.'),

    html.Div('''
        Select the grades you want to climb and filter for commitment(no X-rated etc). 
        Then the heatmap will tell you where the bests crags are. 
    '''),

    dcc.Graph(
        id='graph'
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

@app.callback(
     dash.dependencies.Output('graph', 'figure'),
     [dash.dependencies.Input('grade-slider', 'value')])
def update_graph(grade_bounds):
	[min_g, max_g] = grade_bounds
	fil_data = data[(data['grade'] >= min_g) & (data['grade']<= max_g)]
	fig = px.density_mapbox(fil_data, 
	                        lat = 'latitude', lon = 'longitude', z = 'stars', radius = 15,
	                        hover_name = 'name', 
	                        hover_data = {'longitude':False, 'latitude':False, 'stars':True, 'rating':True},
	                        center=dict(lat=34.012, lon=-116.168), zoom=10,
	                        mapbox_style="stamen-terrain"
	                       )

	return fig	


if __name__ == '__main__':
    app.run_server(debug=True)

