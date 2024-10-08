from pymongo import MongoClient
from typing import Literal, Optional
from datetime import datetime


def transform_data(input_data: dict) -> dict:
    # Extract values from the input data
    points = input_data.get("points", {})

    # Create the new dictionary structure
    output_data = {
        "_id": input_data["_id"],
        "date": input_data["date"],
        "currency": input_data["currency"],
        "price": points.get("0", {}).get("p"),  # Extracting price
        "open_interest": points.get("0", {}).get("oi"),  # Extracting open interest
        "volume": points.get("0", {}).get("v"),  # Extracting volume
        "basis": points.get("0", {}).get("b"),  # Extracting basis
        "yield": points.get("0", {}).get("y"),  # Extracting yield
    }

    return output_data


def get_data(
    coin: Literal["BTC", "ETH"],
    type: Literal["futures", "options", "perpetuals"],
    start: Optional[str] = None,
    end: Optional[str] = None,
    limit: Optional[int] = None,
) -> list:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["laevitas"]
    collection = db[type]

    # Create the base query for currency and hour
    query = {
        "currency": {"$regex": coin},
        "$expr": {"$eq": [{"$hour": "$date"}, 0]},
    }

    # Add date range filter if start and end dates are provided
    if start:
        query["date"] = {"$gte": datetime.fromisoformat(start)}
    if end:
        query.setdefault("date", {})["$lte"] = datetime.fromisoformat(end)

    projection = {"currency": 1, "date": 1, "points.0": 1}

    if limit is not None:
        results = collection.find(query, projection).limit(limit)
    else:
        results = collection.find(query, projection)

    return [transform_data(res) for res in list(results)]
