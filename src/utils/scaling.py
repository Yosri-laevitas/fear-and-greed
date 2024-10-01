import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def z_score_normalize(df):
    """
    Normalize data using Z-score normalization.

    Parameters
    ----------
        df : pd.DataFrame
            Input data to normalize.

    Returns
    -------
        np.ndarray or pd.DataFrame : Z-score normalized data.
    """
    scaler = StandardScaler()
    normalized_array = scaler.fit_transform(df)
    normalized_df = pd.DataFrame(normalized_array, columns=df.columns)
    return normalized_df


def min_max_scale(df):
    """
    Normalize data using Min-Max normalization.

    Parameters
    ----------
        df : pd.DataFrame
            Input data to normalize.

    Returns
    -------
        np.ndarray or pd.DataFrame : Z-score normalized data.
    """
    scaler = MinMaxScaler()
    normalized_array = scaler.fit_transform(df)
    normalized_df = pd.DataFrame(normalized_array, columns=df.columns)
    return normalized_df