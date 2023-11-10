import pandas as pd
import plotly.express as px
import streamlit as st

from definitions import ROOT_DIR
from energy_insights_dashboard.visuals_config import (
    color_discrete_map_energy,
    german_layout,
)

PATH_DF_AK_ENERGY_SEC = ROOT_DIR / "energy_insights_dashboard/data/ak_energy_sec.pkl"

st.header("Endenergie")
st.write(
    "Endenergie bezeichnet die Energie, die dem Verbraucher nach (verlustreicher) "
    "Umwandlung der Primärenergieträger und Transport zur Verfügung steht [1]."
    "Der Endenergieverbrauch lässt sich nach Sektoren aufschlüßeln. Dies ist "
    "hilfreich, um Sektoren zu identifizieren, die im besonderen Maße zur Emission "
    "von Treibhausgasen beitragen."
)

df_ak_energy = pd.read_pickle(PATH_DF_AK_ENERGY_SEC)
df_energy_by_sector = df_ak_energy[2022].groupby("Sektor").sum()

fig_sectors = px.pie(
    df_energy_by_sector,
    values=df_energy_by_sector.values,
    names=df_energy_by_sector.index,
    color_discrete_sequence=px.colors.qualitative.Pastel,
    title="Anteil am Endenergieverbrauch nach Sektor 2022 <br><sup>Quelle: AG Energiebilanzen e. V.</sup>",
)

fig_sectors.update_layout(german_layout)
st.plotly_chart(fig_sectors)

st.write(
    "Die Sektoren Verkehr, Privathaushalte und Industrie haben mit jeweils knapp 30% "
    "ähnliche Anteile am Endenergieverbrauch [2]."
)

df_energy_carrier = df_ak_energy[2022].groupby("Energieträger").sum()
df_energy_carrier = df_energy_carrier.reset_index()
df_energy_carrier.rename({2022: "PJ"}, axis=1, inplace=True)

fig_energy_carriers = px.pie(
    df_energy_carrier,
    values="PJ",
    names="Energieträger",
    color="Energieträger",
    color_discrete_map=color_discrete_map_energy,
    title="Anteil am Endenergieverbrauch nach Energieträger 2022 <br><sup>Quelle: AG Energiebilanzen e. V.</sup>",
)
st.plotly_chart(fig_energy_carriers)
st.write(
    "Erklärung zu Strom: Hier ist Strom aus erneuerbaren Energien inkludiert, im Jahr 2022 betrug der Anteil "
    "der Erneuerbaren am Strommix 46,2%. 'Erneuerbare Energien' bezieht sich hier z.B. auf Geothermie, Solarthermie, "
    "Biomasse und Wärmepumpen."
)


fig_sectors_source = px.scatter(
    df_ak_energy[2022],
    x=df_ak_energy[2022].index.get_level_values("Sektor"),
    y=df_ak_energy[2022].index.get_level_values("Energieträger"),
    color=df_ak_energy[2022].index.get_level_values("Energieträger"),
    size=df_ak_energy[2022].values,
    color_discrete_map=color_discrete_map_energy,
    labels={"x": "Sektor", "y": "Energieträger", "color": "Energieträger"},
    title="Endenergieverbrauch nach Sektor und Energieträger 2022 in Petajoule<br><sup>Quelle: AG Energiebilanzen e. V.</sup>",
)
fig_sectors_source.update_layout(german_layout)
st.plotly_chart(fig_sectors_source)
st.write(
    "Es fällt auf, dass der Verkehrsektor einen sehr hohen Energiebedarf hat und diesen zu großen Teilen aus Mineralölen deckt, was zu einem Verbrauch "
    "von ca. 2.300 PJ an fossilen Energieträgern führt. "
    "Im Industriesektor sind Gase, Strom und Steinkohle die wichtigsten Energieträger. "
    "Bei privaten Haushalten zeigt sich ein hoher Verbrauch an Erdgas und Mineralöl, "
    "welcher überwiegend auf das Heizen zurückzuführen ist."
)


st.header("Quellen:")
st.write(
    "[1] Autoren der Wikimedia-Projekte, “Art von Energie,” Wikipedia.org, Mar. 09, 2004. "
    "https://de.wikipedia.org/wiki/Prim%C3%A4renergie (accessed Nov. 03, 2023)."
)
st.write(
    "[2] Auswertungstabellen» AG Energiebilanzen e. V.,” AG Energiebilanzen e. V. https://ag-energiebilanzen.de/daten-und-fakten/auswertungstabellen/"
)
