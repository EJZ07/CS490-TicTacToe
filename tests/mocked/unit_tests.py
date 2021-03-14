import unittest
import unittest.mock as mock
from unittest.mock import patch
import os
import sys

sys.path.append(os.path.abspath('../'))
from app import add_user
import models

KEY_INPUT = "input"
KEY_EXPECTED = "expected"

INITIAL_USERNAME = "user1"

class DeterminePlayersTestCase(unittest.TestCase):
    def setUp(self):
        self.add_one = [
            {
                KEY_INPUT: 'Elijah',
                KEY_EXPECTED: [INITIAL_USERNAME, 'Elijah'],
            },
            ]
    
    def successfulAdd(self):
        for test in self.add_one:
            actual_result = add_user(test[KEY_INPUT])
            expected_result = test[KEY_EXPECTED]
            
            self.assertEqual(len(actual_result), len(expected_result))
            self.assertEqual(actual_result[1], expected_result[1])
            
            
if __name__ == '__main__':
    unittest.main()