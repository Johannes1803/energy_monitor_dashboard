import pandas as pd
import pdpipe as pdp

from definitions import ROOT_DIR

PATH_PRIMARY_ENERGY = ROOT_DIR / "energy_insights_dashboard/data/PrimärEnergie2022.xlsx"

pipeline = pdp.PdPipeline(
    [
        pdp.df.drop(
            columns=[
                "Unnamed: 0",
                "Unnamed: 1",
                "Unnamed: 5",
                "Unnamed: 6",
                "Unnamed: 7",
                "Unnamed: 8",
                "Unnamed: 9",
                "Unnamed: 10",
                "Unnamed: 11",
            ]
        ),
        pdp.ColRename(
            rename_mapper={
                "Unnamed: 3": "energie_2021",
                "Unnamed: 4": "energie_2022",
            }
        ),
    ]
)

if __name__ == "__main__":
    df_raw = pd.read_excel(PATH_PRIMARY_ENERGY, skiprows=14, index_col=2, skipfooter=9)
    df = pipeline.apply(df_raw)
    df.to_pickle(ROOT_DIR / "energy_insights_dashboard/data/primary_energy.pkl")
