"""
# My first app
Here's our first attempt at using data to create a table:
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from definitions import ROOT_DIR

PATH_DF = ROOT_DIR / "energy_insights_dashboard/data/energy_im_export.pkl"

st.title("Energiewende Dashboard")

st.header("Energieimporte/-exporte in 2023")

df = pd.read_pickle(PATH_DF)

color_discrete_map_im_export = {
    "import": "red",
    "export": "green",
    "net_export": "goldenrod",
}


df_ex_imports_by_season = df.groupby("date")[["import", "export"]].sum()
df_ex_imports_by_season["import"] *= -1

df_ex_imports_by_seasons_stacked = df_ex_imports_by_season.stack()
df_ex_imports_by_seasons_stacked.index.names = ["date", "type"]

fig_net = px.area(
    df_ex_imports_by_seasons_stacked,
    x=df_ex_imports_by_seasons_stacked.index.get_level_values("date"),
    y=df_ex_imports_by_seasons_stacked.values,
    color=df_ex_imports_by_seasons_stacked.index.get_level_values("type"),
    title="Import/Export nach Saison",
    labels={"x": "Monat", "y": "MWh"},
    color_discrete_map=color_discrete_map_im_export,
)

st.plotly_chart(fig_net, use_container_width=True)

fig_net_country = px.bar(
    df,
    x=df.index.get_level_values(level="date"),
    y="net_export",
    color=df.index.get_level_values(level="country"),
    barmode="group",
    title="Im/Export nach Monat und Land",
    labels={"x": "Monat", "y": "MWh"},
)
st.plotly_chart(fig_net_country, use_container_width=True)
