import fastf1
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier

test = fastf1.get_session(2026, 'Brazil', 'Q')
test.load()

test.laps

BRAZIL = {2018: 20, 2019: 20, 2021: 19, 2022: 21, 2023: 20, 2024: 21, 2025: 21, 2026: 20}
LAP_COLS = ["Driver", "Team", "LapNumber", "LapTime", "Sector1Time", "Sector2Time",
            "Sector3Time", "Compound", "TyreLife", "SpeedST", "Deleted",
            "IsAccurate", "PitOutTime", "PitInTime"]



def tag(df, session, year, rnd):
    df = df.copy()
    df["Year"] = year
    df["Round"] = rnd
    df["Session"] = session.name
    df['EventFormat'] = session.event['EventFormat']
    for col in df.select_dtypes('timedelta').columns:
        df[col] = df[col].dt.total_seconds()
    return df

q_laps, q_results, q_weather, r_results = [], [], [], []
for year, rnd in BRAZIL.items():
    quali = fastf1.get_session(year, rnd, 'Q')
    quali.load(telemetry=False)
    q_laps.append(tag(quali.laps[LAP_COLS], quali, year, rnd))
    q_results.append(tag(quali.results, quali, year, rnd,))
    q_weather.append(tag(quali.weather_data, quali, year, rnd))

    if year < 2026:
        race = fastf1.get_session(year, rnd, 'R')
        race.load(laps=False, weather=False, telemetry=False, messages=False)
        r_results.append(tag(race.results, race, year, rnd))

q_laps = pd.concat(q_laps, ignore_index=True)
q_results = pd.concat(q_results, ignore_index=True)
q_weather = pd.concat(q_weather, ignore_index=True)
r_results = pd.concat(r_results, ignore_index=True)


res = q_results.copy()
for seg in ['Q1', 'Q2', 'Q3']:
    fastest = res.groupby('Year')[seg].transform('min')
    res[f"{seg}_gap_pct"] = (res[seg] - fastest) / fastest * 100

res['FinalGapPct'] = res['Q3_gap_pct'].fillna(res['Q2_gap_pct']).fillna(res['Q1_gap_pct'])



quali_feats = res[["Year", 
                   "Round", 
                   "EventFormat", 
                   "Abbreviation", 
                   "TeamName",
                   "Position", 
                   "Q1_gap_pct", 
                   "Q2_gap_pct", 
                   "Q3_gap_pct", 
                   "FinalGapPct"]]
quali_feats = quali_feats.rename(columns = {'Position' : 'QualiPos'})
print(quali_feats.shape)
print(quali_feats[quali_feats["QualiPos"] == 1])
print(quali_feats["FinalGapPct"].isna().sum())

valid = q_laps[
    q_laps['LapTime'].notna()
    & (q_laps['Deleted']==False)
    & (q_laps['IsAccurate']==True)
    & q_laps['PitOutTime'].isna()
    & q_laps['PitInTime'].isna()

]

best_idx = valid.groupby(['Year', 'Driver'])['LapTime'].idxmin()
best = valid.loc[best_idx, ['Year', 'Driver', 'Compound', 'SpeedST']]
best = best.rename(columns={'Compound' : 'best_lap_compound', 
                           'SpeedST' : 
                           'best_lap_top_speed'})

counts = valid.groupby(['Year',
                        'Driver']).size().rename('n_flying_laps').reset_index()

lap_summary = counts.merge(best, on=['Year', 'Driver'])

lap_summary = lap_summary.rename(columns={'Driver': 'Abbreviation'})

quali_feats = quali_feats.merge(lap_summary, on=['Year', 'Abbreviation'], how='left')

weather_summary = q_weather.groupby('Year').agg(
    air_temp=('AirTemp', 'mean'),
    track_temp=('TrackTemp', 'mean' ),
    humidity=('Humidity', 'mean'),
    wind_speed=('WindSpeed', 'mean'),
    any_rain=('Rainfall', 'max')
).reset_index()


weather_summary['any_rain'] = weather_summary['any_rain'].astype(int)

quali_feats = quali_feats.merge(weather_summary, on='Year', how='left')

race_cols = r_results[['Year', 
                       'Abbreviation', 
                       'Position', 
                       'GridPosition', 
                       'Points', 
                       'Status']]
race_cols = race_cols.rename(columns={'Position': 'FinishPos'})
race_cols['Podium'] = (race_cols['FinishPos'] <= 3).astype(int)

quali_feats = quali_feats.merge(race_cols, on=['Year', 'Abbreviation'], how='left')

quali_feats.loc[quali_feats['GridPosition']==0, 'GridPosition']=21

quali_feats['is_sprint'] = (quali_feats['EventFormat'] != 'conventional').astype(int)

quali_feats['best_lap_wet'] = quali_feats['best_lap_compound'].isin(['INTERMEDIATE', 'WET']).astype(int)

FEATURES = ['QualiPos', 'Q1_gap_pct', 'Q2_gap_pct', 'Q3_gap_pct', 'FinalGapPct',
            'n_flying_laps', 'best_lap_top_speed', 'best_lap_wet', 'is_sprint']


train = quali_feats[quali_feats['Year'] < 2026]
test = quali_feats[quali_feats['Year'] == 2026]

X_train = train[FEATURES]
y_train = train['Podium'].astype(int)
X_test = test[FEATURES]
print(X_train.shape, y_train.shape, X_test.shape)

hits = {}
for year, grp in train.groupby('Year'):
    hits[year] = int(grp.nsmallest(3, 'QualiPos')['Podium'].sum())
print(hits, sum(hits.values()), 'of', 3 * len(hits))

final_model = HistGradientBoostingClassifier(
    max_depth=3, learning_rate=0.05, max_iter=100, 
    min_samples_leaf=10, random_state=0
)
final_model.fit(X_train, y_train)

pred = test[['Abbreviation', 'TeamName', 'QualiPos']].copy()
pred['podium_prob'] = final_model.predict_proba(X_test)[:,1]
pred = pred.sort_values('podium_prob', ascending=False)

print(pred.head(8))
print(pred['podium_prob'].sum())

pred

