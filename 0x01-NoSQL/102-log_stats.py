#!/usr/bin/env python3
"""
This module provides statistics about Nginx logs stored in MongoDB,
including top 10 IPs
"""

from pymongo import MongoClient


def log_stats():
    """
    Provide statistics about Nginx logs stored in MongoDB,
    including top 10 IPs
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    collection = client.logs.nginx

    num_logs = collection.count_documents({})
    print(f"{num_logs} logs")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    status_check = collection.count_documents(
            {
                "method": "GET",
                "path": "/status"
                }
            )
    print(f"{status_check} status check")

    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]

    print("IPs:")
    for doc in collection.aggregate(pipeline):
        print(f"\t{doc['_id']}: {doc['count']}")


if __name__ == "__main__":
    log_stats()
