import pickle
import pandas as pd
import numpy as np
import copy

class CryptoMarketData:
    def __init__(self):
        pass

    def z_score_cleaning(self, threshold: float = 3.0):
        """
        Winsorizes outliers from all numerical columns in the DataFrame using the Z-score method.

        Parameters
        ----------
        self.historical_data : pd.DataFrame
            The input DataFrame from which outliers need to be removed.
        threshold : float, optional
            The Z-score threshold above which data points are considered outliers (default is 3.0).

        Returns
        -------
        None

        """
        numerical_cols = self.historical_data.select_dtypes(include=[np.number]).columns

        for column in numerical_cols:
            # Compute the mean and standard deviation of the column
            mean_col = self.historical_data[column].mean()
            std_col = self.historical_data[column].std()

            # Calculate Z-scores
            self.historical_data[f'{column}_z_score'] = (self.historical_data[column] - mean_col) / std_col

            # Winsorize the outliers (clamp the values within the threshold)
            self.historical_data[column] = np.where(
                self.historical_data[f'{column}_z_score'] > threshold, 
                mean_col + threshold * std_col, 
                np.where(
                    self.historical_data[f'{column}_z_score'] < -threshold, 
                    mean_col - threshold * std_col, 
                    self.historical_data[column]
                )
            )

        # Drop the Z-score columns after winsorizing
        self.historical_data.drop(columns=[f'{col}_z_score' for col in numerical_cols], inplace=True)
        
        return self

    def interpolate_missing_values(self):
        # Implement interpolation logic here
        pass

    def save(self, file_name: str) -> None:
        if not file_name.endswith(".pkl"):
            file_name += ".pkl"
        with open(file_name, "wb") as f:
            pickle.dump(self, f)
        print(f"PerpetualsData object saved to {file_name}")

    @classmethod
    def load(cls, file_name: str):
        if not file_name.endswith(".pkl"):
            file_name += ".pkl"
        with open(file_name, "rb") as f:
            perp_data = pickle.load(f)
        print(f"PerpetualsData object loaded from {file_name}")
        return perp_data

    def copy(self):
        return copy.deepcopy(self)