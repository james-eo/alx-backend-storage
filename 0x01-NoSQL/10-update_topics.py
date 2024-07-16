#!/usr/bin/env python3
"""Module that changes all topics of a school document"""
from pymongo import MongoClient


def update_topics(mongo_collection, name, topics):
    """Change all topics of a school document based on the name"""
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    school_collection = client.my_db.school
    update_topics(
            school_collection,
            "Holberton school",
            ["Sys admin", "AI", "Algorithm"])
