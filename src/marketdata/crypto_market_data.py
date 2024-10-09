import pickle


class CryptoMarketData:

    def __init__():
        pass

    def iqr_cleaning(self):
        # Implement IQR cleaning logic here
        pass

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