import pandas as pd
import plotly.express as px
import streamlit as st

from definitions import ROOT_DIR
from energy_insights_dashboard.visuals_config import (
    color_discrete_map_energy,
    german_layout,
)

PATH_DF_PRIMARY_ENERGY = ROOT_DIR / "energy_insights_dashboard/data/primary_energy.pkl"
PATH_DF_AK_ENERGY_SEC = ROOT_DIR / "energy_insights_dashboard/data/ak_energy_sec.pkl"
PATH_DF_AK_ENERGY_PRIMARY = ROOT_DIR / "energy_insights_dashboard/data/ak_energy_primary.pkl"


st.title("Energieverbrauch in Deutschland 2022")

st.header("Primärenergie")
st.write(
    "Primärenergieträger sind natürlich vorkommende Energieträger, welche noch nicht weiterverarbeitet wurden. "
    "I.d.R. können diese nicht direkt vom Verbraucher genutzt werden, sondern müssen vorher umgewandelt werden. "
    "Beispiele sind Wind, Sonne, Mineralöl oder Uran [1]. Um die weitere Verschärfung des Klimawandels zu verlangsamen "
    "und letztendlich zu stoppen ist es entscheidend, den Anteil der erneuerbaren Energien am Primärenergieverbrauch "
    "zu erhöhen sowie den Primärenergieverbrauch zu senken."
)
df_primary_energy = pd.read_pickle(PATH_DF_PRIMARY_ENERGY)
fig_primary_energy = px.pie(
    df_primary_energy,
    values="energie_2022",
    names=df_primary_energy.index,
    title="Primärenergiemix in Deutschland 2022<br><sup>Quelle: AG Energiebilanzen e. V.</sup>",
    color=df_primary_energy.index,
    color_discrete_map=color_discrete_map_energy,
)
fig_primary_energy.update_layout(german_layout)
st.plotly_chart(fig_primary_energy)

st.write(
    "Im Jahr 2022 wurden in Deutschland 11.769 Petajoule (Peta = 10 ^ 15) Primärenergie verbraucht [2]. "
    "Davon stammten 17.2 % aus erneuerbaren Quellen [2]. "
    "Dies unterstreicht, wie weit der Weg der Tranformation noch ist."
)


df_ak_energy_prim = pd.read_pickle(PATH_DF_AK_ENERGY_PRIMARY)

df_ak_energy_prim_long = df_ak_energy_prim.stack()
df_ak_energy_prim_long.index.names = ["Energieträger", "Jahr"]

df_ak_energy_prim_long = df_ak_energy_prim_long.reset_index(inplace=False)
df_ak_energy_prim_long.rename({0: "PJ"}, axis=1, inplace=True)
df_ak_energy_prim_long["Jahr"] = pd.to_datetime(df_ak_energy_prim_long["Jahr"], format="%Y")
fig_energy_sector_year = px.bar(
    df_ak_energy_prim_long,
    x="Jahr",
    y="PJ",
    color="Energieträger",
    color_discrete_map=color_discrete_map_energy,
    title="Primärenergiemix in Deutschland über die Zeit in Petajoule<br><sup>Quelle: AG Energiebilanzen e. V.</sup>",
)
fig_energy_sector_year.update_layout(german_layout)
st.plotly_chart(fig_energy_sector_year)
st.write(
    "Es ist ein Zugewinn an erneuerbaren Energien (dunkelgrün) sowie ein leichter "
    "Rückgang des Gesamtenergieverbrauchs in den letzten Jahren zu beobachten. "
    "Die Geschwindigkeit des Zubaus ist jedoch bisher nicht ausreichend, um "
    "das Pariser Klimaabkommen einzuhalten."
)

st.header("Quellen:")
st.write(
    "[1] Autoren der Wikimedia-Projekte, “Art von Energie,” Wikipedia.org, Mar. 09, 2004. "
    "https://de.wikipedia.org/wiki/Prim%C3%A4renergie (accessed Nov. 03, 2023)."
)
st.write(
    "[2] Auswertungstabellen» AG Energiebilanzen e. V.,” AG Energiebilanzen e. V. https://ag-energiebilanzen.de/daten-und-fakten/auswertungstabellen/"
)
