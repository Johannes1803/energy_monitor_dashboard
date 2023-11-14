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

st.title("Mythen zur Energiewende")

st.write(
    '### "In Deutschland funktioniert die Produktion erneuerbarer Energien nur im Sommer. Im Winter sind wir dann doch wieder fast ausschließlich auf Kohle, Gas und Atomstrom angewiesen."'
)
st.write(
    """Möglicherweise ist dieser Mythos darauf zurückzuführen, dass wir alle wissen, wann die Sonne scheint.
         Windstatistiken sind uns dabei deutlich weniger präsent.
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
    """
    Wenig überraschend bringt Photovoltaik (Orange) im Winter wenig Ertrag, was dann
    im Frühling zunimmt, im Sommer seinen Peak erreicht und im Herbst wieder abnimmt.  
    Natürlich gibt es deutlich mehr erneuerbare Energien, sehen wir uns also das komplette Bild an.
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
    Am Boden des Graphen sind erneurbare Energien zu sehen wie z.B. Biomasse, die kontinuierlich Energie liefern.
    Die Erneuerbaren **fallen also nie auf Null**.
    Der Wind (türkis und dunkelblau) weht im Winter stärker als in den Sommermonaten.
    Dies ist eine sehr gute Nachricht, da es bedeutet, **dass die beiden Energieformen sich sehr gut ergänzen**. Es bedeutet
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
         In jedem Fall stellen solche Perioden die Energiewende vor ihre größte Herausforderung. Für diese Fälle werden
         dann zukünftig grüne Gaskraftwerke benötigt. Aufgrund ihres geringen Wirkungsgrades sind diese i.d.R. zu teuer,
         kämen aber in dieser Phase mangels Alternativen zum Einsatz.
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

    **Fazit:**
    - Wind weht im Winter stärker als im Sommer, was sich mit Photovoltaik gut ergänzt.
    - Die Erneuerbaren fallen nie auf Null (z.B. Biomasse).
    - Die wohl größte Herausforderung bei der Energiewende sind längere, windarme Perioden im Winter. Möglicherweise 
    wird dies bei der grünen Transformation die letzte Etappe. Es ist kein Grund, die Etappen davor nicht jetzt zu
    beschreiten. 
"""
)

st.write(
    """
    ### "Erneuerbare Energien sind sehr billig." bzw. "Erneuerbare Energien sind unbezahlbar."
    Das Merit Order Prinzip bezeichnet den marktwirtschaftlichen Mechanismus, nachdem die günstigeren Energien,
    wenn verfügbar die teureren Energien aus dem Markt drängen. Der Markpreis wird bestimmt durch das teuerste, aktuell
    noch benötigte Kraftwerk. Wenn also der Wind weht und die Sonne scheint,
    werden teurere Gas- und Kohlekraftwerke still gelegt. Der Strom ist in diesen Phasen günstig und grün.
    Aktuell sind wir in Phasen ohne Wind und Sonne noch auf konventionelle Energieträger angewiesen. Mit 
    fortschreitender grüner Transformation sollte dies abnehmen.  
    **Fazit:** Beide Aussagen sind unzulässig verkürzt.
    """
)

st.write("## Quellen:")
st.write(
    """
[1]“Stromerzeugung 2022: Ein Drittel aus Kohle, ein Viertel aus Windkraft,” Statistisches Bundesamt. https://www.destatis.de/DE/Presse/Pressemitteilungen/2023/03/PD23_090_43312.html

‌
"""
)
