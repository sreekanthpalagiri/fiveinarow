import requests
import json
import numpy as np
import configparser
import time
import atexit

'''read configuration and load url's'''
config = configparser.ConfigParser()
config.read('properties.ini')
urlready=config['URL']['ready']
urlnextmoveof=config['URL']['nextmoveof']
urlmove=config['URL']['move']
urlboard=config['URL']['board']
    
'''Rest Calls'''
def joingame(playername):
    parameters={"playername":playername}
    response = requests.post(config['URL']['initialize'], params=parameters)
    return response.json()['response'], response.json()['playernum']

def gamereadytobegin():
    response = requests.get(urlready)
    return response.json()['status']

def nextmoveof():
    response = requests.get(urlnextmoveof)
    return response.json()['moveof'],response.json()['compflag']

def getboard():
    response = requests.get(urlboard)
    return response.json()["board"], response.json()["complete"], response.json()["winner"]

def makemove(column,player):
    parameters={"y":int(column),"player":player} 
    response = requests.post(urlmove, params=parameters)
    return response.json()["board"], response.json()["complete"], response.json()["winner"]

'''Method to return final game status message'''
def getgamestatustext():
    if winner == player:
        return 'You Win' 
    elif winner ==-1:
        return 'You Opponent Disconnected, Ending Game'
    elif winner ==0:
        return 'No Moves Left'
    else:
        return 'Opponent Wins'

def waitforyourmove():
    '''Wait for player's move, break if game is complete due player terminal disconnection'''
    moveof=-1
    while not moveof==player:
        time.sleep(1)
        moveof,gamecomp=nextmoveof()
        if gamecomp:
            break

def takenextmoveasinput(board):
    '''Take Columns as input, get index of empty row in the column and check validity'''
    column=int(input("It's your turn {}, please enter column (1-9):  ".format(playername)))-1
    validmove=False
    while not validmove:
        row=len(board[:,column][board[:,column]==' '])-1
        if int(column) >= 0 and int(column) < 10 and row>=0:
            validmove=True
        else:
            column=int(input("Invalid Move, please enter column which has empty grid (1-9):  "))-1
    return column
    
'''Exit Handler, ends game in the server if client disconnects after starting the game.''' 
def exit_handler():
    if gamestarted:
        print('Terminal Disconnect request, ending game.')
        response = requests.post(config['URL']['end'])
    print ('Ending your Terminal')
    
atexit.register(exit_handler)

'''Take Player Name as input'''
playername = input('Please enter your name:  ')
while playername=='':
    playername =input('Please enter your name:  ')

'''initialize and join game, wait for player two to join if you are first player'''
gamejoinsuccess,player = joingame(playername)
if not gamejoinsuccess:
    print('Two Players are already connected, Please connect back later')
    gamestarted=False
    exit()

print('You are connected to the game, your Player Number: '+str(player))
gamestarted=True
if player==1:
    print('Waiting for second player to Join')
    while not gamereadytobegin():
        time.sleep(1)
    print('Player 2 Joined, Starting the Game.. You get the first move')
else:
    print('Starting the Game.. your oppenent gets the first move.. Please wait for your move')

gameend=False
while not gameend:
    '''Wait for your move'''
    waitforyourmove()

    '''Get Status of current board after other player move and show the board, 
    if game ended show the winner and exit'''
    board, gameend, winner=getboard()
    print("Board after your opponent move:\n",np.array(board))
    if gameend:
        print("End of Game, {}".format(getgamestatustext()))
        exit()

    '''Take next move as input'''
    column=takenextmoveasinput(np.array(board))

    '''Make the move, print the latest board'''
    board, gameend, winner=makemove(column,player)
    print("Board after your move:\n",np.array(board))
        
    '''Wait for opponents move or if game is complete, print the winner and exit'''
    if not gameend:
        print("Waiting for your opponent to make his move.")
    else:
        print("End of Game, {}".format(getgamestatustext()))
        exit()