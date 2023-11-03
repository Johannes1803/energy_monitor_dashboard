import pandas as pd
import pdpipe as pdp

from definitions import ROOT_DIR

PATH_AK_ENERGY = ROOT_DIR / "energy_insights_dashboard/data/AKEnergie.xlsx"
MAPPING_SECTOR_WORKSHEET = {"6.2": "Industrie", "6.3": "Haushalte", "6.4": "Dienstleistungen/Gewerbe", "6.6": "Verkehr"}
PRIMARY_ENERGY_WORKSHEET = "6.1"
ENERGY_UNIT = "PJ"  # peta joule

pipeline = pdp.PdPipeline(
    [
        pdp.RowDrop(conditions=[lambda x: x != "PJ"], columns="Einheit"),
        pdp.RowDrop(conditions=[lambda x: x == "Insgesamt"], columns="Energieträger"),
        pdp.RowDrop(conditions=[lambda x: x == "Erdgas, Erdölgas"], columns="Energieträger"),
        pdp.df.drop(columns=["Unnamed: 0", "Einheit", "Unnamed: 36"]),
    ]
)

if __name__ == "__main__":
    xls = pd.ExcelFile(PATH_AK_ENERGY)
    dfs = []

    for worksheet, sector in MAPPING_SECTOR_WORKSHEET.items():
        df_raw = pd.read_excel(xls, sheet_name=worksheet, skiprows=2, header=1)
        df = pipeline.apply(df_raw)
        df["Sektor"] = sector
        df.set_index(["Sektor", "Energieträger"], inplace=True)
        df = df.groupby(["Sektor", "Energieträger"]).sum()
        dfs.append(df)

    df_final = pd.concat(dfs)
    df_final = df_final.groupby(["Sektor", "Energieträger"]).sum()

    df_final.to_pickle(ROOT_DIR / "energy_insights_dashboard/data/ak_energy_sec.pkl")

    df_raw_primary = pd.read_excel(xls, sheet_name="2.1", skiprows=2, header=1)
    df_primary_en = pipeline.apply(df_raw_primary)
    df_primary_en.set_index(["Energieträger"], inplace=True)
    df_primary_en = df_primary_en.groupby(["Energieträger"]).sum()

    df_primary_en.to_pickle(ROOT_DIR / "energy_insights_dashboard/data/ak_energy_primary.pkl")
