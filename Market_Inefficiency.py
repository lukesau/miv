# Import necessary libraries
import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objects as go
import numpy as np


default_shape = 'star'
colors = {
    'QB': '#9647b8',
    'RB': '#15997e',
    'WR': '#e67e22',
    'TE': '#2980b9',
}

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))

def interp_color(low_rgb, high_rgb, interp_value):
    return tuple(np.array(low_rgb) + interp_value * (np.array(high_rgb) - np.array(low_rgb)))

# Load CSV data
file_path = r'ValueChart.csv'
data = pd.read_csv(file_path)
# Remove '%' symbol and convert DELTA % to numeric
data['DELTA %'] = data['DELTA %'].str.rstrip('%').astype(float)

# Convert 'DELTA %' column to numeric values
data['DELTA %'] = pd.to_numeric(data['DELTA %'], errors='coerce')

# Sort by ADP
data = data.sort_values('ADP')

min_delta = data['DELTA %'].min()
max_delta = data['DELTA %'].max()

# Filter out rows with missing POSITION values
data = data.dropna(subset=['POSITION'])

# Define shapes for positions
shapes = {'QB': 'circle', 'WR': 'square', 'RB': 'diamond', 'TE': 'cross'}

# Define a function to get the appropriate x and y coordinates for the scatter plot
def get_scatter_location(index):
    y = (index // 12) * 2 + 1
    x = (index % 12) + 1
    return x, y

# Add x and y columns to the DataFrame for scatter plot coordinates
data['x'] = [get_scatter_location(index)[0] for index in range(len(data))]
data['y'] = [get_scatter_location(index)[1] for index in range(len(data))]

colors = ['#ff0000', '#ff6666', '#b3b3b3', '#66ff66', '#00cc00']

def get_color(delta):
    if delta <= -8:
        return colors[0]
    elif -8 < delta <= -4:
        return colors[1]
    elif -4 < delta < 4:
        return colors[2]
    elif 4 <= delta < 8:
        return colors[3]
    else:
        return colors[4]

# Create a scatter plot using Plotly Express
fig = go.Figure()

# Set to keep track of positions added to the legend
positions_in_legend = set()

for index, row in data.iterrows():
    adp = row['ADP']
    delta = row['DELTA %']
    position = row['POSITION']
    x, y = get_scatter_location(index)
    shape = shapes.get(position, default_shape)

    if pd.isna(delta):
        color = 'gray'
    else:
        color = get_color(delta)



    show_legend = position not in positions_in_legend
    positions_in_legend.add(position)

    fig.add_trace(go.Scatter(x=[x], y=[y],
                             mode='markers',
                             marker=dict(size=10,
                                         symbol=shape,
                                         color=color,
                                         line=dict(width=1, color='black')),
                             showlegend=show_legend,
                             name=position,
                             hovertext=f'ADP: {adp}, DELTA %: {delta}, POSITION: {position}'))

# Invert the y-axis range
fig.update_yaxes(autorange='reversed')

fig.update_layout(title_text='Market Inefficiency Finder',
                  coloraxis_colorbar=dict(title='DELTA %'),
                  xaxis=dict(tickvals=list(range(1, 13)), ticktext=[f'Col {i}' for i in range(1, 13)]),
                  yaxis=dict(tickvals=list(range(1, 37, 2)), ticktext=[f'Round {i}' for i in range(1, 19)]))
fig.update_layout(autosize=True)




# Initialize your Dash app
app = dash.Dash(__name__)

# Define the layout of your app
app.layout = html.Div([
    dcc.Graph(
        id='my-plotly-graph',
        figure=fig,  # Assuming 'fig' is your Plotly figure object,
        style={'flex': '1'}
    ),
    # You can add more web elements here as needed
], style={'display': 'flex', 'alignItems': 'stretch', 'width': '100%', 'height': '100vh'})
