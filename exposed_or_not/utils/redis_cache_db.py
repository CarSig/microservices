import json
import hashlib
import inspect
from config import config


def redis_cache_db(ttl: int = 300):
    redisDB = config.REDIS.CLIENT
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Skip Redis in tests
            if config.TESTING:
                return await func(*args, **kwargs)
            filtered_args = tuple(
                a for a in args
                if not hasattr(a, "execute") and not hasattr(a, "query")
            )
            raw_key = (
                func.__name__,
                filtered_args,
                tuple(sorted(kwargs.items()))
            )     
            key = "cache:" + hashlib.sha256(
                json.dumps(raw_key, default=str).encode()
            ).hexdigest()
            cached = await redisDB.get(key)
            if cached is not None:
                print("Redis HIT:", key)
                return json.loads(cached)
            print("Redis MISS:", key)
            # Run function (async or sync)
            if inspect.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
            await redisDB.set(
                key, json.dumps(result, default=str), ex=ttl
            )
            return result
        return wrapper
    return decorator
