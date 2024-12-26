import time
from functools import wraps

def ttl_cache(ttl: int):
    """
    Decorator to implement a simple TTL cache for a function.
    
    Args:
        ttl (int): Time-to-live in seconds for the cache.

    Returns:
        A wrapped function with TTL caching.
    """
    def decorator(func):
        cache = {}
        
        @wraps(func)
        def wrapped(*args, **kwargs):
            # Create a cache key based on function arguments
            key = (args, frozenset(kwargs.items()))
            current_time = time.time()
            
            # Check if the key is in the cache and still valid
            if key in cache:
                value, expiration = cache[key]
                if current_time < expiration:
                    return value

            # Recompute and update the cache
            value = func(*args, **kwargs)
            cache[key] = (value, current_time + ttl)
            return value

        return wrapped

    return decorator