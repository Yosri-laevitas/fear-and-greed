from pymongo import MongoClient
from typing import Literal

type = "futures"
coin = "btc"


def get_futures(
    coin: Literal["BTC", "ETH"], type: Literal["futures", "options", "perpetuals"]
) -> list:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["laevitas"]
    collection = db[type]

    query = {"currency": {"$regex": coin}, "$expr": {"$eq": [{"$hour": "$date"}, 0]}}
    projection = {"currency": 1, "date": 1, "points.0": 1}
    results = collection.find(query, projection).limit(10)

    client.close()

    return list(results)
