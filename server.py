from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import numpy as np
import time

app = Flask(__name__)
api = Api(app)

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

    def mark(self,y,player):
        x=len(game.gameframe[:,y][game.gameframe[:,y]==' '])-1
        if int(y) >= 0 and int(y) < 10 and x>=0 and self.turn==player:
            self.move+=1
            if self.turn==1:
                self.turn=2
                self.gameframe[x,y]='X'
            else:
                self.turn=1
                self.gameframe[x,y]='0'      
            self.iscomplete(x,y)
            return True
        else:
            return False  

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
        

class gametasks(Resource):

    def get(self,what):
        if what=='board':
            return jsonify({"board": game.gameframe.tolist(),"complete":game.compflag,"winner":game.winner})
        elif what=='gamestartstatus':
            if game.noplayers==2:
                print('Initial Board:')
                print(game.gameframe)
                return jsonify({ "status":True})
            else:
                return jsonify({ "status":False})
        elif what=='nextmoveof':
            return jsonify({ "moveof":game.turn,"compflag":game.compflag})
        else:
            return 'Invalid Request',404

    def post(self,what):
        if what=='AddPlayer':
            name = request.args.get('playername')
            print('Intializing... Request from Player '+name)
            playerstatus=game.addplayer(name)
            return playerstatus
        elif what=='Move':
            status=game.mark(int(request.args.get('y')),int(request.args.get('player')))
            print('Current Board:')
            print(game.gameframe)
            print('Next Move of:',game.turn)
            return  jsonify({"board": game.gameframe.tolist(),"complete":game.compflag,"winner":game.winner,"status":status}) 
        elif what=='Endgame':
            game.endgame()
            return 'Game Ended'
        else:
            return 'Invalid Request',404

game=fiveinarow((6,9))
api.add_resource(gametasks, '/5inarow/<what>')

if __name__ == '__main__':
    app.run(debug=True)