#!/usr/bin/env python3
"""Web caching and tracking module"""

import redis
import requests
from functools import wraps
from typing import Callable

redis_client = redis.Redis()


def cache_and_track(expiration_time: int = 10) -> Callable:
    """Decorator to cache the page and track access count"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str) -> str:
            redis_client.incr(f"count:{url}")

            cached_page = redis_client.get(f"cache:{url}")
            if cached_page:
                return cached_page.decode('utf-8')

            page_content = func(url)

            redis_client.setex(f"cache:{url}", expiration_time, page_content)

            return page_content
        return wrapper
    return decorator


@cache_and_track()
def get_page(url: str) -> str:
    """Fetch a web page and return its content"""
    response = requests.get(url)
    return response.text
