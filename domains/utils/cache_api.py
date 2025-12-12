import asyncio
import functools
from typing import Any, Callable, Dict, Tuple

def cache_api(ttl: int = 10*24*3600):
    """
    Async-safe in-memory cache with TTL.
    Suitable for caching Pydantic models or raw JSON.
    """
    cache: Dict[Any, Tuple[Any, float]] = {}
    lock = asyncio.Lock()

    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            key = (func.__name__, args, tuple(sorted(kwargs.items())))
            now = asyncio.get_running_loop().time()
            
            # Cache hit
            if key in cache:
                print("Cache hit for key:", key)
                value, expires = cache[key]
                if expires > now:
                    return value
            print("Cache miss for key:", key)

            # Cache miss – compute under lock
            async with lock:
                # double-check after waiting for lock
                if key in cache:
                    value, expires = cache[key]
                    if expires > now:
                        return value

                result = await func(*args, **kwargs)
                cache[key] = (result, now + ttl)
                return result

        return wrapper
    
    return decorator
