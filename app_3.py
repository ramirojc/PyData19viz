import dash
import dash_core_components as dcc
import dash_html_components as html

from plotly import graph_objs as go

import pandas as pd

mapbox_access_token = 'pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w'

#################################
trd = pd.read_csv('./data/UNI_TRD_ENF17.csv')
print(trd.CONJ.unique())


app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([

    html.H1("Mapa de distribucion Electrica"),
    html.H3("Seleccione Regiones"),

    dcc.Dropdown(
        id= 'dd_region',
        multi= True,
        options= [dict(label=x, value=x) for x in trd.CONJ.unique()]),

    dcc.Graph(
        id = 'map',
        figure = go.Figure(
            data=[
                go.Scattermapbox(
                    lat= trd.lat,
                    lon= trd.lon,
                    text=['Universidad Tecnologica Nacional'],
                    mode='markers',
                    name='UTN')
            ],
            layout= go.Layout(
                mapbox= go.layout.Mapbox(
                    accesstoken= mapbox_access_token,
                    center= dict(lat=trd.lat[0], lon=trd.lon[0]),
                    zoom=10,
                    pitch=45,
                    style='light'),
                margin= dict(l=10,t=10,b=10,r=10)
            )
        )
    )

])

if __name__ == '__main__':
    app.run_server(debug=True)