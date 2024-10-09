import pandas as pd
from statsmodels.tsa.stattools import adfuller

def adf_test(series: pd.Series, interpret: bool = True) -> dict:
    """
    Perform Augmented Dickey-Fuller test on a pandas Series.

    Parameters
    ----------
    series : pd.Series
        The time series data to test.
    interpret : bool, optional
        Whether to interpret the p-value. Default is True.

    Returns
    -------
    dict :
        A dictionary containing the ADF statistic, p-value, and critical values.
    """
    result = adfuller(series.dropna())

    if interpret:
        if result[1] < 0.05:
            print(
                "The time series is stationary (reject the null hypothesis)."
            )
        else:
            print(
                "The time series is non-stationary (fail to reject the null hypothesis)."
            )
    return {
        "ADF Statistic": result[0],
        "p-value": result[1],
        "Critical Values": result[4],
    }