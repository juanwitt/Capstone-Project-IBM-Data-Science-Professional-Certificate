# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                        options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},],
                                        #value='ALL',
                                        placeholder="Choose Location",
                                        searchable=True
                                        ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div([
                                    html.Div(dcc.Graph(id='success-pie-chart')),
                                ]),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                    100: '100'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                                ])

# TASK 2:
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='title')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        filtered_df.index = np.arange(len(filtered_df))
        dz = filtered_df.groupby('Launch Site')
        value = [dz['class'].mean()[0], 1-dz['class'].mean()[0]]
        #value = [0.7, 0.3]
        fig = px.pie(values= value, 
                    names=['Success','Failure'], 
                    title='title')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id='payload-slider', component_property='value'))


def get_scatter_plot(entered_site, payload):
    payload_df = spacex_df
    if entered_site == 'ALL':   
        payload_df2 = payload_df.sort_values('Payload Mass (kg)')
        payload_df1 = payload_df2[payload[0] < payload_df['Payload Mass (kg)']]
        payload_df3 = payload_df1[payload[1] > payload_df['Payload Mass (kg)']]
        payload_df3.index = np.arange(len(payload_df3))    
        fig = px.scatter(payload_df3 ,x = 'Payload Mass (kg)', y = 'class',color="Booster Version Category")
        return fig
    else:
        payload_df2 = spacex_df[spacex_df['Launch Site'] == entered_site]
        payload_df2 = payload_df2.sort_values('Payload Mass (kg)')
        payload_df1 = payload_df2[payload[0] < payload_df['Payload Mass (kg)']]
        payload_df3 = payload_df1[payload[1] > payload_df['Payload Mass (kg)']]
        payload_df3.index = np.arange(len(payload_df3))
 
        
        fig = px.scatter(payload_df3 ,x = 'Payload Mass (kg)', y = 'class',color="Booster Version Category")
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
