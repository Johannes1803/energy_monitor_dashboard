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


PATH_DF = ROOT_DIR / "energy_insights_dashboard/data/energy_im_export.pkl"

color_discrete_map_im_export = {
    "import": "red",
    "export": "green",
    "net_export": "goldenrod",
}

st.title("Energiewende Dashboard Deutschland")

st.header("Stromimporte/-exporte in 2023")

df = pd.read_pickle(PATH_DF)


# figure
df_ex_imports_by_season = df.groupby("date")[["import", "export", "net_export"]].sum()
df_ex_imports_by_season["import"] *= -1

df_ex_imports_by_seasons_stacked = df_ex_imports_by_season.stack()
df_ex_imports_by_seasons_stacked.index.names = ["date", "type"]

fig_net = px.bar(
    df_ex_imports_by_seasons_stacked,
    x=df_ex_imports_by_seasons_stacked.index.get_level_values("date"),
    y=df_ex_imports_by_seasons_stacked.values,
    color=df_ex_imports_by_seasons_stacked.index.get_level_values("type"),
    title="Import/Export nach Monat",
    labels={
        "x": "Monat",
        "y": "MegaWattstunden (MWh)",
        "import": "Import",
        "export": "Export",
        "net_export": "Exportüberschuss",
    },
    color_discrete_map=color_discrete_map_im_export,
    barmode="group",
)

st.plotly_chart(fig_net, use_container_width=True)
st.write(
    "Nach Exportüberschüssen im Winter ging die Tendenz ab April hin zu Exportdefiziten. "
    "Ein Zusammenhang mit der Abschaltung der letzten Atomkraftwerke im April ist naheliegend."
)

fig_net_country = px.bar(
    df,
    x=df.index.get_level_values(level="date"),
    y="net_export",
    color=df.index.get_level_values(level="country"),
    barmode="group",
    title="Import/Export nach Monat und Land",
    labels={"x": "Monat", "net_export": "MWh"},
)
st.plotly_chart(fig_net_country, use_container_width=True)

st.write(
    "Quelle: [Statistisches Bundesamt](https://www-genesis.destatis.de/genesis/online?&sequenz=tabelleErgebnis&selectionname=43312-0002#abreadcrumb)"
)
