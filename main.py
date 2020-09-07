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
	# heading text
    html.H1('Where to climb? A visualization of better crags to hit.'),

    html.Div('''
        Select the grades you want to climb and filter for commitment(no X-rated etc). 
        Then the heatmap will tell you where the best crags are. 
    	'''),

    # column 1
    html.Div(style = {'display':'flex' , 'flex-direction':'row'},
    	children=[
    	html.Div(
    		dcc.Graph(id='graph',
    					style = {'height':'90vh', 'width':'80vw'})
    		),

    #column2
    html.Div(
    	style = {'background':'AliceBlue'},
    	children=[
	    html.Label('Grade Range'),
	    dcc.RangeSlider(
	        id='grade-slider',
	        min=data['grade'].min(),
	        max=data['grade'].max(),
	        marks={str(grade): ('5.'+str(grade)) for grade in range(data['grade'].min(), data['grade'].max()+1)},
	        step=None,
	        allowCross = False,
	        value = [data['grade'].min(), data['grade'].max()],
	        vertical = True
	    ),

	    html.Label('Include the following:'),
	    dcc.Checklist(
	    	id = 'safety',
	        options=[
	            {'label': 'PG13', 'value': 'PG13'},
	            {'label': 'R', 'value': 'R'},
	            {'label': 'X', 'value': 'X'}
	        ],
	        value=['PG13', 'R', 'X'])
	    ])
    ])
])


def filter_data(min_g, max_g, PG_bool, R_bool, X_bool):
	fil_data = data[(data['grade'] >= min_g) & (data['grade']<= max_g)]
	if PG_bool == False:
		fil_data = fil_data[(fil_data['safety'] == 'PG13') ==False]
	if R_bool == False:
		fil_data = fil_data[(fil_data['safety'] == 'R') ==False]
	if X_bool == False:
		fil_data = fil_data[(fil_data['safety'] == 'X') ==False]
	return fil_data		


@app.callback(
     dash.dependencies.Output('graph', 'figure'),
     [dash.dependencies.Input('grade-slider', 'value'),
     dash.dependencies.Input('safety', 'value')])
def update_graph(grade_bounds, safety_fil):
	[min_g, max_g] = grade_bounds
	PG_bool = ('PG13' in safety_fil)
	R_bool = ('R' in safety_fil)
	X_bool = ('X' in safety_fil)
	fil_data = filter_data(min_g, max_g, PG_bool, R_bool, X_bool)
	fig = px.density_mapbox(fil_data, 
	                        lat = 'latitude', lon = 'longitude', z = 'stars', radius = 15,
	                        hover_name = 'name', 
	                        hover_data = {'longitude':False, 'latitude':False, 'stars':True, 'rating':True},
	                        #colorscale = Jet,
	                        center=dict(lat=34.012, lon=-116.168), zoom=10,
	                        #mapbox_style="stamen-terrain"
	                       )
	fig.update_layout(mapbox_style="open-street-map")
	return fig	


if __name__ == '__main__':
    app.run_server(debug=True)

