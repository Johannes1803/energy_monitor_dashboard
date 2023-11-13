import pandas as pd
import pdpipe as pdp

from definitions import ROOT_DIR
from energy_insights_dashboard.custom_transformers import (
    MWHToPetaJouleTransformer,
    ToDateTimeTransformer,
    ToTimeDeltaTransformer,
)

PATH_DATA = ROOT_DIR / "energy_insights_dashboard/data/StromErzeugung2022.csv"

pipeline = pdp.PdPipeline(
    [
        pdp.ColRename(lambda x: x.replace(" [MWh] Calculated resolutions", "")),
        pdp.ColRename(lambda x: x.replace(" [MWh] Berechnete Auflösungen", "")),
        ToDateTimeTransformer("Datum", "%Y-%m-%d"),
        ToTimeDeltaTransformer("Anfang"),
        pdp.df["Datum"] << pdp.df["Datum"] + pdp.df["Anfang"],
        pdp.ColDrop(["Anfang", "Ende"], errors="ignore"),
        pdp.SetIndex("Datum"),
        pdp.ColumnDtypeEnforcer(
            {
                "Wind Offshore": float,
                "Wind Onshore": float,
                "Photovoltaik": float,
                "Biomasse": float,
                "Wasserkraft": float,
                "Sonstige Erneuerbare": float,
                "Kernenergie": float,
                "Braunkohle": float,
                "Steinkohle": float,
                "Erdgas": float,
                "Pumpspeicher": float,
                "Sonstige Konventionelle": float,
            }
        ),
        MWHToPetaJouleTransformer(
            [
                "Photovoltaik",
                "Wind Offshore",
                "Wind Onshore",
                "Biomasse",
                "Wasserkraft",
                "Sonstige Erneuerbare",
                "Kernenergie",
                "Braunkohle",
                "Steinkohle",
                "Erdgas",
                "Pumpspeicher",
                "Sonstige Konventionelle",
            ]
        ),
    ]
)

if __name__ == "__main__":
    df_raw = pd.read_csv(PATH_DATA, sep=";", decimal=",", thousands=".", date_format="%d.%m.%Y", parse_dates=[0, 1])
    df = pipeline.apply(df_raw)

    df_stacked = df.stack()
    df_stacked = df_stacked.reset_index()
    df_stacked.rename({"level_1": "Energiequelle", 0: "Petajoule"}, axis=1, inplace=True)
    df_stacked["Energieklasse"] = df_stacked["Energiequelle"].replace(
        {
            "Biomasse": "Erneuerbar",
            "Wasserkraft": "Erneuerbar",
            "Wind Offshore": "Erneuerbar",
            "Wind Onshore": "Erneuerbar",
            "Photovoltaik": "Erneuerbar",
            "Sonstige Erneuerbare": "Erneuerbar",
            "Kernenergie": "Konventionell",
            "Braunkohle": "Konventionell",
            "Steinkohle": "Konventionell",
            "Erdgas": "Konventionell",
            "Pumpspeicher": "Erneuerbar",
            "Sonstige Konventionelle": "Konventionell",
        }
    )

    df_stacked["Energiekategorie"] = df_stacked["Energiequelle"].where(
        df_stacked["Energieklasse"] == "Erneuerbar", "Konventionell"
    )

    df_renewable_vs_rest_stacked = df_stacked.groupby(["Datum", "Energiekategorie"])["Petajoule"].sum()

    df_renewable_vs_rest_stacked.reset_index().to_pickle(
        ROOT_DIR / "energy_insights_dashboard/data/electricity_2022_daily.pkl"
    )
