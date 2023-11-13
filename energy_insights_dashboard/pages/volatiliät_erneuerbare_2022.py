import pandas as pd
import plotly.express as px
import streamlit as st

from definitions import ROOT_DIR

PATH_DF_DAILY = ROOT_DIR / "energy_insights_dashboard/data/electricity_2022_daily.pkl"
PATH_DF_HOURLY = ROOT_DIR / "energy_insights_dashboard/data/electricity_2022_hourly.pkl"

df_renewable_vs_rest_stacked_daily = pd.read_pickle(PATH_DF_DAILY)
df_renewable_vs_rest_stacked_hourly = pd.read_pickle(PATH_DF_HOURLY)


color_map = {
    "Biomasse": "#862A16",
    "Wind Onshore": "#00A08B",
    "Wind Offshore": "#1616A7",
    "Photovoltaik": "#EB663B",
    "Konventionell": "#DA16FF",
    "Pumpspeicher": "#0D2A63",
    "Wasserkraft": "#2E91E5",
}


st.title("Betrachtungen zur Volatilität der Erneuerbaren Energien")
# st.write(
#     """Zur Erreichung der Klimaziele ist es unerläßlich, dass die Sektoren Verkehr,
#     Industrie, Dienstleistungen/Gewerbe sowie Haushalte auf erneuerbare Energien
#     umsteigen. Grüner Wasserstoff und Co. werden aufgrund geringer Energieeffizenz
#     auf absehbare Zeit teuer bleiben und damit in Bereichen zum Einsatz kommen, in
#     denen es keine Alternativen gibt. Dazu zählen z.B. Industrie, Flug-, Schiff- und
#     Schwerlastverkehr. Aufgrund des wesentlich höheren Wirkungsgrades sollte wo möglich
#     elektrifiziert werden.
#     Dies führt dazu, dass der Strombedarf künftig ansteigen wird. Die größten Ausbaupotenziale
#     für erneuerbare Energien besitzen Windkraft und Photovoltaik. Diese Quellen sind jedoch volatil,
#     d.h. sie sind nur verfügbar, wenn der Wind weht bzw. die Sonne scheint. Dieser Artikel
#     beschäftigt sich mit der Frage, wie der erzeugte elektrische Strom schwankte im Jahr 2022 und
#     was sich daraus über die Volatilität ableiten lässt."""
# )

st.write(
    """
Etwas vereinfacht gesagt ist das Ziel den Einsatz konventioneller Energieträger zu minimieren. Hierbei sind drei Fragen
entscheidend:  
    1. Wie viel Strom muss mit konventionellen Energieträgern produziert werden (Weil der Bedarf nicht durch
    erneuerbare Energien gedeckt werden kann)?  
    2. Über welche Zeiträume muss das Delta zwischen verfügbaren erneuerbaren Energien und dem Bedarf
        zwischen verfügbaren erneuerbaren Energien und dem Bedarf
    durch konventionelle Energieträger gedeckt werden?  
    3. Wie viel installierte Leistung muss durch konventionelle Kraftwerke vorgehalten werden? Dies entspricht dem
    maximalen Delta?  

Des Weiteren gehen wir im Folgenden davon aus, dass erneuerbare Energien, wenn verfügbar immer eingespeist werden.
Diese Annahme ist zutreffend, da sie die geringsten Marktpreise haben und somit teurere Alternativen aus dem
Markt drängen (Merit Order).
"""
)

st.write("## 1. Wie viel Strom muss mit konventionellen Energieträgern produziert werden?")
st.write(
    """Machen wir (die natürlich falsche) Annahme, dass erneuerbare Energien gratis, in unbeschränkten Mengen,
    verlustfrei und beliebig lange gespeichert werden können ("perfekter Speicher").
    In diesem Fall müsste man einfach nur die installierte Leistung der erneuerbaren Energien erhöhen, bis sie den Bedarf decken.
    Im Jahr 2022 wurden 46,2% des Stroms aus erneuerbaren Energien gedeckt. 
    """
)
series_total = df_renewable_vs_rest_stacked_hourly.groupby("Datum")["Petajoule"].sum()
series_total = series_total.reset_index()
series_total["Energiekategorie"] = "Total"
series_solar = df_renewable_vs_rest_stacked_hourly.query("Energiekategorie == 'Photovoltaik'")
df_solar_vs_total_long = pd.concat([series_total, series_solar])

