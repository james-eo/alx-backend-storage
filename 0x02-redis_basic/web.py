#!/usr/bin/env python3
"""Web caching and tracking module"""

import redis
import requests
import time
from typing import Callable

redis_client = redis.Redis()


def get_page(url: str) -> str:
    """
    Fetch a web page, cache it, and track access count.

    Args:
        url (str): The URL of the web page to fetch.

    Returns:
        str: The content of the web page.
    """
    count_key = f"count:{url}"
    redis_client.incr(count_key)

    cache_key = f"cache:{url}"
    cached_page = redis_client.get(cache_key)

    if cached_page:
        return cached_page.decode('utf-8')

    response = requests.get(url)
    page_content = response.text

    redis_client.setex(cache_key, 10, page_content)

    return page_content


if __name__ == "__main__":
    url = "http://google.com"
    print(get_page(url))
    print(f"{redis_client.get(f'count:{url}').decode('utf-8')} times")

    print("Sleeping for 5 seconds...")
    time.sleep(5)
    print("Accessing again (should be cached):")
    print(get_page(url))

    print("Sleeping for 6 more seconds...")
    time.sleep(6)
    print("Accessing again (should not be cached):")
    print(get_page(url))
