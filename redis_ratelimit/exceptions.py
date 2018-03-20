

class RateLimiterException(Exception):
    """General Exception"""
    pass


class RateLimited(RateLimiterException):
    """The user exceeded API rate limit"""
    pass
