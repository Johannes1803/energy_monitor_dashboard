import pandas as pd
import plotly.express as px
import streamlit as st

from definitions import ROOT_DIR

PATH_DF_ELECTRICITY_IM_EXPORT = ROOT_DIR / "energy_insights_dashboard/data/energy_im_export.pkl"
st.header("Stromimporte/-exporte in 2023")
df_electricity_im_export = pd.read_pickle(PATH_DF_ELECTRICITY_IM_EXPORT)

color_discrete_map_im_export = {
    "import": "red",
    "export": "green",
    "net_export": "goldenrod",
}
# figure
df_ex_imports_by_season = df_electricity_im_export.groupby("date")[["import", "export", "net_export"]].sum()
df_ex_imports_by_season["import"] *= -1

df_ex_imports_by_seasons_stacked = df_ex_imports_by_season.stack()
df_ex_imports_by_seasons_stacked.index.names = ["date", "type"]

fig_net = px.bar(
    df_ex_imports_by_seasons_stacked,
    x=df_ex_imports_by_seasons_stacked.index.get_level_values("date"),
    y=df_ex_imports_by_seasons_stacked.values,
    color=df_ex_imports_by_seasons_stacked.index.get_level_values("type"),
    title="Import/Export nach Monat<br><sup>Quelle: Statistisches Bundesamt</sup>",
    labels={
        "x": "Monat",
        "y": "Petajoule (PJ)",
        "import": "Import",
        "export": "Export",
        "net_export": "Exportüberschuss",
        "color": "Legende",
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
    df_electricity_im_export,
    x=df_electricity_im_export.index.get_level_values(level="date"),
    y="net_export",
    color=df_electricity_im_export.index.get_level_values(level="country"),
    barmode="group",
    title="Netto Exportüberschuss-/defizit nach Monat und Land<br><sup>Quelle: Statistisches Bundesamt</sup>",
    labels={"x": "Monat", "net_export": "PJ", "color": "Nation"},
)
st.plotly_chart(fig_net_country, use_container_width=True)

st.write(
    "Quelle: [1] Federal Statistical Office Germany - GENESIS-Online,” www-genesis.destatis.de, Nov. 03, 2023."
    " https://www-genesis.destatis.de/genesis/online?&sequenz=tabelleErgebnis&selectionname=43312-0002#abreadcrumb"
    " (accessed Nov. 03, 2023)."
)
