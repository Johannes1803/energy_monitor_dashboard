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


class ToTimeDeltaTransformer(ColumnTransformer):
    def __init__(self, columns, result_columns=None, drop=True, suffix=None, **kwargs):
        super().__init__(columns, result_columns, drop, suffix, **kwargs)

    def _col_transform(
        self,
        series: pd.Series,
        label: str,
    ) -> pd.Series:
        return pd.to_timedelta(series + ":00")


class MWHToPetaJouleTransformer(ColumnTransformer):
    def __init__(self, columns, result_columns=None, drop=True, suffix=None, **kwargs):
        super().__init__(columns, result_columns, drop, suffix, **kwargs)

    def _col_transform(
        self,
        series: pd.Series,
        label: str,
    ) -> pd.Series:
        return (series * 3.6 * 10e09) / 10e15
