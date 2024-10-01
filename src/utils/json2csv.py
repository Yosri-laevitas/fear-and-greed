import json
import csv
import os

def json_to_csv(json_file_path, csv_file_path):
    """
    Convert a JSON file to a CSV file.

    Parameters
    ----------
        json_file_path : str
            The path to the input JSON file.
        csv_file_path : str 
            The path where the output CSV file will be saved.
    Returns
    -------
        None
    Raises
    ------
        FileNotFoundError
            If the JSON file does not exist.
        ValueError
            If the JSON data is not a list of dictionaries or a single dictionary.

    """
    # Check if the JSON file exists
    if not os.path.exists(json_file_path):
        raise FileNotFoundError(f"The file {json_file_path} does not exist.")

    # Read the JSON data from the file
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Check if data is a list of dictionaries
    if isinstance(data, dict):
        # If the JSON data is a dictionary, convert it to a list of dictionaries
        data = [data]

    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise ValueError("JSON data must be a list of dictionaries or a single dictionary.")

    # Extract the header from the keys of the first dictionary
    header = data[0].keys()

    # Write to the CSV file
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)

    print(f"Successfully converted {json_file_path} to {csv_file_path}.")
