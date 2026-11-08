import pandas as pd
import plotly.express as px
import fastf1
import fastf1.plotting
import streamlit as st

prac = fastf1.get_session(2026, 'Brazil', 'FP1')
prac.load()

fastf1.plotting.setup_mpl(color_scheme='fastf1')
driver_colors = fastf1.plotting.get_driver_color_mapping(session=prac)
compound_color = fastf1.plotting.get_driver_color_mapping(session=prac)

rookiesNOR = prac.laps.pick_drivers(['NOR', 'SLA', 'BEG', 'CAM', 'BRO', 'MIN'])
rookiesNOR['LapTimeSeconds'] = rookiesNOR['LapTime'].dt.total_seconds()
rookiesNOR.dropna(subset=['LapTimeSeconds'])

violin = px.violin(
    rookiesNOR,
    x='Driver',
    y='LapTimeSeconds',
    color = 'Driver',
    color_discrete_map=driver_colors,
    points=False,
    violinmode='overlay',
    title = 'Lap Distrobution on Tyre Compound',
    labels = {'LapTimeSeconds' : 'Lap Time (s)', 'Driver' : 'Driver'},
    template = 'plotly_dark'
)

dots = px.strip(
    rookiesNOR,
    x='Driver',
    y='LapTimeSeconds',
    color='Compound',
    color_discrete_map=compound_color,
    stripmode='overlay',
    template='plotly_dark',
)
dots.update_traces(jitter=0.6, marker_size=5)

violin.add_traces(dots.data)
violin.update_layout(boxmode='overlay', legend_title_text='Compound')

drivers = ['NOR', 'BEG', 'BRO', 'CAM', 'MIN', 'SLA']

laps = prac.laps.pick_drivers(drivers).pick_wo_box().copy()
laps['LapTimeSec'] = laps['LapTime'].dt.total_seconds()
laps = laps.dropna(subset=["LapTimeSec", 'TyreLife'])

best = laps.loc[laps.groupby('Driver')['TyreLife'].idxmax(), ['Driver', 'Stint']]
long_runs = laps.merge(best, on=['Driver', 'Stint'])

long = px.line(
    long_runs,
    x='TyreLife',
    y='LapTimeSec',
    color='Driver',
    markers=True,
    hover_data=['Compound', 'Stint', 'LapNumber'],
    title='Long Runs',
    labels={'TyreLife': 'Tyre Life (laps)', 'LapTimeSec' : 'Lap Time (s)'},
    color_discrete_map=driver_colors,
    template='plotly_dark'

)

st.set_page_config(layout='wide')
st.title('Rookie Performance vs Top Performer: FP1 Brasil')
st.header('By: Jake Sherman')
st.write('How the rookie(s) held up against the top performer at FP1 in Brasil')

st.plotly_chart(violin, use_container_width=True)
st.plotly_chart(long, use_container_width=True)