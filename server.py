from flask import Flask, jsonify, request
import numpy as np
import time

app = Flask(__name__)
players=0

class player:
    def __init__(self,name):
        self.name=name

class fiveinarow:
    def __init__(self,shape):
        self.gameframe=np.chararray(shape,unicode=True)
        self.dimx=shape[0]
        self.dimy=shape[1]
        self.gameon=False
        self.noplayers=0
    
    def initializenewgame(self):
        self.gameframe[:]=' '
        self.move=0
        self.turn=1
        self.winner=-1
        self.compflag=False
        self.gameon=True

    def addplayer(self,name):
        if self.noplayers==2:
            return jsonify({ "message":"Two players have already connected", 
            'response':False,"playernum":-1})
        
        self.noplayers=self.noplayers+1
        
        if self.noplayers==1:
            self.initializenewgame()
            self.player1=player(name)
            return jsonify({ "message":"Connected, Waiting for Player 2 to join", 
            'response':True,"playernum":1})
        else:
            self.player2=player(name)
            return jsonify({ "message":"Connected", 
            'response':True,"playernum":2})

    def mark(self,x,y):
        self.move+=1
        if self.turn==1:
            self.turn=2
            self.gameframe[x,y]='X'
        else:
            self.turn=1
            self.gameframe[x,y]='0'      
        self.iscomplete(x,y)  

    def checkhor(self,x,y):
        #Check Horizontal Completion
        cell=self.gameframe[x,y]
        horcounter=4
        for i in range(1,horcounter+1):
            if y-i<0: 
                break
            if cell==self.gameframe[x,y-i]:
                horcounter-=1
            else:
                break
        
        for i in range(1,horcounter+1):
            if y+i>self.dimy-1:
                break   
            if cell==self.gameframe[x,y+i]:
                horcounter-=1
            else:
                break
        
        if horcounter==0:
            return True
        else:
            return False

    def checkver(self,x,y):
        #Check Vertical Completion
        cell=self.gameframe[x,y]
        vercounter=4
        for i in range(1,vercounter+1):
            if x-i<0:
                break
            if cell==self.gameframe[x-i,y]:
                vercounter-=1
            else:
                break
        for i in range(1,vercounter+1):
            if x+i>self.dimx-1:
                break
            if cell==self.gameframe[x+i,y]:
                vercounter-=1
            else:
                break
        if vercounter==0:
            return True
        else:
            return False     

    def checkdiagltr(self,x,y):
        cell=self.gameframe[x,y]
        diagcntr=4
        for i in range(1,diagcntr+1):
            if x-i<0 or y-i<0:
                break
            if cell==self.gameframe[x-i,y-i]:
                diagcntr-=1
            else:
                break
        for i in range(1,diagcntr+1):
            if x+i>self.dimx-1 or y+i>self.dimy-1:
                break
            if cell==self.gameframe[x+i,y+i]:
                diagcntr-=1
            else:
                break
        if diagcntr==0:
            return True
        else:
            return False   
        
    def checkdiagrtl(self,x,y):
        cell=self.gameframe[x,y]
        diagcntr=4
        for i in range(1,diagcntr+1):
            if x+i>self.dimx-1 or y-i<0:
                break
            if cell==self.gameframe[x+i,y-i]:
                diagcntr-=1
            else:
                break
        for i in range(1,diagcntr+1):
            if x-i<0 or y+i>self.dimy-1:
                break
            if cell==self.gameframe[x-i,y+i]:
                diagcntr-=1
            else:
                break
        if diagcntr==0:
            return True
        else:
            return False

    def iscomplete(self,x,y):
        if self.checkhor(x,y) or self.checkver(x,y) or self.checkdiagltr(x,y) or self.checkdiagrtl(x,y):
            self.compflag=True
            if self.turn==1:
                self.winner=2
            else:
                self.winner=1
        if np.count_nonzero(self.gameframe == ' ')==0:
            self.compflag=True
            self.winner=0

    def endgame(self): 
        self.gameon=False
        self.noplayers=0
        self.compflag=True
        print('Ending Game')
        

@app.route('/intialize/', methods=['POST'])
def intialize():
    name = request.args.get('playername')
    print('Intializing... Request from Player'+name)
    playerstatus=game.addplayer(name)
    return playerstatus

@app.route('/readytostart/', methods=['GET'])
def readytostart():
    if game.noplayers==2:
        print('Initial Board Board:')
        print(game.gameframe)
        return jsonify({ "status":True})
    else:
        return jsonify({ "status":False})

@app.route('/nextmoveof/', methods=['GET'])
def nextmoveof():
    print('Wating for move of:',game.turn)
    return jsonify({ "moveof":game.turn,"compflag":game.compflag})

@app.route('/end/', methods=['POST'])
def end():
    game.endgame()
    return 'Game Ended'

@app.route('/move/', methods=['POST'])
def move():
    game.mark(int(request.args.get('x')),int(request.args.get('y')))
    print('Current Board:')
    print(game.gameframe)
    print('Next Move of:',game.turn)
    return  jsonify({"board": game.gameframe.tolist(),"complete":game.compflag,"winner":game.winner}) 

@app.route('/currentboard/', methods=['GET'])
def currentboard():
    return jsonify({"board": game.gameframe.tolist(),"complete":game.compflag,"winner":game.winner})


game=fiveinarow((6,9))

if __name__ == '__main__':
    app.run(debug=True)