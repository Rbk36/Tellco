# Import necessary libraries
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Assuming df_xdr is your DataFrame with relevant data
df_xdr = pd.DataFrame({'Handset Type''Throughput (Bps)'})

# Aggregate data for plotting
throughput_per_handset = df_xdr.groupby('Handset Type').agg({'Throughput (Bps)': 'mean'}).reset_index()
top_handsets = df_xdr['Handset Type'].value_counts().head(10).reset_index()
top_handsets.columns = ['Handset Type', 'Count']

# Initialize Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1('Telecom Data Insights Dashboard', style={'textAlign': 'center', 'color': '#1f77b4'}),

    html.Div([
        html.H2('Average Throughput by Handset Type', style={'marginBottom': '0'}),
        dcc.Graph(
            id='throughput-handset',
            figure=px.bar(
                throughput_per_handset,
                x='Handset Type',
                y='Throughput (Bps)',
                title='Average Throughput by Handset Type',
                labels={'Handset Type': 'Handset Type', 'Throughput (Bps)': 'Average Throughput (Bps)'}
            ).update_layout(
                xaxis_title='Handset Type',
                yaxis_title='Average Throughput (Bps)',
                xaxis_tickangle=-45,
                title_font_size=20,
                xaxis_title_font_size=14,
                yaxis_title_font_size=14
            )
        )
    ], style={'padding': '10px'}),

    html.Div([
        html.H2('Top 10 Handsets Used by Customers', style={'marginBottom': '0'}),
        dcc.Graph(
            id='top-handsets',
            figure=px.bar(
                top_handsets,
                x='Handset Type',
                y='Count',
                title='Top 10 Handsets Used by Customers',
                labels={'Handset Type': 'Handset Type', 'Count': 'Count'}
            ).update_layout(
                xaxis_title='Handset Type',
                yaxis_title='Count',
                xaxis_tickangle=-45,
                title_font_size=20,
                xaxis_title_font_size=14,
                yaxis_title_font_size=14
            )
        )
    ], style={'padding': '10px'}),

    html.Div([
        html.H2('Interactive Elements', style={'marginBottom': '0'}),
        html.Label('Select Handset Type:', style={'fontSize': '16px'}),
        dcc.Dropdown(
            id='handset-dropdown',
            options=[{'label': i, 'value': i} for i in throughput_per_handset['Handset Type']],
            value=throughput_per_handset['Handset Type'].iloc[0],
            style={'width': '50%'}
        ),
        dcc.Graph(id='selected-handset-throughput')
    ], style={'padding': '10px'})
])

# Define callback to update graph based on dropdown selection
@app.callback(
    Output('selected-handset-throughput', 'figure'),
    [Input('handset-dropdown', 'value')]
)
def update_graph(selected_handset):
    filtered_df = throughput_per_handset[throughput_per_handset['Handset Type'] == selected_handset]
    return px.bar(
        filtered_df,
        x='Handset Type',
        y='Throughput (Bps)',
        title=f'Average Throughput for {selected_handset}',
        labels={'Handset Type': 'Handset Type', 'Throughput (Bps)': 'Average Throughput (Bps)'}
    ).update_layout(
        xaxis_title='Handset Type',
        yaxis_title='Average Throughput (Bps)',
        title_font_size=20,
        xaxis_title_font_size=14,
        yaxis_title_font_size=14
    )

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
