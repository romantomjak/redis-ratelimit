import re

import redis

from redis_ratelimit.exceptions import RateLimiterException

rate_re = re.compile('([\d]+)/([\d]*)([smhd])')

UNITS = {
    's': 1,
    'm': 60,
    'h': 60 * 60,
    'd': 24 * 60 * 60
}


def parse_rate(rate):
    try:
        count, factor, unit = rate_re.match(rate).groups()
        count = int(count)
        seconds = UNITS[unit.lower()]
        if factor:
            seconds *= int(factor)
        return count, seconds
    except ValueError:
        raise RateLimiterException("Invalid rate value")


def is_rate_limited(rate, key, func, redis_url):
    if not rate:
        return False

    count, seconds = parse_rate(rate)
    redis_key = "{}/{}/{}".format(key, func.__name__, count, seconds)

    r = redis.from_url(redis_url)

    current = r.get(redis_key)
    if current:
        current = int(current.decode('utf-8'))
        if current >= count:
            return True

    value = r.incr(redis_key)
    if value == 1:
        r.expire(redis_key, seconds)

    return False
