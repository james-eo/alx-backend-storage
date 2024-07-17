#!/usr/bin/env python3
"""
Web cache module for caching web pages and tracking access.
"""

import requests
import redis
from typing import Callable

redis_client = redis.Redis()


def cache_page(expiration: int):
    """
    Decorator to cache web pages with expiration.

    Args:
        expiration (int): Expiration time in seconds.
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(url: str) -> str:
            # Check if the page is already cached
            cached_page = redis_client.get(url)
            if cached_page:
                return cached_page.decode('utf-8')

            result = func(url)
            redis_client.setex(url, expiration, result)
            return result
        return wrapper
    return decorator


def track_access(func: Callable) -> Callable:
    """
    Decorator to track the number of times a URL is accessed.
    """
    def wrapper(url: str) -> str:
        redis_client.incr(f"count:{url}")
        return func(url)
    return wrapper


@cache_page(expiration=10)
@track_access
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a URL and track its access.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"
    print(get_page(url))  # Fetch and cache the page
    print(redis_client.get(f"count:{url}"))  # Print the access count
