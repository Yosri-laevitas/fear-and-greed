import json
import csv
import os

import json
import pandas as pd

def json_to_csv(json_path: str, items_csv_path: str, meta_csv_path: str) -> None:
    """
    Convert a JSON file to CSV for 'items' and 'meta' data.
    
    Parameters
    ----------
    json_path : str
        The path to the JSON file.
    items_csv_path : str
        The path to save the 'items' data CSV file.
    meta_csv_path : str 
        The path to save the 'meta' data CSV file.

    Returns
    -------
    None: 
        Saves the 'items' and 'meta' data to CSV files.

    Raises
    ------
    FileNotFoundError : 
        If the JSON file does not exist.
    json.JSONDecodeError : 
        If the JSON file contains an invalid JSON encoding.
    """
    try:
        # Load the JSON data
        with open(json_path, 'r') as file:
            data = json.load(file)
        
        # Parse 'items' into a DataFrame
        items_df = pd.DataFrame(data.get('items', []))
        
        # Parse 'meta' into a DataFrame (single row)
        meta_df = pd.DataFrame([data.get('meta', {})])
        
        # Save both DataFrames to CSV
        items_df.to_csv(items_csv_path, index=False)
        meta_df.to_csv(meta_csv_path, index=False)

        print(f"Items and meta data have been successfully saved to {items_csv_path} and {meta_csv_path} respectively.")
    except FileNotFoundError:
        print(f"Error: The file {json_path} does not exist.")
    except json.JSONDecodeError:
        print("Error: Failed to parse JSON file. Please check the file's format.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

