import numpy as np
import random
import Functionality as Functionality
#import Tableality
from datetime import time
from matplotlib import pyplot as plt

#TODO PROJECT KEYSTROKELOGGER (Sahanav):
#Create a Game.awardInput(time1, time2, input1, input2)
class Game:
    
    def __init__(self,player1, player2):
        #self.playerWithTurnNumber = 1
        self.player1:Player = player1
        self.player2:Player = player2
        #self.player3 = player3
        #self.player4 = player4
        self.pot:int = 0
        self.myFunction:Functionality.Function = None
        self.myCorrectAnswer = -1 #0 is left, 1 is right, 2 is midpoint, 3 is trapezoidal
        self.start = 0
        self.end = 5
        self.step = 0.25
        self.currentBet:int = int(np.average([self.player1.points,self.player2.points])/10)
    def readyPlayers(self): #sets the player id and myGame attribute
        self.player1.setId(1)
        self.player2.setId(2)
        #self.player3.setId(3)
        #self.player4.setId(4)
        self.player1.setMyGame(self)
        self.player2.setMyGame(self)
        #self.player3.setMyGame(self)
        #self.player4.setMyGame(self)
    def generateFunction(self, degree:int):
        self.myFunction = Functionality.Function(np.randn(degree+1), degree)
    def setRandomCorrectAnswer(self):
        self.myCorrectAnswer = random.randint(0,3)
    #Precondition: setRandomCorrectAnswer() and generateFunction(degree) must have been called before this method is called
    def plot(self):
        self.myFunction.plot()
        match(self.myCorrectAnswer):
            case 0:
                Functionality.leftRectangleCreator(self.myFunction, self.step, self.start, self.end)
            case 1:
                Functionality.rightRectangleCreator(self.myFunction, self.step, self.start, self.end)
            case 2:
                Functionality.midpointRectangleCreator(self.myFunction, self.step, self.start, self.end)
            case 3:
                Functionality.trapezoidCreator(self.myFunction, self.step, self.start, self.end)
    def isRightAnswer(self,choice:int):
        return choice == self.myCorrectAnswer
    def addPointsToPot(self, amount:float):
        self.pot += amount
    def clearTheBoard(self):
        plt.clf()
    def makeNewBet(self): #Sets the current bet to a new random integer
        if self.player1.points < self.player2.points:
            self.currentBet = random.randint(1, self.player1.points)
        else:
            self.currentBet = random.randint(1, self.player2.points)
        
    #Preconditions: plot(), generateFunction(degree), and setRandomCorrectAnswer() have all ran before awardInput(time1, time2, input1, input2)
    #Parameters: time1 is a time object of class time that represents when player1 buzzed in, time2 is a time object of class time that represents when player2 buzzed in
    #input1 is an integer on [0,3] that represents the answer of player1, input2 is an integer on [0,3] that represents the answer of player2
    def awardInput(self, time1=time, time2=time, input1=int, input2=int):
        isOneCorrect = self.isRightAnswer(input1)
        isTwoCorrect = self.isRightAnswer(input2)
        areBothCorrect = isOneCorrect and isTwoCorrect
        if areBothCorrect:
            if time1 < time2:
                self.player1.receivePoints(self.pot)
                self.pot = 0
            elif time1 > time2:
                self.player2.receivePoints(self.pot)
                self.pot = 0
            else:
                self.player1.receivePoints(int(self.pot/2))
                self.player2.receivePoints(int(self.pot/2))
                self.pot = 0
        if isOneCorrect and (not areBothCorrect):
            self.player1.receivePoints(self.pot)
            self.pot = 0
        elif isTwoCorrect and (not areBothCorrect):
            self.player2.receivePoints(self.pot)
            self.pot = 0
    def isWinnerReached(self): #returns the player who has won if a winner was reached, False otherwise
        if self.player1.points == 0:
            return self.player2
        elif self.player2.points == 0:
            return self.player1
        else:
            return False    
class Player:
    def __init__(self, name:str): #Constructor for class Player. The parameter name is the player's name.
        self.name = name
        self.id = 0 #the player's turn in the game
        self.points = 100 #how many points the player has
        self.myGame = None
    def setId(self, newId:int): #Sets the player id to newId
        self.id = newId
    def setMyGame(self, myGame:Game): #Sets the myGame attribute of the player to myGame parameter.
        self.myGame = myGame
    #Precondition: myGame must be set
    def betPoints(self, amount:int):
        if(self.points <= amount):
            raise "Too many points bet!"
        else:
            self.points -= amount
        
            self.myGame.addPointsToPot(amount)
    def receivePoints(self, amount:int):
        self.points += amount
    
    
        
game = Game(Player("me"), Player("you"))