fig_solar_vs_total = px.line(
    df_solar_vs_total_long,
    x="Datum",
    y="Petajoule",
    color="Energiekategorie",
    color_discrete_map=color_map,
    title="Stromerzeugung Konventionelle vs. Solar pro Stunde im Jahr 2022 <br><sup>Quelle: SMARD</sup>",
)
st.plotly_chart(fig_solar_vs_total)
st.write(
    """Solar ist eine volatile Energiequelle, da die Sonne nachts gar nicht und im Winter wenig scheint. Trotzdem zeigt
    die Grafik, dass noch Kapazitäten zum Ausbau von Solar bestehen. Die Annahme des perfekten Speichers ist also
    durchaus zielführend in einem frühen Stadium der grünen Transformation (in dem wir uns befinden). Mit zunehmendem
    Ausbau der Erneuerbaren wird sie entsprechend unbrauchbarer, da überschüßiger Strom nicht eingespeißt werden kann.
    """
)


st.write("## 2.  Über welche Zeiträume muss das Delta gedeckt werden? ")
st.write(
    """Beim Blick auf Photovoltaik alleine (siehe oben) steht zu befürchten, dass über die kompletten Wintermonate das
    Delta durch konventionelle Energieträger aufgefangen werden muss. Natürlich gibt es deutlich mehr erneuerbare
    Energien, sehen wir uns also das komplette Bild an.
    """
)

df_konventionell = df_renewable_vs_rest_stacked_daily.query("Energiekategorie == 'Konventionell'")
fig_electricity_day_konventionell = px.area(
    df_konventionell,
    x="Datum",
    y="Petajoule",
    color="Energiekategorie",
    labels={"x": "Tag"},
    title="Stromerzeugung Konventionelle pro Tag im Jahr 2022 <br><sup>Quelle: SMARD</sup>",
    color_discrete_map=color_map,
    category_orders={
        "Energiekategorie": [
            "Pumpspeicher",
            "Biomasse",
            "Wasserkraft",
            "Sonstige Erneuerbare",
            "Photovoltaik",
            "Wind Onshore",
            "Wind Offshore",
            "Konventionell",
        ]
    },
)
# st.plotly_chart(fig_electricity_day_konventionell)

# st.write(
#     """
#     In dieser Grafik ist die Stromerzeugung durch konventionelle Energieträger nochmals alleine abgebildet.
# """
# )
fig_electricity_day = px.area(
    df_renewable_vs_rest_stacked_daily,
    x="Datum",
    y="Petajoule",
    color="Energiekategorie",
    labels={"x": "Tag"},
    title="Stromerzeugung pro Tag im Jahr 2022 <br><sup>Quelle: SMARD</sup>",
    color_discrete_map=color_map,
    category_orders={
        "Energiekategorie": [
            "Pumpspeicher",
            "Biomasse",
            "Wasserkraft",
            "Sonstige Erneuerbare",
            "Photovoltaik",
            "Wind Onshore",
            "Wind Offshore",
            "Konventionell",
        ]
    },
)

st.plotly_chart(fig_electricity_day)

