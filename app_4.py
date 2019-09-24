import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from plotly import graph_objs as go

import pandas as pd

mapbox_access_token = 'pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w'

##################################################
trd = pd.read_csv('./data/UNI_TRD_ENF17.csv')
print(trd.CONJ.unique())

map_layout = go.Layout(
        mapbox= go.layout.Mapbox(
            accesstoken= mapbox_access_token,
            center= dict(lat=trd.lat[0], lon=trd.lon[0]),
            zoom=10,
            pitch=45,
            style='light'),
        margin= dict(l=10,t=10,b=10,r=10)
        )

app = dash.Dash(__name__)
server = app.server

###################################################
# Layout
###################################################

app.layout = html.Div([

    html.H1("Mapa de distribucion Electrica", style={'text-align':'center'}),
    html.H3("Regiones"),

    dcc.Dropdown(
        id= 'dd_region',
        multi= True,
        placeholder= 'Regiones',
        options= [dict(label=x, value=x) for x in trd.CONJ.unique()]),

    dcc.Graph(id = 'map')

])

###################################################
# CallBacks
###################################################
@app.callback(
    Output(component_id='map', component_property='figure'),
    [Input(component_id='dd_region', component_property='value')]
)
def update_map(region):
    print(region)

    if region:
        print(region)

        map_data = [
            go.Scattermapbox(
                lat= trd[trd.CONJ.isin(region)].lat,
                lon= trd[trd.CONJ.isin(region)].lon,
                mode='markers'
            )]
    else:
        map_data = [
            go.Scattermapbox(
                lat= [],
                lon= [],
                mode='markers'
            )
        ]

    return dict(data=map_data, layout=map_layout)


#####################################################
if __name__ == '__main__':
    app.run_server(debug=True)