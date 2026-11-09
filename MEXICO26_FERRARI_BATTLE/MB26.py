import fastf1
import fastf1.plotting
import pandas as pd
import plotly.express as px
import streamlit as st

battle = fastf1.get_session(2026, 'Mexico', 'R')
battle.load()

lecl1 = battle.laps.pick_drivers('LEC').pick_laps(1)
haml1 = battle.laps.pick_drivers('HAM').pick_laps(1)

lecl1 = lecl1.get_car_data().add_distance()
haml1 = haml1.get_car_data().add_distance()

track = battle.get_circuit_info().corners

speed = 'Speed'
telem = pd.concat([
    lecl1[['Distance', speed]].assign(Driver='LEC'),
    haml1[['Distance', speed]].assign(Driver='HAM'),
], ignore_index=True)

speed = px.line(
    telem,
    x='Distance',
    y=speed,
    color='Driver',
    template='plotly_dark'
)


for _, corner in track.iterrows():
    speed.add_vline(
        x=corner['Distance'],
        line_dash='dash',
        line_color='gray',
        line_width=1,
        annotation_text=f"{corner['Number']}{corner['Letter']}",
        annotation_position='top',
        annotation_font_size=10
    )
   
speed.update_layout(hovermode='x unified')

throttle = 'Throttle'
telem2 = pd.concat([
    lecl1[['Distance', throttle]].assign(Driver='LEC'),
    haml1[['Distance', throttle]].assign(Driver='HAM')
], ignore_index=True)

throttle = px.line(
    telem2,
    x='Distance',
    y=throttle,
    color='Driver',
    template='plotly_dark'
)


for _, corner in track.iterrows():
    throttle.add_vline(
        x=corner['Distance'],
        line_dash='dash',
        line_color='gray',
        line_width=1,
        annotation_text=f"{corner['Number']}{corner['Letter']}",
        annotation_font_size=10,
        annotation_position='top'
    )
throttle.update_layout(hovermode='x unified')


brake = 'Brake'

telem3 = pd.concat([
    lecl1[['Distance', brake]].assign(Driver='LEC'),
    haml1[['Distance', brake]].assign(Driver='HAM'),
], ignore_index=True)


brake = px.line(
    telem3,
    x='Distance',
    y=brake,
    color='Driver',
    template='plotly_dark'
)

for _, corner in track.iterrows():
    brake.add_vline(
    x=corner['Distance'],
    line_dash='dash',
    line_width=1,
    line_color='gray',
    annotation_text=f"{corner['Number']}{corner['Letter']}",
    annotation_font_size=10,
    annotation_position='top'
)
brake.update_layout(hovermode='x unified')

telem4 = pd.concat([
    lecl1[['Distance', 'nGear']].assign(Driver='LEC'),
    haml1[['Distance', 'nGear']].assign(Driver='HAM')
], ignore_index=True)

gear = px.line(
    telem4,
    x='Distance',
    y='nGear',
    color='Driver',
    template='plotly_dark'
)

for _, corner in track.iterrows():
    gear.add_vline(
        x=corner['Distance'],
        line_dash='dash',
        line_color='gray',
        line_width=1,
        annotation_text=f"{corner['Number']}{corner['Letter']}",
        annotation_position='top',
        annotation_font_size=10
    )
gear.update_layout(hovermode='x unified')

st.set_page_config(layout='wide')
st.title('Ferrari First Lap Battle Analysis')
st.header('By: Jake Sherman')
st.write('An analysis of a pivotal and contreversial battle for The Scuderia')

st.plotly_chart(speed, use_container_width=True)
st.plotly_chart(throttle, use_container_width=True)
st.plotly_chart(brake, use_container_width=True)
st.plotly_chart(gear, use_container_width=True)