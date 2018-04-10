from classes import *
import cards

class Game():

    def __init__(self):

        self.player1=Player(self)
        self.player2=Player(self)

        self.turn=self.player2

        

    def print(self):
        

        print("Player 1 - {}".format(self.player1.health))
        for card in self.player1.board.cards:
            print(card)
        print("Player 2 - {}".format(self.player2.health))
        for card in self.player2.board.cards:
            print(card)

    def end_turn(self):
        queued=[]
        
        for card in self.turn.board.cards:
            queued.append(card.on_end_of_turn)

        for effect in queued:
            effect()

        self.turn=self.turn.opponent()

        queued=[]
        for card in self.turn.board.cards:
            queued.append(card.on_end_of_turn)

        for effect in queued:
            effect()

        self.turn.draw()

    def fight(self, x, y):

        m1=self.player1.board.cards[x]
        m2=self.player2.board.cards[y]

        m1.fight(m2)
            
            
              


if __name__=="__main__":
    g=Game()
    p1=g.player1
    p2=g.player2
    g.player1.load_deck('deck1.txt')
    g.player2.load_deck('deck1.txt')
