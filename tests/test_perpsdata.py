import unittest
import pandas as pd
import os
import pickle
from src.marketdata import PerpetualsData


class TestPerpetualsData(unittest.TestCase):
    def setUp(self):
        """
        This function is called before each test case to set up common test conditions.
        """
        # Initialize test data
        self.currency = "BTC"
        self.start_date = "2024-10-01"
        self.end_date = "2024-10-03"
        self.granularity = "1d"
        self.file_name = "test_perp_data.pkl"

        # Create PerpetualsData object
        self.perp_data = PerpetualsData(
            self.currency, self.start_date, self.end_date, self.granularity
        )

    def test_initialization(self):
        """Test if the object initializes correctly and fetches data."""
        self.assertEqual(self.perp_data.currency, self.currency)
        self.assertEqual(self.perp_data.start, self.start_date)
        self.assertEqual(self.perp_data.end, self.end_date)
        self.assertEqual(self.perp_data.granularity, self.granularity)

        # Test that historical data is fetched (based on known data structure)
        self.assertIsInstance(self.perp_data.historical_data, pd.DataFrame)
        self.assertEqual(len(self.perp_data.historical_data.columns), 9)
        self.assertFalse(self.perp_data.historical_data.empty)

    def test_currency_setter(self):
        """Test changing the currency."""
        self.perp_data.currency = "ETH"
        self.assertEqual(self.perp_data.currency, "ETH")

        # Check if historical data is updated (based on new currency)
        self.assertIsInstance(self.perp_data.historical_data, pd.DataFrame)
        self.assertTrue(
            any("ETH" in symbol for symbol in self.perp_data.historical_data["symbol"]),
            "ETH not found in symbol column.",
        )
        self.assertFalse(self.perp_data.historical_data.empty)

    def test_start_setter(self):
        """Test changing the start date."""
        # Test updating start date to a later date
        new_start = "2024-10-02"
        self.perp_data.start = new_start
        self.assertEqual(self.perp_data.start, new_start)
        self.assertTrue(all(self.perp_data.historical_data["date"] >= new_start))

        # Test setting an earlier start date
        prior_length = len(self.perp_data.historical_data)
        earlier_start = "2024-09-30"
        self.perp_data.start = earlier_start
        self.assertEqual(self.perp_data.start, earlier_start)
        self.assertTrue(len(self.perp_data.historical_data) > prior_length)

    def test_end_setter(self):
        """Test changing the end date."""
        # Test updating end date to an earlier date
        new_end = "2024-10-02"
        self.perp_data.end = new_end
        self.assertEqual(self.perp_data.end, new_end)
        self.assertTrue(all(self.perp_data.historical_data["date"] <= new_end))

        # Test setting a later end date
        prior_length = len(self.perp_data.historical_data)
        later_end = "2024-10-05"
        self.perp_data.end = later_end
        self.assertEqual(self.perp_data.end, later_end)
        self.assertTrue(len(self.perp_data.historical_data) > prior_length)

    def test_granularity_setter(self):
        """Test changing the granularity."""
        new_granularity = "12h"
        prior_length = len(self.perp_data.historical_data)
        self.perp_data.granularity = new_granularity
        self.assertEqual(self.perp_data.granularity, new_granularity)

        # Ensure historical data is updated accordingly
        self.assertIsInstance(self.perp_data.historical_data, pd.DataFrame)
        self.assertFalse(self.perp_data.historical_data.empty)
        self.assertTrue(len(self.perp_data.historical_data) > prior_length)

    def tearDown(self):
        """
        Clean up any generated files after each test case.
        """
        if os.path.exists(self.file_name):
            os.remove(self.file_name)

    def test_save_method(self):
        """
        Test that the save method works correctly and adds .pkl if not present.
        """
        self.perp_data.save(self.file_name[:-4])  # Test without .pkl extension
        self.assertTrue(os.path.exists(self.file_name))  # Check file exists
        with open(self.file_name, "rb") as f:
            loaded_data = pickle.load(f)
        self.assertEqual(
            loaded_data.currency, self.perp_data.currency
        )  # Check that the data is saved correctly

    def test_load_method(self):
        """
        Test that the load method works correctly and loads the saved object.
        """
        self.perp_data.save(self.file_name)
        loaded_perp_data = PerpetualsData.load(self.file_name)

        self.assertEqual(loaded_perp_data.currency, self.perp_data.currency)
        self.assertEqual(loaded_perp_data.start, self.perp_data.start)
        self.assertEqual(loaded_perp_data.end, self.perp_data.end)
        self.assertEqual(loaded_perp_data.granularity, self.perp_data.granularity)

    def test_save_load_without_extension(self):
        """
        Test save and load methods when file_name does not have .pkl extension.
        """
        file_name_no_extension = "test_perp_data"
        self.perp_data.save(file_name_no_extension)
        self.assertTrue(os.path.exists(file_name_no_extension + ".pkl"))

        loaded_perp_data = PerpetualsData.load(file_name_no_extension)
        self.assertEqual(loaded_perp_data.currency, self.perp_data.currency)


if __name__ == "__main__":
    unittest.main()
