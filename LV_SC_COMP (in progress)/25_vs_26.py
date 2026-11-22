import fastf1
import fastf1.plotting
import plotly.express as px
import pandas as pd
import streamlit as st


# 2025 Qualifying Session

q25 = fastf1.get_session(2025, 'Las Vegas', 'Q')
q25.load()

fastf1.plotting.setup_mpl(color_scheme='fastf1')
driver_colors = fastf1.plotting.get_driver_color_mapping(session=q25)

q1, q2, q3 = q25.laps.split_qualifying_sessions()


drivers = ['NOR', 'VER', 'SAI', 'RUS', 'PIA', 'LAW', 'ALO', 'HAD', 'LEC', 'GAS']

q_results = []
for abb in drivers:
    q3_drive_25 = q3.pick_drivers(abb).pick_fastest()
    q_results.append(q3_drive_25) 


q_tele = []
for lap in q_results:
    q3_tele_25 = lap.get_car_data().add_distance().assign(Driver=lap['Driver'])
    q_tele.append(q3_tele_25)

    distance = []
for dist in q_tele:
    mask = (dist['Distance'] >= 3200) & (dist['Distance'] <=5300)
    dist = dist.loc[mask, ['Throttle', 'Brake', 'Distance','Speed', 'nGear', 'RPM', 'DRS', 'Time', 'Driver']].copy()
    dist['TimeSeconds'] = dist['Time'].dt.total_seconds()
    distance.append(dist)

q25_tele = pd.concat(distance, ignore_index=True)
q25_tele['Year'] = 2025

q25_tele['Speed_ms'] = q25_tele['Speed'] / 3.6

deltav = q25_tele.groupby('Driver')['Speed_ms'].diff().dropna()
deltat = q25_tele.groupby('Driver')['TimeSeconds'].diff().dropna()

a_g = deltav / deltat / 9.81

q25_tele['Longitudinal_Acceleration_g'] = a_g

q25_tele = q25_tele.dropna()

# 2025 Graphs

scat25 = px.scatter(
    q25_tele,
    x='Speed_ms',
    y='Longitudinal_Acceleration_g',
    color='Driver',
    color_discrete_map=driver_colors,
    template='plotly_dark',
    title='Longitudinal Acceleration vs Speed (m/s) - 2025 Las Vegas GP',
    labels={'Speed_ms': 'Speed (m/s)', 'Longitudinal_Acceleration_g': 'Longitudinal Acceleration (g)'},
    trendline='lowess',
    trendline_scope='overall',
)
scat25.update_traces(marker=dict(size=5, opacity=0.7), selector=dict(mode='markers'))

speed25 = px.line(
    q25_tele,
    x='Distance',
    y='Speed',
    color='Driver',
    color_discrete_map=driver_colors,
    template='plotly_dark',
    title='Speed vs Distance (m) - 2025 Las Vegas GP',
    labels={'Distance': 'Distance (m)', 'Speed_ms': 'Speed (m/s)'},
)

throttle25 = px.line(
    q25_tele,
    x='Distance',
    y='Throttle',
    color='Driver',
    color_discrete_map=driver_colors,
    template='plotly_dark',
    title='Throttle vs Distance (m) - 2025 Las Vegas GP',
    labels={'Distance': 'Distance (m)', 'Throttle': 'Throttle'},
)

accel25 = px.line(
    q25_tele,
    x='Distance',
    y='Longitudinal_Acceleration_g',
    color='Driver',
    color_discrete_map=driver_colors,
    template='plotly_dark',
    title='Longitudinal Acceleration vs Distance (m) - 2025 Las Vegas GP',
    labels={'Distance': 'Distance (m)', 'Longitudinal_Acceleration_g': 'Longitudinal Acceleration (g)'},
)

rpm25 = px.line(
    q25_tele,
    x='Distance',
    y='RPM',
    color='Driver',
    color_discrete_map=driver_colors,
    template='plotly_dark',
    title='RPM vs Distance (m) - 2025 Las Vegas GP',
    labels={'Distance': 'Distance (m)', 'RPM': 'RPM'},
)

nGear25 = px.line(
    q25_tele,
    x='Distance',
    y='nGear',
    color='Driver',
    color_discrete_map=driver_colors,
    template='plotly_dark',
    title='Gear vs Distance (m) - 2025 Las Vegas GP',
    labels={'Distance': 'Distance (m)', 'nGear': 'Gear'},
)

# 2026 Qualifying Session

q26 = fastf1.get_session(2026, 'Las Vegas', 'Q')
q26.load()

q1, q2, q3 = q26.laps.split_qualifying_sessions()

top_10 = ['ANT', 'VER', 'RUS', 'NOR', 'HAD', 'LIN', 'PIA', 'LAW', 'GAS', 'COL']

q26_results = []
for res in top_10:
    q3_drive_26 = q3.pick_drivers(res).pick_fastest()
    q26_results.append(q3_drive_26)

