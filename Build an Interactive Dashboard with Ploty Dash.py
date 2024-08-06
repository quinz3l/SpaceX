# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv(r"C:\Users\ASUS\Pictures\Coursera\Capstone\spacex_launch_dash.csv")
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
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Div(["Launch Site :", 
                                          dcc.Dropdown(id='site-dropdown', 
                                                       options=[{'label':'All Sites', 'value':'ALL'},
                                                                {'label':'CCAFS LC-40', 'value':'CCAFS_LC_40'},
                                                                {'label':'VAFB SLC-4E', 'value':'VAFB_SLC_4E'},
                                                                {'label':'KSC LC-39A', 'value':'KSC_LC_39A'},
                                                                {'label':'CCAFS SLC-40', 'value':'CCAFS_SLC_40'}],
                                                       value='ALL',
                                                       placeholder='Select a Launch Site here',
                                                       searchable=True)]),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Div(dcc.RangeSlider(id='payload-slider',
                                                         min=0,
                                                         max=10000,
                                                         step=1000,
                                                         marks={0:'0',
                                                                1000:'1000', 
                                                                2000:'2000',
                                                                3000:'3000', 
                                                                4000:'4000',
                                                                5000:'5000',
                                                                6000:'6000',
                                                                7000:'7000',
                                                                8000:'8000',
                                                                9000:'9000', 
                                                                10000:'10000'},
                                                         value=[min_payload, max_payload])),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)

def get_pie_chart(entered_site_dropdown):
    counts = spacex_df.groupby(['Launch Site', 'class']).size().unstack(fill_value=0).reset_index()
    
    if entered_site_dropdown == 'ALL':
        figure = px.pie(counts,
                        values=1,
                        names='Launch Site',
                        title = "Total Success Launched by Site")
        
        return figure
    
    if entered_site_dropdown == 'CCAFS_LC_40':
        df_new = spacex_df[spacex_df['Launch Site']=='CCAFS LC-40']
        class_counts = df_new['class'].value_counts(normalize=True) * 100
        class_counts_df = class_counts.reset_index()
        class_counts_df.columns = ['Class', 'Percentage']
        class_counts_df.iloc[0,0] = 'Success'
        class_counts_df.iloc[1,0] = 'Failure'
        figure = px.pie(class_counts_df,
                        values='Percentage',
                        names='Class',
                        title = f"Launch Site Success and Failure for {entered_site_dropdown}")
        
        return figure
    
    if entered_site_dropdown == 'VAFB_SLC_4E':
        df_new = spacex_df[spacex_df['Launch Site']=='VAFB SLC-4E']
        class_counts = df_new['class'].value_counts(normalize=True) * 100
        class_counts_df = class_counts.reset_index()
        class_counts_df.columns = ['Class', 'Percentage']
        class_counts_df.iloc[0,0] = 'Success'
        class_counts_df.iloc[1,0] = 'Failure'
        figure = px.pie(class_counts_df,
                        values='Percentage',
                        names='Class',
                        title = f"Launch Site Success and Failure for {entered_site_dropdown}")
        
        return figure
    
    if entered_site_dropdown == 'KSC_LC_39A':
        df_new = spacex_df[spacex_df['Launch Site']=='KSC LC-39A']
        class_counts = df_new['class'].value_counts(normalize=True) * 100
        class_counts_df = class_counts.reset_index()
        class_counts_df.columns = ['Class', 'Percentage']
        class_counts_df.iloc[0,0] = 'Success'
        class_counts_df.iloc[1,0] = 'Failure'
        figure = px.pie(class_counts_df,
                        values='Percentage',
                        names='Class',
                        title = f"Launch Site Success and Failure for {entered_site_dropdown}")
        
        return figure
    
    if entered_site_dropdown == 'CCAFS_SLC_40':
        df_new = spacex_df[spacex_df['Launch Site']=='CCAFS SLC-40']
        class_counts = df_new['class'].value_counts(normalize=True) * 100
        class_counts_df = class_counts.reset_index()
        class_counts_df.columns = ['Class', 'Percentage']
        class_counts_df.iloc[0,0] = 'Success'
        class_counts_df.iloc[1,0] = 'Failure'
        figure = px.pie(class_counts_df,
                        values='Percentage',
                        names='Class',
                        title = f"Launch Site Success and Failure for {entered_site_dropdown}")
        
        return figure

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
    )

def get_scatter_chart(entered_site_dropdown, entered_payload_slider):
    if entered_site_dropdown == 'ALL':
        df_payload = spacex_df[spacex_df['Payload Mass (kg)'] >= entered_payload_slider[0]]
        df_payload = df_payload[df_payload['Payload Mass (kg)'] <= entered_payload_slider[1]]
        fig = px.scatter(df_payload, 
                         x='Payload Mass (kg)', 
                         y='class',
                         color='Booster Version Category',
                         title='Correlation Between Payload Mass and Class')
        
        return fig
    
    if entered_site_dropdown == 'CCAFS_LC_40':
        df_payload = spacex_df[spacex_df['Payload Mass (kg)'] >= entered_payload_slider[0]]
        df_payload = df_payload[df_payload['Payload Mass (kg)'] <= entered_payload_slider[1]]
        df_payload = df_payload[df_payload['Launch Site'] == 'CCAFS LC-40']
        fig = px.scatter(df_payload, 
                         x='Payload Mass (kg)', 
                         y='class',
                         color='Booster Version Category',
                         title=f'Correlation Between Payload Mass and Class on {entered_site_dropdown}')
        
        return fig

    if entered_site_dropdown == 'VAFB_SLC_4E':
        df_payload = spacex_df[spacex_df['Payload Mass (kg)'] >= entered_payload_slider[0]]
        df_payload = df_payload[df_payload['Payload Mass (kg)'] <= entered_payload_slider[1]]
        df_payload = df_payload[df_payload['Launch Site'] == 'VAFB SLC-4E']
        fig = px.scatter(df_payload, 
                         x='Payload Mass (kg)', 
                         y='class',
                         color='Booster Version Category',
                         title=f'Correlation Between Payload Mass and Class on {entered_site_dropdown}')
        
        return fig
    
    if entered_site_dropdown == 'KSC_LC_39A':
        df_payload = spacex_df[spacex_df['Payload Mass (kg)'] >= entered_payload_slider[0]]
        df_payload = df_payload[df_payload['Payload Mass (kg)'] <= entered_payload_slider[1]]
        df_payload = df_payload[df_payload['Launch Site'] == 'KSC LC-39A']
        fig = px.scatter(df_payload, 
                         x='Payload Mass (kg)', 
                         y='class',
                         color='Booster Version Category',
                         title=f'Correlation Between Payload Mass and Class on {entered_site_dropdown}')
        
        return fig
    
    if entered_site_dropdown == 'CCAFS_SLC_40':
        df_payload = spacex_df[spacex_df['Payload Mass (kg)'] >= entered_payload_slider[0]]
        df_payload = df_payload[df_payload['Payload Mass (kg)'] <= entered_payload_slider[1]]
        df_payload = df_payload[df_payload['Launch Site'] == 'CCAFS SLC-40']
        fig = px.scatter(df_payload, 
                         x='Payload Mass (kg)', 
                         y='class',
                         color='Booster Version Category',
                         title=f'Correlation Between Payload Mass and Class on {entered_site_dropdown}')
        
        return fig
# Run the app
if __name__ == '__main__':
    app.run_server()