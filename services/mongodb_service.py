from pymongo import MongoClient
from typing import Literal, Optional
from datetime import datetime

type = "futures"
coin = "btc"


def get_futures(
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
        "currency": {"$regex": coin, "$options": "i"},
        "$expr": {"$eq": [{"$hour": "$date"}, 0]},
    }

    # Add date range filter if start and end dates are provided
    if start:
        query["date"] = {
            "$gte": datetime.fromisoformat(start)
        }  # Assuming ISO format for input
    if end:
        query.setdefault("date", {})["$lte"] = datetime.fromisoformat(end)

    projection = {"currency": 1, "date": 1, "points.0": 1}

    if limit is not None:
        results = collection.find(query, projection).limit(limit)
    else:
        results = collection.find(query, projection)

    client.close()

    return list(results)
