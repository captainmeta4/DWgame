from classes import *
import cards

class Game():

    def __init__(self):

        self.player1=Player(self)
        self.player2=Player(self)

        self.turn=self.player2

        self.queue=[]
        self.deathbed_queue=[]

    def run(self):

        self.player1.load_deck('deck1.txt')
        self.player2.load_deck('deck2.txt')

    

    def queue_up(self, effect):

        #Deathbed effects come after all other effects

        if effect.__name__ is "deathbed":        
            self.deathbed_queue.append(effect)
        else:
            self.queue.append(effect)

    def execute_queue(self):

        queue=self.queue+self.deathbed_queue
        self.queue=[]
        self.deathbed_queue=[]

        while len(queue)>0:
            queue.pop(0)()


        #it's possible that effects in the queue
        #may have caused new effects to be queued up
        #so this method then calls itself
        if len(self.queue+self.deathbed_queue)>0:
            self.execute_queue()
        

    def print(self):
        

        print("Player 1 - {}".format(self.player1.health))
        for card in self.player1.board.cards:
            print(card)
        print("Player 2 - {}".format(self.player2.health))
        for card in self.player2.board.cards:
            print(card)

    def end_turn(self):
        for card in self.turn.board.cards:
            self.queue_up(card.on_end_of_turn)

        self.execute_queue()

        self.turn=self.turn.opponent()

        for card in self.turn.board.cards:
            self.queue_up(card.on_end_of_turn)

        self.execute_queue()

        self.turn.draw()

    def fight(self, x, y):

        m1=self.player1.board.cards[x]
        m2=self.player2.board.cards[y]

        m1.fight(m2)
            
              


if __name__=="__main__":
    g=Game()
    g.run()
