import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np

from ast import literal_eval


# setting seed for random number generator
np.random.seed(20)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# load data
df = pd.read_csv('app_data/whole_jt_data.csv', index_col= 'id')

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


server = app.server

#app.run_server(debug=True, use_reloader=False)


app.layout = html.Div(children=[
	# heading text
    html.H1('Where to climb? A visualization of better crags to hit.'),

    html.Div('''
        Select the grades you want to climb and filter for protection ratings(R-rated etc.). 
        Then the heatmap will tell you where the best crags are. Using the spread drop down to 
        adjust the clustering.
    	'''),

    # html.Div(
    #     dcc.RangeSlider(
    # 	id = 'star-slider',
    # 	min=df['stars'].min(),
	   #  max=df['stars'].max(),
	   #  marks = {str(star/10): str(star/10) for star in range(int(df['stars'].min())*10, int(df['stars'].max())*10+1)},
	   #  step = None,
	   #  value = [int(df['stars'].min()), int(df['stars'].max())]
	   #  	)
    # 	),



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
    	
    	html.Label('Spread'),
    	dcc.Dropdown(
    	id = 'radius-option',
    	options = [ { 'label':str(val), 'value': val} for val in [0,1,2,3,4,5,7,10,15,20]],
    	value = 10
    		)
    	,

	    html.Label('Grade Range (YDS)'),
	    dcc.RangeSlider(
	        id='grade-slider',
	        min=df['grade'].min(),
	        max=df['grade'].max()+1,
	        marks={str(grade): ('5.'+str(grade)) for grade in range(df['grade'].min(), df['grade'].max()+2)},
	        step=None,
	        allowCross = False,
	        value = [df['grade'].min()+1, df['grade'].max()],
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
def add_vibrations(data):
	"""
	spread climb locations sort of uniformly in a circle around base lat/long
	"""
	radius = np.random.uniform(0, 0.0003, len(data))
	angle = np.random.uniform(0, 2*np.pi, len(data))
	lat_del = radius* np.sin(angle)
	long_del = radius* np.cos(angle)
	data['latitude'] = data['latitude'] + lat_del
	data['longitude'] = data['longitude'] + long_del

def add_cragnames(data):
	"""Extract crag names from locations"""
	data['area'] = data['location'].apply(lambda x : literal_eval(x)[0])


def filter_data(data, min_g, max_g, PG_bool, R_bool, X_bool):
	"""
	filters the dataframe according to users selection of grade range 
	and safety ratings
	"""
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
     dash.dependencies.Input('safety', 'value'),
     dash.dependencies.Input('radius-option', 'value')])
def update_graph(grade_bounds, safety_fil, radius_v):
	[min_g, max_g] = grade_bounds
	PG_bool = ('PG13' in safety_fil)
	R_bool = ('R' in safety_fil)
	X_bool = ('X' in safety_fil)
	add_vibrations(df)
	add_cragnames(df)
	df_filter = filter_data(df, min_g, max_g, PG_bool, R_bool, X_bool)
	fig = px.density_mapbox(df_filter, 
	                        lat = 'latitude', lon = 'longitude', z = 'stars', radius = radius_v,
	                        hover_name = 'name', 
	                        hover_data = {'longitude':False, 'latitude':False, 'area':True, 'stars':True, 'rating':True},
	                        #colorscale = Jet,
	                        center=dict(lat=34.012, lon=-116.168), zoom=10,
	                        opacity = 0.7
	                       )
	fig['layout']['uirevision'] = 'some-constant'
	fig.update_layout(mapbox_style="open-street-map")
	return fig	


if __name__ == '__main__':
    app.run_server(debug=True)