st.write(
    """Zu sehen ist die Stromerzeugung aggregiert über einen Tag pro Energieträger.
    Zur Verbesserung der Übersichtlichkeit sind alle konventionellen Energieträger zusammengefasst (Pink).
    Da die Daten über einen Tag aggregiert sind, lässt sich hier keine Aussage über Schwankungen
    innerhalb eines Tages machen.  
    Am Boden des Graphen sind erneurbare Energien zu sehen wie z.B. Biomasse, die kontinuierlich Energie liefern.
    Die Erneuerbaren fallen also nie auf Null.
    Wenig überraschend bringt Photovoltaik (Orange) im Winter wenig Ertrag, was dann
    im Frühling zunimmt, im Sommer seinen Peak erreicht und im Herbst wieder abnimmt. Der Wind (türkis und dunkelblau)
    weht im Winter stärker als in den Sommermonaten.
    Dies ist eine sehr gute Nachricht, da es bedeutet, dass die beiden Energieformen sich sehr gut ergänzen. Es bedeutet
    aber auch, dass man den Ausbau der Windenergie nicht vernachlässigen darf, wie es in Bayern und Baden-Württemberg
    sträflicherweise der Fall ist.
    """
)
mask_date_little_renewables = (
    df_renewable_vs_rest_stacked_hourly["Datum"] >= pd.to_datetime("2022-11-17", format="%Y-%m-%d")
) & (df_renewable_vs_rest_stacked_hourly["Datum"] <= pd.to_datetime("2022-12-20", format="%Y-%m-%d"))

st.write(
    """Zoomen wir auf den schlechtesten Zeitraum für Erneuerbare in Deutschland 2022, Ende November bis Mitte Dezember.
    Hier war über einen außergewöhnlich langen Zeitraum wenig Wind und erwartungsgemäß wenig Sonne.
    """
)
fig_electricity_hour_lacking = px.area(
    df_renewable_vs_rest_stacked_hourly[mask_date_little_renewables],
    x="Datum",
    y="Petajoule",
    color="Energiekategorie",
    labels={"x": "Tag"},
    title="Stromerzeugung pro Stunde <br><sup>Quelle: SMARD</sup>",
    color_discrete_map=color_map,
    category_orders={
        "Energiekategorie": [
            "Pumpspeicher",
            "Biomasse",
            "Wasserkraft",
            "Sonstige Erneuerbare",
            "Photovoltaik",
            "Wind Onshore",
            "Wind Offshore",
            "Konventionell",
        ]
    },
)
st.plotly_chart(fig_electricity_hour_lacking)

st.write(
    """In der stündlichen Auflösung sehen wir die Schwankungen innerhalb eines Tages. Um den 30. November
         und 11. Dezember waren jeweils 3 Tage mit besonders wenig Wind. Auch das durchschnittliche Windniveau
         war in diesem Zeitraum gering. Aus den Daten eines Jahres lässt sich natürlich nicht ablesen, wie oft das 
         vorkommt.
         In jedem Fall stellen solche Perioden die Energiewende vor ihre größte Herausforderung.
         """
)


mask_date_many_renewables = (
    df_renewable_vs_rest_stacked_hourly["Datum"] >= pd.to_datetime("2022-01-25", format="%Y-%m-%d")
) & (df_renewable_vs_rest_stacked_hourly["Datum"] <= pd.to_datetime("2022-02-25", format="%Y-%m-%d"))

fig_electricity_hour_sufficient = px.area(
    df_renewable_vs_rest_stacked_hourly[mask_date_many_renewables],
    x="Datum",
    y="Petajoule",
    color="Energiekategorie",
    labels={"x": "Tag"},
    title="Stromerzeugung pro Stunde <br><sup>Quelle: SMARD</sup>",
    color_discrete_map=color_map,
    category_orders={
        "Energiekategorie": [
            "Pumpspeicher",
            "Biomasse",
            "Wasserkraft",
            "Sonstige Erneuerbare",
            "Photovoltaik",
            "Wind Onshore",
            "Wind Offshore",
            "Konventionell",
        ]
    },
)
st.plotly_chart(fig_electricity_hour_sufficient)
st.write(
    """
    Dass Winter nicht gleichzusetzen ist mit wenig erneuerbaren Energien, zeigt der Februar eindrucksvoll, in dem viel
    Wind wehte und somit wesentlich weniger auf konventionelle Energieträger zurückgegriffen werden musste.
"""
)
