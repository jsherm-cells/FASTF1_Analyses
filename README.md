# FASTF1_Analyses

Personal project I am pursuing to increase my knowledge of python and data analytics. I will look at data from all sessions, making weekend predictions, and analyzing car/driver performance.

## Analyses

| Analysis | Question | Dashboard |
|---|---|---|
| [USA Grand Prix Analysis](USA_GP_2026/) | What performance factors separated the top 5 finishers? | Coming Soon |
| [Mexico Gran Prix Battle Analysis](MEXICO26_FERRARI_BATTLE/) | Who deserved to win this battle? Was it worth it or did it ruin the Ferrari's race? | Coming Soon |
| [Free Practice One Rookie Analysis](ROOKIES_BRAZIL_26/) | How did the rookies fare against the fastest in FP1? | Coming Soon |
| [Las Vegas Strip Straight Super Clipping Analysis](LV_SC_COMP/) | How was super clipping affected car performance on the Las Vegas Strip Straight? | Coming Soon |
| [Brazil Podium Prediction](BRAZIL_26_PRED/) | Using HistGradientBoostingClassifier to predict the podium finishers of the 2026 Brazilian Gran Prix | N/A |

## Run it locally

```bash
git clone https://github.com/jsherm-cells/FASTF1_Analyses
cd FASTF1_Analyses
pip install -r requirements.txt
streamlit run [gp_folder]/[app].py
```

## Built with

- [FastF1](https://github.com/theOehrly/Fast-F1): F1 data access
- [pandas](https://pandas.pydata.org): data analysis
- [Plotly Express](https://plotly.com/python/plotly-express/): interactive charts
- [Streamlit](https://streamlit.io): interactive dashboard

## Data and acknowledgements

Data was accessed using [FastF1](https://github.com/theOehrly/Fast-F1), an
open-source Python package. The underlying data belongs to its respective
owners and is not included in this repository. This is an independent,
non-commercial project and is not affiliated with or endorsed by Formula 1 or
the FIA. F1, FORMULA 1, and related marks are trademarks of Formula One
Licensing B.V.
