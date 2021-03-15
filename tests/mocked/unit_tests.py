import unittest
import unittest.mock as mock
from unittest.mock import patch
import os
import sys

sys.path.append(os.path.abspath('../'))
from app import add_user, new_score
import models

KEY_INPUT = "input"
KEY_EXPECTED = "expected"

INITIAL_USERNAME = "user1"
INITIAL_PLAYERS = ["Player1", "Player2"]

class DeterminePlayersTestCase(unittest.TestCase):
    def setUp(self):
        self.add_one = [
            {
                KEY_INPUT: 'Elijah',
                KEY_EXPECTED: [INITIAL_USERNAME, 'Elijah'],
            },
            {
                KEY_INPUT: 'Elias',
                KEY_EXPECTED: [INITIAL_USERNAME, 'Elijah', 'Elias'],
            },
            {
                KEY_INPUT: 'spectator1',
                KEY_EXPECTED: [INITIAL_USERNAME, 'Elijah', 'Elias', 'spectator1'],
            }
        ]
        
        initial_person = models.Username(username=INITIAL_USERNAME, score=100)    
        self.initial_db_mock = [initial_person]
       
    def mocked_db_session_add(self, username):
        self.initial_db_mock.append(username)
        
    def mocked_db_session_commit(self):
        pass
    
    def mocked_username_query_all(self):
        return self.initial_db_mock
    
    def successfulAdd(self):
        for test in self.add_one:
            with patch('app.db.session.add', self.mocked_db_session_add):
                with patch('app.db.session.commit', self.mocked_db_session_commit):
                    with patch('models.Username.query') as mocked_query:
                        mocked_query.all = self.mocked_username_query_all
                 
                        print(self.initial_db_mock)  
                        
                        actual_result = add_user(test[KEY_INPUT])
                        print(actual_result)
                        expected_result = test[KEY_EXPECTED]
                        print(self.initial_db_mock) 
                        print(expected_result)
                       
                        
                        self.assertEqual(len(actual_result), len(expected_result))
                        self.assertEqual(actual_result[1], expected_result[1])
 
class DetermineScoresTestCase(unittest.TestCase):
    def setUp(self):
        self.new_scores = [
            {
                KEY_INPUT: {'message': 'X', 
                    "playerBase": INITIAL_PLAYERS},
                KEY_EXPECTED: [101, 99],
            }
        ] 
        INITIAL_ARRAY = []
        for user in INITIAL_PLAYERS:
            INITIAL_ARRAY.append(models.Username(username=user, score=100))
            
        self.initial_db_mock = [INITIAL_ARRAY]
        
    def mocked_db_session_filter(self):
        for i in self.initial_db_mock:
            if(i == INITIAL_PLAYERS[0]):
                return i
                
    def mocked_db_session_commit(self):
        pass
      
    
    def successfulChange(self):
        for test in self.new_scores:
            with patch('mocked_db_session_filter', self.mocked_db_session_filter):
                with patch('app.db.session.commit', self.mocked_db_session_commit):
                    print(self.initial_db_mock)  
                            
                    actual_result = new_score(test[KEY_INPUT])
                    print(actual_result)
                    expected_result = test[KEY_EXPECTED]
                    print(self.initial_db_mock) 
                    print(expected_result)
                           
                            
                    self.assertEqual(actual_result, expected_result)
             
            
if __name__ == '__main__':
    unittest.main()