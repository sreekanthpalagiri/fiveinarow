import requests
import json
import numpy as np
import configparser
import time
import atexit

#read configuration
config = configparser.ConfigParser()
config.read('properties.ini')

def exit_handler():
    if gamestarted:
        response = requests.post(config['URL']['end'])
        print(response.content)
    print ('Ending your Terminal')
    
atexit.register(exit_handler)

#Take Player Name as input
playername = input('Please enter your name:  ')

#initialize
parameters={"playername":playername}
response = requests.post(config['URL']['initialize'], params=parameters)
respjson=response.json()

if not respjson['response']:
    print('Two Players are already connected, Please connect back later')
    gamestarted=False
    exit()

gamestarted=True
player=respjson['playernum']
print('You are connected to the game, your Player Number: '+str(player))
    
#initialize
if player==1:
    print('Waiting for second player to Join')
    url=config['URL']['ready']
    response = requests.get(url)
    respjson=response.json()
    while not respjson['status']:
        response = requests.get(url)
        respjson=response.json()
        time.sleep(1)
    print('Player 2 Joined, Starting the Game.. You get the first move')
else:
    print('Starting the Game.. your oppenent gets the first move.. Please wait for your move')


urlnextmoveof=config['URL']['nextmoveof']
response = requests.get(urlnextmoveof)
respjson=response.json()
moveof=respjson['moveof']

urlmove=config['URL']['move']
urlboard=config['URL']['board']
gameend=False

while not gameend:
    while not moveof==player:
        response = requests.get(urlnextmoveof)
        respjson=response.json()
        moveof=respjson['moveof']
        time.sleep(1)
        if respjson['compflag']:
            break
    
    response = requests.get(urlboard)
    respjson=response.json()
    gameend=respjson["complete"]

    if gameend:
        winner=respjson["winner"]
        if winner == player:
            text = 'You Win' 
        elif winner ==-1:
                text='You Opponent Disconnected, Ending Game'
        elif winner ==0:
            text='No Moves Left'
        else:
            text=  'Opponent Wins'

        print("End of Game, {}".format(text))
        exit()

    if moveof==player:
        print(np.array(respjson["board"]))
        move=input("It's your turn {}, Enter Column(0-5) and Row(0-8) as X Y:  ".format(playername))
        move = move.split()
        validmove=False
        while not validmove:
            if len(move)==2 and int(move[0]) < 6 and int(move[1]) < 9 and respjson["board"][int(move[0])][int(move[1])]==' ':
                validmove=True
            else:
                move=input("Invalid Move, Enter Column and Row as X Y:  ")
                move = move.split()
        
        parameters={"x":int(move[0]),"y":int(move[1])}
        response = requests.post(urlmove, params=parameters)
        respjson=response.json()
        print("Board after your move:")
        print(np.array(respjson["board"]))
        gameend=respjson["complete"]
        if not gameend:
            print("Waiting for your opponent to make his move.")
            moveof=-1
        else:
            winner=respjson["winner"]
            if winner == player:
                text = 'You Win' 
            elif winner ==-1:
                text='You Opponent Disconnected, Ending Game'
            elif winner ==0:
                text='No Moves Left'
            else:
                text=  'Opponent Wins'

            print("End of Game, {}".format(text))
            exit()

