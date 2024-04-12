# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 09:52:31 2024

@author: dearde
"""
import plotly.graph_objects as go
import pandas as pd

# Create a data frame with the provided data
df = pd.DataFrame({
    'Country': ["GBR", "FRA", "DEU", "ITA", "JPN", "USA", "CAN", "DNK", "POL", "SVN"],
    'CP_2019_2021': [20.7, 19.9, 15.5, 25.5, 14.8, 26.2, 17.2, 9.9, 14.1, 10],
    'CP_2012_2014': [17.3, 18, 14.8, 25.7, 18.2, 28.1, 22.3, 9.6, 22.6, 14.6],
    'Fill_Color': ["#b2182b", "#3f366d", "#3f366d", "#3f366d", "#3f366d", "#3f366d", "#3f366d", "#3f366d", "#3f366d", "#3f366d"]
})

# Calculate percentage point change
df['Change'] = df['CP_2019_2021'] - df['CP_2012_2014']

# Sort the DataFrame by CP_2019_2021 in ascending order
df = df.sort_values(by='CP_2019_2021')

# Create traces
trace1 = go.Bar(x=df['Country'], y=df['CP_2019_2021'], marker=dict(color=df['Fill_Color']), name='2019-2021')
trace2 = go.Scatter(x=df['Country'], y=df['CP_2012_2014'], mode='markers', marker=dict(color='orange', size=10), name='2012-2014')

annotations = []
annotations_base = []

for i, country in enumerate(df['Country']):
    annotations.append(dict(
        x=country,
        y=df['CP_2012_2014'].iloc[i] + 1,
        xref='x',
        yref='y',
        text= df['CP_2012_2014'].iloc[i],
        textangle=0,
        font=dict(
            color="orange",
            size=12
        ),
        bordercolor="orange",
        borderwidth=2,
        borderpad=4,
        bgcolor="white",
        opacity=0.7,
        xanchor='center',  # Anchor text to the center
        showarrow=False  # Remove arrow
    ))
    
    # Add annotations for CP_2019_2021 at the base of each bar
    annotations_base.append(dict(
        x=country,
        y= 1,  # Adjust y position
        xref='x',
        yref='y',
        text= df['CP_2019_2021'].iloc[i],  # Use CP_2019_2021 for text
        textangle=0,
        font=dict(
            color="black",  # Set font color to black
            size=12
        ),
        bgcolor="rgba(255, 255, 255, 0.7)",  # Opaque white box
        showarrow=False  # Remove arrow
    ))

# Create shape traces for connecting lines
lines = []
for i, country in enumerate(df['Country']):
    lines.append(go.layout.Shape(
        type="line",
        x0=country,
        y0=df['CP_2012_2014'].iloc[i],
        x1=country,
        y1=df['CP_2019_2021'].iloc[i],
        line=dict(
            color="orange",
            width=2,
            dash="dot"
        )
    ))

# Create layout
layout = go.Layout(
    title="Child Poverty Rate (2019-2021) with Comparison to 2012-2014",
    xaxis=dict(title='Country', showgrid=False),
    yaxis=dict(title='Child Poverty Rate (%)', range=[0, 30], dtick=5, showgrid=True, gridwidth=1, gridcolor='lightgrey'),
    legend=dict(title='Child poverty (%)'),
    plot_bgcolor='white',
    font=dict(family="Open Sans")
)

# Create figure
fig = go.Figure(data=[trace1, trace2], layout=layout)

# Add annotations
for annotation in annotations:
    fig.add_annotation(**annotation)

# Add annotations for CP_2019_2021 at the base of each bar
for annotation_base in annotations_base:
    fig.add_annotation(**annotation_base)

# Add shape traces for connecting lines
for line in lines:
    fig.add_shape(line)

# Show figure
fig.show(renderer="browser")
