import pandas as pd
from pdpipe.col_generation import ColumnTransformer


class ToDateTimeTransformer(ColumnTransformer):
    def __init__(self, columns, format_str: str, result_columns=None, drop=True, suffix=None, **kwargs):
        super().__init__(columns, result_columns, drop, suffix, **kwargs)
        self.format_str = format_str

    def _col_transform(
        self,
        series: pd.Series,
        label: str,
    ) -> pd.Series:
        return pd.to_datetime(series, format=self.format_str)
