#!/usr/bin/env python3
"""Module that inserts a new document in a collection"""
from pymongo import MongoClient


def insert_school(mongo_collection, **kwargs):
    """Insert a new document in a collection"""
    return mongo_collection.insert_one(kwargs).inserted_id
