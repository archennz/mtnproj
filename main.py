import pandas as pd
import plotly.express as px


#load data
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


import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()
app.layout = html.Div([
	html.Div('hi'),
    dcc.Graph(figure=fig)
])


if __name__ == '__main__':
    app.run_server(debug=True)

#app.run_server(debug=True, use_reloader=False)