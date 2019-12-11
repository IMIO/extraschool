import unittest

from datetime import date
from helper import usefull


class unittest_check_age(unittest.TestCase):


    def test_age_from_birthdate(self):
        self.assertEqual(5, 6)
    #
    # def test_birthdate_from_age(self):
    #     pass


if __name__ == '__main__':
    unittest.main()
