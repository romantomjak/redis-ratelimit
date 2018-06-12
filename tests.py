import time
import unittest
import uuid

from redis_ratelimit.decorators import ratelimit
from redis_ratelimit.exceptions import RateLimited
from redis_ratelimit.utils import parse_rate


def random_key():
    return uuid.uuid4()


class RateParsingTests(unittest.TestCase):
    def test_rate_parsing(self):
        tests = (
            ('100/s', (100, 1)),
            ('100/10s', (100, 10)),
            ('100/m', (100, 60)),
            ('400/10m', (400, 10 * 60)),
            ('600/h', (600, 60 * 60)),
            ('800/d', (800, 24 * 60 * 60)),
        )

        for input, output in tests:
            assert output == parse_rate(input)


class DecoratorTests(unittest.TestCase):

    def setUp(self):
        self.key = random_key()

    def test_view(self):
        @ratelimit(rate='5/s', key=self.key)
        def view():
            return True

        assert view()

    def test_rate_limit_exception(self):
        @ratelimit(rate='5/s', key=self.key)
        def view():
            return True

        for _ in range(5):
            view()

        with self.assertRaises(RateLimited):
            view()

    def test_rate_limit_groups(self):
        @ratelimit(rate='10/m', key=self.key)
        @ratelimit(rate='5/s', key=self.key)
        def view():
            return True

        with self.assertRaises(RateLimited):
            for _ in range(6):
                view()

        time.sleep(1)

        for _ in range(4):
            view()

        with self.assertRaises(RateLimited):
            view()


if __name__ == '__main__':
    unittest.main()