q26_tele = []
for tele in q26_results:
    q3_tele_26 = tele.get_car_data().add_distance().assign(top_10=tele['Driver'])
    q26_tele.append(q3_tele_26)

q26_distance = []
for distance in q26_tele:
    mask = (distance['Distance'] >= 3200) & (distance['Distance'] <= 5300)
    distance = distance.loc[mask, ['Throttle', 'Brake', 'Distance', 'Speed', 'nGear', 'RPM', 'Time', 'top_10']].copy()
    distance['TimeSeconds'] = distance['Time'].dt.total_seconds()
    q26_distance.append(distance)

q26_tele = pd.concat(q26_distance, ignore_index=True)

q26_tele['Year'] = 2026

q26_tele['Speed_ms'] = q26_tele['Speed'] / 3.6

deltav_26 = q26_tele.groupby('top_10')['Speed_ms'].diff().dropna()
deltat_26 = q26_tele.groupby('top_10')['TimeSeconds'].diff().dropna()

a_g_26 = deltav_26 / deltat_26 / 9.81

q26_tele['Longitudinal_Acceleration_g'] = a_g_26

q26_tele = q26_tele.dropna()

# 2026 Graphs

scat26 = px.scatter(
    q26_tele,
    x='Speed_ms',
    y='Longitudinal_Acceleration_g',
    color='top_10',
    color_discrete_map=driver_colors,
    template='plotly_dark',
    title='Longitudinal Acceleration vs Speed (m/s) - 2026 Las Vegas GP',
    labels={'Speed_ms': 'Speed (m/s)', 'Longitudinal_Acceleration_g': 'Longitudinal Acceleration (g)'},
    trendline='lowess', 
    trendline_scope='overall'
)
scat26.update_traces(marker=dict(size=5, opacity=0.7), selector=dict(mode='markers'))

speed26 = px.line(
    q26_tele,
    x='Distance',
    y='Speed',
    color='top_10',
    color_discrete_map=driver_colors,
    template='plotly_dark',
    title='Speed vs Distance (m) - 2026 Las Vegas GP',
    labels={'Distance': 'Distance (m)', 'Speed_ms': 'Speed (m/s)'}
)

throttle26 = px.line(
    q26_tele,
    x='Distance',
    y='Throttle',
    color='top_10',
    color_discrete_map=driver_colors,
    template='plotly_dark',
    title='Throttle vs Distance (m) - 2026 Las Vegas GP',
    labels={'Distance': 'Distance (m)', 'Throttle': 'Throttle'},
)
accel26 = px.line(
    q26_tele,
    x='Distance',
    y='Longitudinal_Acceleration_g',
    color='top_10',
    template='plotly_dark',
    title='Longitudinal Acceleration vs Distance (m) - 2025 Las Vegas GP',
    labels={'Distance': 'Distance (m)', 'Longitudinal_Acceleration_g': 'Longitudinal Acceleration (g)'},
)

rpm26 = px.line(
    q26_tele,
    x='Distance',
    y='RPM',
    color='top_10',
    template='plotly_dark',
    title='RPM vs Distance (m) - 2025 Las Vegas GP',
    labels={'Distance': 'Distance (m)', 'RPM': 'RPM'}
)

nGear26 = px.line(
    q26_tele,
    x='Distance',
    y='nGear',
    color='top_10',
    color_discrete_map=driver_colors,
    template='plotly_dark',
    title='Gear vs Distance (m) - 2025 Las Vegas GP',
    labels={'Distance': 'Distance (m)', 'nGear': 'Gear'}
)



st.set_page_config(layout='wide')
st.title('How Is Super Clipping Effecting The Cars on the Las Vegas Strip Straight')
st.header('By: Jake Sherman')

col1, col2 = st.columns([5,5])
with col1:
    st.plotly_chart(scat26, width='stretch')
with col2: 
    st.plotly_chart(scat25, width='stretch')

col3, col4 = st.columns([5,5])
with col3:
    st.plotly_chart(speed26, width='stretch')
with col4: 
    st.plotly_chart(speed25, width='stretch')

col5, col6 = st.columns([5,5])
with col5:
    st.plotly_chart(throttle26, width='stretch')
with col6: 
    st.plotly_chart(throttle25, width='stretch')

col7, col8 = st.columns([5,5])
with col7:
    st.plotly_chart(accel26, width='stretch')
with col8: 
    st.plotly_chart(accel25, width='stretch')

col9, col10 = st.columns([5,5])
with col9:
    st.plotly_chart(rpm26, width='stretch')
with col10: 
    st.plotly_chart(rpm25, width='stretch')    

col11, col12 = st.columns([5,5])
with col11:
    st.plotly_chart(nGear26, width='stretch')
with col12: 
    st.plotly_chart(nGear25, width='stretch')