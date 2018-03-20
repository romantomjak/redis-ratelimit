from functools import wraps

from redis_ratelimit.exceptions import RateLimited
from redis_ratelimit.utils import is_rate_limited


def ratelimit(rate, key, redis_url='redis://localhost:6379/0'):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if is_rate_limited(rate, key, f, redis_url):
                raise RateLimited("Too Many Requests")
            return f(*args, **kwargs)
        return decorated_function
    return decorator
