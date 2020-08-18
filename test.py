import unittest 
import json
from server import app

class TestServer(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        print(self.client)

    #Should add player 1
    def test_01(self):
        response = self.client.post('/intialize/?playername=Sreekanth')
        self.assertEqual(200, response.status_code)
        respjson=json.loads(response.get_data(as_text=True))
        self.assertEqual(respjson['response'],True)
        self.assertEqual(respjson['playernum'],1)

    #checking if game ready to start Should return status as ready
    def test_02(self):
        response = self.client.get('/readytostart/')
        self.assertEqual(200, response.status_code)
        respjson=json.loads(response.get_data(as_text=True))
        self.assertEqual(respjson['status'],False)

    #Should add player 2
    def test_03(self):
        response = self.client.post('/intialize/?playername=Palagiri')
        self.assertEqual(200, response.status_code)
        respjson=json.loads(response.get_data(as_text=True))
        self.assertEqual(respjson['response'],True)
        self.assertEqual(respjson['playernum'],2)

    #Should not add player 3
    def test_04(self):
        response = self.client.post('/intialize/?playername=Reddy')
        self.assertEqual(200, response.status_code)
        respjson=json.loads(response.get_data(as_text=True))
        self.assertEqual(respjson['response'],False)

    #checking if game ready to start Should return status as ready
    def test_05(self):
        response = self.client.get('/readytostart/')
        self.assertEqual(200, response.status_code)
        respjson=json.loads(response.get_data(as_text=True))
        self.assertEqual(respjson['status'],True)

    #Checking who has next move, Should return move of player 1 and complete flag as flase
    def test_06(self):
        response = self.client.get('/nextmoveof/')
        self.assertEqual(200, response.status_code)
        respjson=json.loads(response.get_data(as_text=True))
        self.assertEqual(respjson['moveof'],1)
        self.assertEqual(respjson['compflag'],False)

    #Checking status of current board, Should return winner as -1 and complete flag as flase
    def test_07(self):
        response = self.client.get('/currentboard/')
        self.assertEqual(200, response.status_code)
        respjson=json.loads(response.get_data(as_text=True))
        self.assertEqual(respjson['complete'],False)
        self.assertEqual(respjson['winner'],-1)

    #Should post a move for player 1 and winner as -1 and complete flag as false
    def test_08(self):
        response = self.client.post('/move/?x=0&y=0')
        self.assertEqual(200, response.status_code)
        respjson=json.loads(response.get_data(as_text=True))
        self.assertEqual(respjson['complete'],False)
        self.assertEqual(respjson['winner'],-1)
    
    #Should post a move for player 2 and winner as -1 and complete flag as false
    def test_09(self):
        response = self.client.post('/move/?x=2&y=0')
        self.assertEqual(200, response.status_code)
        respjson=json.loads(response.get_data(as_text=True))
        self.assertEqual(respjson['complete'],False)
        self.assertEqual(respjson['winner'],-1)

    #After series of moves, winner is 1 and complete flag as True
    def test_10(self):
        response = self.client.post('/move/?x=0&y=1')
        self.assertEqual(200, response.status_code)
        response = self.client.post('/move/?x=2&y=1')
        self.assertEqual(200, response.status_code)
        response = self.client.post('/move/?x=0&y=3')
        self.assertEqual(200, response.status_code)
        response = self.client.post('/move/?x=2&y=3')
        self.assertEqual(200, response.status_code)
        response = self.client.post('/move/?x=0&y=2')
        self.assertEqual(200, response.status_code)
        response = self.client.post('/move/?x=2&y=2')
        self.assertEqual(200, response.status_code)
        response = self.client.post('/move/?x=0&y=4')
        self.assertEqual(200, response.status_code)
        respjson=json.loads(response.get_data(as_text=True))
        self.assertEqual(respjson['complete'],True)
        self.assertEqual(respjson['winner'],1)

    #Should end Game and return complete and winner
    def test_11(self):
        response = self.client.post('/end/')
        self.assertEqual(200, response.status_code)
        response = self.client.get('/currentboard/')
        self.assertEqual(200, response.status_code)
        respjson=json.loads(response.get_data(as_text=True))
        self.assertEqual(respjson['complete'],True)
        self.assertEqual(respjson['winner'],1)

    #Test for Vertical Completion and Player 2 as winner
    def test_12(self):
        response = self.client.post('/intialize/?playername=Sreekanth')
        self.assertEqual(200, response.status_code)
        respjson=json.loads(response.get_data(as_text=True))
        self.assertEqual(respjson['playernum'],1)
        response = self.client.post('/intialize/?playername=Palagiri')
        self.assertEqual(200, response.status_code)
        respjson=json.loads(response.get_data(as_text=True))
        self.assertEqual(respjson['playernum'],2)
        response = self.client.post('/move/?x=1&y=0')
        self.assertEqual(200, response.status_code)
        response = self.client.post('/move/?x=1&y=2')
        self.assertEqual(200, response.status_code)
        response = self.client.post('/move/?x=3&y=0')
        self.assertEqual(200, response.status_code)
        response = self.client.post('/move/?x=3&y=2')
        self.assertEqual(200, response.status_code)
        response = self.client.post('/move/?x=2&y=0')
        self.assertEqual(200, response.status_code)
        response = self.client.post('/move/?x=2&y=2')
        self.assertEqual(200, response.status_code)
        response = self.client.post('/move/?x=4&y=5')
        self.assertEqual(200, response.status_code)
        response = self.client.post('/move/?x=4&y=2')
        self.assertEqual(200, response.status_code)
        response = self.client.post('/move/?x=5&y=0')
        self.assertEqual(200, response.status_code)
        response = self.client.post('/move/?x=5&y=2')
        self.assertEqual(200, response.status_code)
        respjson=json.loads(response.get_data(as_text=True))
        self.assertEqual(respjson['complete'],True)
        self.assertEqual(respjson['winner'],2)
        response = self.client.post('/end/')
        self.assertEqual(200, response.status_code)

    #Test for diagnal right to left Completion and Player 1 as winner
    def test_13(self):
        response = self.client.post('/intialize/?playername=Sreekanth')
        self.assertEqual(200, response.status_code)
        respjson=json.loads(response.get_data(as_text=True))
        self.assertEqual(respjson['playernum'],1)
        response = self.client.post('/intialize/?playername=Palagiri')
        self.assertEqual(200, response.status_code)
        respjson=json.loads(response.get_data(as_text=True))
        self.assertEqual(respjson['playernum'],2)
        response = self.client.post('/move/?x=5&y=5')
        self.assertEqual(200, response.status_code)
        response = self.client.post('/move/?x=1&y=3')
        self.assertEqual(200, response.status_code)
        response = self.client.post('/move/?x=3&y=3')
        self.assertEqual(200, response.status_code)
        response = self.client.post('/move/?x=4&y=3')
        self.assertEqual(200, response.status_code)
        response = self.client.post('/move/?x=4&y=4')
        self.assertEqual(200, response.status_code)
        response = self.client.post('/move/?x=0&y=2')
        self.assertEqual(200, response.status_code)
        response = self.client.post('/move/?x=2&y=2')
        self.assertEqual(200, response.status_code)
        response = self.client.post('/move/?x=0&y=8')
        self.assertEqual(200, response.status_code)
        response = self.client.post('/move/?x=1&y=1')
        self.assertEqual(200, response.status_code)
        respjson=json.loads(response.get_data(as_text=True))
        self.assertEqual(respjson['complete'],True)
        self.assertEqual(respjson['winner'],1)
        response = self.client.post('/end/')
        self.assertEqual(200, response.status_code)

    #Test for diagnal left to right Completion and Player 2 as winner
    def test_14(self):
        response = self.client.post('/intialize/?playername=Sreekanth')
        self.assertEqual(200, response.status_code)
        respjson=json.loads(response.get_data(as_text=True))
        self.assertEqual(respjson['playernum'],1)
        response = self.client.post('/intialize/?playername=Palagiri')
        self.assertEqual(200, response.status_code)
        respjson=json.loads(response.get_data(as_text=True))
        self.assertEqual(respjson['playernum'],2)
        response = self.client.post('/move/?x=1&y=0')
        self.assertEqual(200, response.status_code)
        response = self.client.post('/move/?x=5&y=0')
        self.assertEqual(200, response.status_code)
        response = self.client.post('/move/?x=3&y=0')
        self.assertEqual(200, response.status_code)
        response = self.client.post('/move/?x=4&y=1')
        self.assertEqual(200, response.status_code)
        response = self.client.post('/move/?x=2&y=0')
        self.assertEqual(200, response.status_code)
        response = self.client.post('/move/?x=2&y=3')
        self.assertEqual(200, response.status_code)
        response = self.client.post('/move/?x=4&y=5')
        self.assertEqual(200, response.status_code)
        response = self.client.post('/move/?x=3&y=2')
        self.assertEqual(200, response.status_code)
        response = self.client.post('/move/?x=5&y=5')
        self.assertEqual(200, response.status_code)
        response = self.client.post('/move/?x=1&y=4')
        self.assertEqual(200, response.status_code)
        respjson=json.loads(response.get_data(as_text=True))
        self.assertEqual(respjson['complete'],True)
        self.assertEqual(respjson['winner'],2)
        response = self.client.post('/end/')
        self.assertEqual(200, response.status_code)

if __name__ == '__main__':
    unittest.main()