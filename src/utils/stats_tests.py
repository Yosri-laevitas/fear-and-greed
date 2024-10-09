import pandas as pd
from statsmodels.tsa.stattools import adfuller
from typing import Literal


def adf_test(
    series: pd.Series, reg: Literal["c", "ct", "ctt", "n"] = "c", interpret: bool = True
) -> dict:
    """
    Perform Augmented Dickey-Fuller test on a pandas Series.

    Parameters
    ----------
    series : pd.Series
        The time series data to test.

    reg : str, optional
        - c: constant only
        - ct: constant and trend
        - ctt: constant, trend, and quadratic
        - n: no constant or trend

        Default is "c".

    interpret : bool, optional
        Whether to interpret the p-value. Default is True.

    Returns
    -------
    dict :
        A dictionary containing the ADF statistic, p-value, and critical values.
    """
    result = adfuller(series.dropna(), regression=reg)

    if interpret:
        if result[1] < 0.05:
            print("The time series is stationary (reject the null hypothesis).\n")
        else:
            print(
                "The time series is non-stationary (fail to reject the null hypothesis).\n"
            )
    return {
        "regression": reg,
        "ADF Statistic": result[0],
        "p-value": result[1],
        "Critical Values": result[4],
    }
