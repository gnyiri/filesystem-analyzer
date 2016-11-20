import unittest
from .context import util


class TestLogger(unittest.TestCase):
    def test_singleton(self):
        logger_a = util.FSLogger.get_instance()
        logger_b = util.FSLogger.get_instance()
        self.assertEqual(logger_a, logger_b)


if __name__ == '__main__':
    unittest.main()
