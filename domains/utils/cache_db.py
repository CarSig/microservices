import time
import functools
from typing import Any, Callable, Dict, Tuple
import asyncio
lock = asyncio.Lock()

def cache_db(ttl: int = 300):
    cache: Dict[Any, Tuple[Any, float]] = {}
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Remove SQLAlchemy Session from args
            filtered_args = tuple(
                arg for arg in args
                if not hasattr(arg, "execute")  # Session-like object
            )
            # Build meaningful key (function name + parameters)
            key = (
                func.__name__,
                filtered_args,
                tuple(sorted(kwargs.items()))
            )
            now = time.time()
            async with lock: 
                if key in cache:
                    value, expires = cache[key]
                    if expires > now:
                        print("Cache hit for key:", key)
                        return value

            print("Cache miss for key:", key)
            result = func(*args, **kwargs)
            async with lock:
                cache[key] = (result, now + ttl)
            return result

        return wrapper
    return decorator
