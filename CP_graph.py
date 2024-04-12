# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 12:18:40 2024
@author: dearde

"""
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

df = pd.DataFrame({
    'Country': ["GBR", "FRA", "DEU", "ITA", "JPN", "USA", "CAN", "DNK", "POL", "SVN"],
    'CP_2019_2021': [20.7, 19.9, 15.5, 25.5, 14.8, 26.2, 17.2, 9.9, 14.1, 10],
    'CP_2012_2014': [17.3, 18, 14.8, 25.7, 18.2, 28.1, 22.3, 9.6, 22.6, 14.6]
})

df = df.sort_values(by='CP_2019_2021', ascending=False).reset_index(drop=True)
df['Change'] = df['CP_2019_2021'] - df['CP_2012_2014']
df[['CP_2019_2021', 'CP_2012_2014', 'Change']] = df[['CP_2019_2021', 'CP_2012_2014', 'Change']].applymap(lambda x: round(x, 1))
df['arrow'] = df.apply(lambda row: row['CP_2019_2021'] - 0.4 if row['Change'] > 0 else row['CP_2019_2021'] + 0.4, axis=1)

traces = []
annotations = []
for index, row in df[~df['Country'].isin(['ITA', 'DNK'])].iterrows():
    if row['Change'] != 0:
        symbol = 'triangle-right' if row['Change'] > 0 else 'triangle-left'
        line_trace = go.Scatter(
            x=[row['CP_2012_2014'], row['arrow']],
            y=[row['Country'], row['Country']],
            mode='lines+markers',
            marker=dict(color=['grey', 'black'], size=[17, 8], symbol=['circle', symbol], opacity=1, line=dict(color="grey")),
            line=dict(color='black', width=1),
            showlegend=False
        )
        traces.append(line_trace)

        text = f"{row['Change']:+.1f}"
        font_color = 'red' if row['Change'] > 0 else '#393939'
        annotation = dict(
            x=row['CP_2019_2021'] + 0.8 if row['Change'] > 0 else row['CP_2012_2014'] + 0.8,
            y=row['Country'],
            text=text,
            showarrow=False,
            font=dict(color=font_color, size=18)
        )
        annotations.append(annotation)

fig = go.Figure(data=[
    go.Scatter(x=df['CP_2019_2021'], y=df['Country'], mode='markers', name='2019-2021', marker=dict(color='#3f366d', size=17)),
    go.Scatter(x=df['CP_2012_2014'], y=df['Country'], mode='markers', name='2012-2014', marker=dict(color='#7f7f7f', size=17), legendgroup="group2")
] + traces)

fig.update_layout(
    annotations=annotations,
    title='Child poverty rate (2019-2021, 2012-2014)',
    xaxis=dict(title='Child poverty rate (%)', tickvals=list(range(0, 31, 5)), showgrid=True, gridcolor='lightgray'),
    yaxis=dict(title='Country', tickfont=dict(size=18), dtick=1),
    plot_bgcolor='white',
    font=dict(family='Open Sans', size=18, color='#393939'),
    height=600
)

pio.show(fig, renderer='browser')