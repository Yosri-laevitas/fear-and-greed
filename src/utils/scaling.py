import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def z_score_normalize(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize numerical columns of pd.DataFrame object using Z-score normalization.

    Parameters
    ----------
    df : pd.DataFrame
        Input data to normalize.

    Returns
    -------
    pd.DataFrame : DataFrame with Z-score normalized numerical columns.
    """
    numerical_cols = df.select_dtypes(include=['number']).columns
    scaler = StandardScaler()
    normalized_array = scaler.fit_transform(df[numerical_cols])
    normalized_df = pd.DataFrame(normalized_array, columns=numerical_cols, index=df.index)
    df[numerical_cols] = normalized_df
    
    return df


def min_max_scale(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize numerical columns of pd.DataFrame object using Min-Max normalization.

    Parameters
    ----------
    df : pd.DataFrame
        Input data to normalize.

    Returns
    -------
    pd.DataFrame : DataFrame with Min-Max normalized numerical columns.
    """
    numerical_cols = df.select_dtypes(include=['number']).columns
    scaler = MinMaxScaler()
    normalized_array = scaler.fit_transform(df[numerical_cols])
    normalized_df = pd.DataFrame(normalized_array, columns=numerical_cols, index=df.index)
    df[numerical_cols] = normalized_df
    
    return df
