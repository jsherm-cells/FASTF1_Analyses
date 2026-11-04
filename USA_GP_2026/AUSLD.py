import pandas as pd 
import plotly.express as px
import fastf1
import fastf1.plotting
import streamlit as st
fastf1.plotting.setup_mpl(color_scheme='fastf1')


race = fastf1.get_session(2026, 'United States Grand Prix', 'R')
race.load()

driver_colors = fastf1.plotting.get_driver_color_mapping(session=race)
compound_colors = fastf1.plotting.get_compound_mapping(session=race)

top_5 = race.results.sort_values('Position').head(5)['Abbreviation'].tolist()
print(top_5)

laps = race.laps.pick_drivers(top_5).pick_quicklaps()[['Driver', 'LapNumber', 'LapTime']].copy()
laps['LapTimeSeconds'] = laps['LapTime'].dt.total_seconds()
lapsdf = pd.DataFrame(laps.dropna(subset=['LapTimeSeconds']))

dash_map = {'HAM' : 'dot'}

fig1 = px.line(
    lapsdf,
    x='LapNumber',
    y='LapTimeSeconds',
    color='Driver',
    category_orders={'Driver' : top_5},
    line_dash='Driver',
    line_dash_map=dash_map,
    color_discrete_map=driver_colors,
    title='Lap Times Across Race: Top 5 Finishers',
    labels={'LapNumber': 'Lap', 'LapTimeSeconds': 'Lap Time (seconds)'},
    template='plotly_dark'
)

compounds = race.laps[['Driver', 'LapNumber', 'Compound']]
lapsdf = lapsdf.merge(compounds, on=['Driver', 'LapNumber'], how='left')

violin = px.violin(
    lapsdf,
    x='Driver',
    y='LapTimeSeconds',
    color='Driver',
    category_orders={'Driver' : top_5},
    color_discrete_map=driver_colors,
    points=False,
    violinmode='overlay',
    title='Lap Time Distrobution on Tyre Compound',
    labels={'LapTimeSeconds': 'Lap Time (s)', 'Driver': 'Driver'},
    template='plotly_dark'
)
violin.update_traces(showlegend=False)

dots = px.strip(
    lapsdf,
    x='Driver',
    y='LapTimeSeconds',
    color='Compound',
    category_orders={'Driver' : top_5},
    stripmode='overlay',
    color_discrete_map=compound_colors,
    template = 'plotly_dark'
)
dots.update_traces(jitter=0.6, marker_size=5)

violin.add_traces(dots.data)
violin.update_layout(boxmode='overlay', legend_title_text='Compound')


position = []
for driver in top_5:
    driver_pos = race.laps.pick_drivers(driver).pick_quicklaps()

    for _, pos in driver_pos.iterlaps():
        position.append({
        'Driver': driver,
        'LapNumber': pos['LapNumber'],
        'Position': pos['Position']
    })

posdf = pd.DataFrame(position)
lapsdf = lapsdf.merge(posdf, on=['Driver', 'LapNumber'], how='left')

dash_map = {'HAM': 'dot'}

RacePosition = px.line(
    lapsdf,
    x='LapNumber',
    y='Position',
    color='Driver',
    line_dash='Driver',
    line_dash_map=dash_map,
    color_discrete_map=driver_colors,
    title='Position Changes',
    labels={'LapNumber': 'Lap', 'Position': 'Position'},
    template='plotly_dark'
)
RacePosition.update_yaxes(autorange='reversed')


stints = (
    pd.DataFrame(race.laps.pick_drivers(top_5))
    .groupby(['Driver', 'Stint', 'Compound'], as_index=False)
    .agg(StartLap=('LapNumber', 'min'), EndLap=('LapNumber', 'max'))
    )
stints['StintLength'] = stints['EndLap'] - stints['StartLap'] + 1
stints['BarStart'] = stints['StartLap'] - 1

strat = px.bar(
    stints,
    x='StintLength',
    y='Driver',
    base='BarStart',
    orientation='h',
    color='Compound',
    category_orders={'Driver' : top_5},
    barmode='overlay',
    color_discrete_map=compound_colors,
    template='plotly_dark',
    title='Strategies',
    labels={'StintLength': 'Lap'},
    hover_data=['StartLap', 'EndLap']
)

st.set_page_config(layout='wide')
st.title('2026 United States Grand Prix Top 5 Finishers Analysis')
st.header('By: Jake Sherman')
st.write('A dive into the top 5 finishers of the grand prix, highlighting the strategies and skills that brought them there')
col1, col2 = st.columns([5,5])
with col1:
    st.plotly_chart(fig1, width='stretch')
with col2:
    st.plotly_chart(violin, width='stretch')
col3,col4 = st.columns([5,5])
with col3:
    st.plotly_chart(heatspeed, width='stretch')
with col4:
    st.plotly_chart(strat, width='stretch')