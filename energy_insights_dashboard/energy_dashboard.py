"""
# My first app
Here's our first attempt at using data to create a table:
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from definitions import ROOT_DIR


def cond_formatting(x):
    if x >= 0:
        return "background-color: green"
    else:
        return "background-color: red"


PATH_DF_PRIMARY_ENERGY = ROOT_DIR / "energy_insights_dashboard/data/primary_energy.pkl"
PATH_DF_AK_ENERGY = ROOT_DIR / "energy_insights_dashboard/data/ak_energy.pkl"

color_discrete_map_energy = {
    "Braunkohle": "brown",
    "Erdgas": "blue",
    "Erdgas, Erdölgas": "blue",
    "Gase": "blue",
    "Erneuerbare Energien": "green",
    "Mineralöl": "black",
    "Mineralöle": "black",
    "Kernenergie": "orange",
    "Sonstige": "yellow",
    "Sonstige Energieträger": "yellow",
    "Steinkohle": "grey",
    "Strom": "#13DB38",
}


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
st.plotly_chart(fig_primary_energy)

st.write(
    "Im Jahr 2022 wurden in Deutschland 11.769 Petajoule (Peta = 10 ^ 15) Primärenergie verbraucht [2]. "
    "Davon stammten 17.2 % aus erneuerbaren Quellen [2]. "
    "Dies unterstreicht, wie weit der Weg der Tranformation noch ist."
)


st.header("Endenergie")
st.write(
    "Endenergie bezeichnet die Energie, die dem Verbraucher nach (verlustreicher) "
    "Umwandlung der Primärenergieträger und Transport zur Verfügung steht [1]."
)

df_ak_energy = pd.read_pickle(PATH_DF_AK_ENERGY)
df_energy_by_sector = df_ak_energy[2022].groupby("Sektor").sum()

fig_sectors = px.pie(
    df_energy_by_sector,
    values=df_energy_by_sector.values,
    names=df_energy_by_sector.index,
    color_discrete_sequence=px.colors.qualitative.Pastel,
    title="Anteil am Endenergieverbrauch nach Sektor 2022 <br><sup>Quelle: AG Energiebilanzen e. V.</sup>",
)
st.plotly_chart(fig_sectors)

st.write(
    "Die Sektoren Verkehr, Privathaushalte und Industrie haben mit jeweils knapp 30% "
    "ähnliche Anteile am Endenergieverbrauch [2]."
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
