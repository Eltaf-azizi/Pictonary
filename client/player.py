"""
Represent the player(s) in each game
"""

class Player(object):
    def __init__(self, name):
        self.name = name
        self.score = 0

    
    def updatescore(self, x):
        self.score += x


    def getscore(self):
        return self.score
    

    def getname(self):
        return self.name