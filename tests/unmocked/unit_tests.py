'''
This program tests for cases in app.py
'''

import unittest

KEY_INPUT = 'input'
KEY_EXPECTED = 'expected'
KEY_REMOVE = 'Jason'
KEY_LENGTH = 'length'

name_arr = ['Elijah', 'John', 'Wong', 'Jason', 'Chris']

class nameArrayTests(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                 KEY_INPUT: ['Elijah', 'John', 'Wong', 'Jason', 'Chris'],
                 KEY_EXPECTED: ['Elijah', 'John', 'Wong', 'Chris'],
             }
            ]
            
        self.unchanged_test_params = [
            {
                 KEY_INPUT: ['Elijah', 'John', 'Wong', 'Jason', 'Chris'],
                 KEY_EXPECTED: ['Elijah', 'John', 'Wong', 'Jason', 'Chris'],
            }
    
            ]
            
        self.empty_test_params = [
            {
                 KEY_INPUT: ['Elijah', 'John', 'Wong', 'Jason', 'Chris'],
                 KEY_EXPECTED: []
            }
    
            ]
            
    def correctArray(self):
        for test in self.success_test_params:
            
            actual_result = test[KEY_INPUT]
            actual_result.remove(KEY_REMOVE)
            expected_result = test[KEY_EXPECTED]
            
            self.assertEqual(len(actual_result), len(expected_result))
            self.assertEqual(actual_result[3], expected_result[3])
    
    def unchangedArray(self):
        for test in self.unchanged_test_params:
            
            actual_result = test[KEY_INPUT]
            actual_result.remove(KEY_REMOVE)
            expected_result = test[KEY_EXPECTED]
            
            self.assertNotEqual(len(actual_result), len(expected_result))
            self.assertNotEqual(actual_result[3], expected_result[3])
    
    def emptyArray(self):
        for test in self.empty_test_params:
            
            actual_result = test[KEY_INPUT]
            actual_result.remove(KEY_REMOVE)
            expected_result = test[KEY_EXPECTED]
            
            self.assertNotEqual(len(actual_result), len(expected_result))
    
class playerSizeTests(unittest.TestCase):
    def setUp(self):
        self.players_are_assigned = [
            {
                 KEY_INPUT: ['Elijah'],
                 KEY_EXPECTED: [1],
             },
             {
                 KEY_INPUT: ['Elijah', 'Elias'],
                 KEY_EXPECTED: [1, 2],
             },
             {
                 KEY_INPUT: ['Elijah', 'John', 'Wong', 'Jason', 'Chris'],
                 KEY_EXPECTED: [1, 2, 3],
             }
            ]
        
        self.more_than_one_emit = [
            {
                 KEY_INPUT: ['Elijah'],
                 KEY_EXPECTED: [1],
             },
             {
                 KEY_INPUT: ['Elijah', 'Elias', 'James'],
                 KEY_EXPECTED: [1, 2],
             },
             {
                 KEY_INPUT: ['Elijah', 'John', 'Wong', 'Jason', 'Chris'],
                 KEY_EXPECTED: [1, 2, 3],
             }
            ]
        
        self.no_player_numbers = [
             {
                 KEY_INPUT: ['Elijah'],
                 KEY_EXPECTED: [],
             },
             {
                 KEY_INPUT: ['Elijah', 'Elias'],
                 KEY_EXPECTED: [],
             },
             {
                 KEY_INPUT: ['Elijah', 'Elias', 'Wong', 'Jason', 'Chris'],
                 KEY_EXPECTED: [],
             }
            ]
    
    def playersCorrect(self):
        player_array = []
        for test in self.players_are_assigned:
            
            name_array = test[KEY_INPUT]
            playerSize = len(name_array)
            
            if (playerSize == 1):
                playerType = 1
                player_array.append(playerType)
            elif (playerSize == 2):
                playerType = 2
                player_array.append(playerType)
            elif (playerSize > 2):
                playerType = 3
                player_array.append(playerType)
                
            expected_result = test[KEY_EXPECTED]
            
            self.assertEqual(player_array, expected_result)
            
    def tooManyPlayers(self):
        player_array = []
        for test in self.more_than_one_emit:
            
            name_array = test[KEY_INPUT]
            playerSize = len(name_array)
            
            if (playerSize == 1):
                playerType = 1
                player_array.append(playerType)
            elif (playerSize == 2):
                playerType = 2
                player_array.append(playerType)
            elif (playerSize > 2):
                playerType = 3
                player_array.append(playerType)
                
            expected_result = test[KEY_EXPECTED]
            
            self.assertNotEqual(player_array, expected_result)
    
    def lenNotDetermined(self):
        player_array = []
        for test in self.no_player_numbers:
            
            name_array = test[KEY_INPUT]
            playerSize = len(name_array)
            
            if (playerSize == 1):
                playerType = 1
                player_array.append(playerType)
            elif (playerSize == 2):
                playerType = 2
                player_array.append(playerType)
            elif (playerSize > 2):
                playerType = 3
                player_array.append(playerType)
                
            expected_result = test[KEY_EXPECTED]
            
            self.assertNotEqual(player_array, expected_result)
            self.assertNotEqual(len(player_array), len(expected_result))

class determineScoreTests(unittest.TestCase):
    def setUp(self):
        self.players_are_assigned = [
            {
                 KEY_INPUT: ['X', ['Elijah', 'John', 'Wong', 'Jason', 'Chris']],
                 KEY_EXPECTED: [101, 99],
            },
            {
                 KEY_INPUT: ['O', ['Elijah', 'John', 'Wong', 'Jason', 'Chris']],
                 KEY_EXPECTED: [100, 100],
             }, 
             
            ]
        
        self.reversedScores = [
            {
                 KEY_INPUT: ['X', ['Elijah', 'John', 'Wong', 'Jason', 'Chris']],
                 KEY_EXPECTED: [99, 101],
            },
            ]
            
        self.infiniteScores = [
            {
                 KEY_INPUT: ['X', ['Elijah', 'John', 'Wong', 'Jason', 'Chris']],
                 KEY_EXPECTED: [999, 99],
            },
            {
                 KEY_INPUT: ['O', ['Elijah', 'John', 'Wong', 'Jason', 'Chris']],
                 KEY_EXPECTED: [99, 999],
            },
            ]
    
    def correctScores(self):
        score_array = [100, 100]
        
        for test in self.players_are_assigned:
            message = test[KEY_INPUT]
            if (message[0] == 'X'):
                score_array[0] += 1
                score_array[1] -= 1
            elif (message[0] == 'O'):
                score_array[1] += 1
                score_array[0] -= 1
                
            expected_result = test[KEY_EXPECTED]
            
            self.assertEqual(score_array, expected_result)
    
    def wrongScores(self):
        score_array = [100, 100]
        
        for test in self.reversedScores:
            message = test[KEY_INPUT]
            if (message[0] == 'X'):
                score_array[0] += 1
                score_array[1] -= 1
            elif (message[0] == 'O'):
                score_array[1] += 1
                score_array[0] -= 1
                
            expected_result = test[KEY_EXPECTED]
            
            self.assertEqual(score_array, expected_result)
    
    def multipleScoreChanges(self):
        score_array = [100, 100]
        
        for test in self.reversedScores:
            message = test[KEY_INPUT]
            if (message[0] == 'X'):
                score_array[0] += 1
                score_array[1] -= 1
            elif (message[0] == 'O'):
                score_array[1] += 1
                score_array[0] -= 1
                
            expected_result = test[KEY_EXPECTED]
            
            self.assertEqual(score_array, expected_result)
    
if __name__ == '__main__':
    unittest.main()