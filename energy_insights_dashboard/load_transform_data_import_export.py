import locale

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pdpipe as pdp
import plotly.express as px

from definitions import ROOT_DIR
from energy_insights_dashboard.custom_transformers import ToDateTimeTransformer

PATH_ENERGY_IM_EXPORTS = ROOT_DIR / "energy_insights_dashboard/data/EinAusFuhrElektrizität.csv"
FIX_ASCII_ENCODING = {
    "D�nemark": "Dänemark",
    "M�rz": "März",
    "�sterreich": "Österreich",
    "Sonstige L�nder": "Sonstige Länder",
}
MONTHS_TO_SEASON = {
    "Januar": "Winter",
    "Februar": "Winter",
    "März": "Frühling",
    "April": "Frühling",
    "Mai": "Frühling",
    "Juni": "Sommer",
    "Juli": "Sommer",
    "August": "Sommer",
    "September": "Herbst",
    "Oktober": "Herbst",
    "November": "Winter",
    "Dezember": "Winter",
}

locale.setlocale(locale.LC_ALL, "de_DE.utf8")

pipeline = pdp.PdPipeline(
    [
        pdp.df.replace(to_replace=".", value=np.nan),
        pdp.df.replace(to_replace="...", value=np.nan),
        pdp.df.dropna(axis=0, how="any"),
        pdp.df.replace(FIX_ASCII_ENCODING),
        pdp.ColRename(
            rename_mapper={
                "Unnamed: 0": "year",
                "Unnamed: 1": "month",
                "Unnamed: 2": "country",
                "MWh": "import",
                "MWh.1": "export",
                "MWh.2": "net_import",
            }
        ),
        pdp.ColumnDtypeEnforcer(
            {
                "year": str,
                "month": str,
                "country": str,
                "import": np.float32,
                "export": np.float32,
                "net_import": np.float32,
            }
        ),
        pdp.df["net_export"] << pdp.df["net_import"] * (-1),
        pdp.df["season"] << pdp.df["month"].replace(MONTHS_TO_SEASON),
        pdp.ValDrop(values=["Insgesamt"], columns=["country"]),
        pdp.df["date"] << pdp.df["year"] + "-" + pdp.df["month"],
        ToDateTimeTransformer("date", "%Y-%B"),
        pdp.df.drop(columns=["year", "month"]),
        pdp.df.reindex(columns=["date", "country", "season", "import", "export", "net_import", "net_export"]),
        pdp.df.set_index(["date", "country"]),
    ]
)

if __name__ == "__main__":
    df_raw = pd.read_csv(
        PATH_ENERGY_IM_EXPORTS, sep=";", decimal=",", header=6, encoding="utf-8", skipfooter=4, engine="python"
    )
    df = pipeline(df_raw)
    df.to_pickle(ROOT_DIR / "energy_insights_dashboard/data/energy_im_export.pkl")
