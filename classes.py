import random


class Card():

    def __init__(self, name="", owner=None):
        self.owner=owner
        if name:
            self.__class__= eval("cards."+name.replace(" ","_"))
            

        self.reset_stats()
        self.default_traits()
        self.set_traits()
        self.set_type()

    def __str__(self):
        output="({}) {}/{} {}".format(self.cost, self.attack,self.health, self.name)
        if self.text:
            output+=" - {}".format(self.text)
        return output

    def reset_stats(self):
        raise Exception("stats not defined for this card")

    def set_type(self):
        self.type=None #intended to be overridden

    def is_type(self, s):
        if self.type==s:
            return True
        else:
            return False
    

class Minion(Card):

    def warcry(self, target=None):
        pass

    def deathcry(self):
        pass

    def on_start_of_turn(self):
        pass

    def on_end_of_turn(self):
        pass

    def default_traits(self):
        self.taunt=False
        self.pending_destroy=False

        self.set_traits()

    def set_traits(self):
        pass

    def add_health(self, x):
        if type(x) is not int:
            raise(TypeError("x must be an integer"))
        elif x<1:
            raise(ValueError("x must be 1 or greater"))
        
        self.health += x
        self.base_health += x

    def restore_health(self, x):
        if type(x) is not int:
            raise(TypeError("x must be an integer"))
        elif x<1:
            raise(ValueError("x must be 1 or greater"))
        
        if self.health + x > self.base_health:
            self.health=self.base_health
        else:
            self.health += x
        
    def add_attack(self, x):
        if type(x) is not int:
            raise(TypeError("x must be an integer"))

        if self.attack + x < 0:
            self.attack=0
        else:
            self.attack += x

    def set_health(self, x):
        if type(x) is not int:
            raise(TypeError("x must be an integer"))
        self.health=x
        self.base_Health=x

    def set_attack(self, x):
        if type(x) is not int:
            raise(TypeError("x must be an integer"))
        self.attack=x
        
    def take_damage(self, x):
        if type(x) is not int:
            raise(TypeError("x must be an integer"))
        elif x<1:
            raise(ValueError("x must be 1 or greater"))

        self.health -= x

    def fight(self, target):

        target.take_damage(self.attack)
        self.take_damage(target.attack)

        queued=[]
        
        for minion in [self,target]:
            if minion.health <=0:
                minion.reset_stats()
                minion.owner.board.cards.remove(minion)
                queued.append(minion.deathcry)
                minion.owner.graveyard.append(minion)
        for effect in queued:
            effect()

class Spell(Card):
    pass

import cards

class Deck():
    
    def __init__(self, owner):
        self.cards=[]
        self.owner=owner
        self.fatigue=1

    def insert(self, card):
        self.cards.append(card)
        random.shuffle(self.cards)

    def draw(self):
        if len(self.cards)>=1:
            return self.cards.pop()
        else:
            self.owner.take_damage(self.fatigue)
            self.fatigue+=1
            return None

    def shuffle(self):
        random.shuffle(self.cards)

    def validate(self):

        if len(self.cards) > 40:
            raise ValueError("Deck has over 40 cards")

        counts={}

        for card in self.cards:
            if card.name not in counts:
                counts[card.name]=1
            else:
                counts[card.name]+=1

            if counts[card.name]>(5-card.rarity):
                msg="Too many copies of {}. Only {} are allowed".format(card.name, str(5-card.rarity))
                raise ValueError(msg)
                
        

        

class Hand():
    def __init__(self, owner):
        self.cards=[]
        self.owner=owner

    def print(self):
        for card in self.cards:
            print(card)
        
        


class Player():

    def __init__(self, game):

        self.game=game

        self.hand=Hand(self)
        self.deck=Deck(self)
        self.attack=0
        self.health=40
        self.base_health=40
        self.board=Board(self)
        self.graveyard=[]

    def opponent(self):

        if self.game.player1 is self:
            return self.game.player2
        elif self.game.player2 is self:
            return self.game.player1

    def play(self, x):

        card=self.hand.cards[x]
        if not self.board.can_play:
            return

        if card.owner is not self:
            raise ValueError("That's not your card!")
        
        self.hand.cards.remove(card)
        self.board.play(card)

    def draw(self):
        card=self.deck.draw()

        if len(self.hand.cards)<10 and card is not None:
            self.hand.cards.append(card)
            print("{}".format(card))
        elif card is None:
            print("Fatigued!")
        else:
            print('Burned: {}'.format(card))

    def draw_x(self, x):
        if type(x) is not int:
            raise(TypeError("x must be an integer"))
        elif x<1:
            raise(ValueError("x must be 1 or greater"))

        for i in range(x):
            self.draw()
        

    def take_damage(self, x):
        if type(x) is not int:
            raise(TypeError("x must be an integer"))
        elif x<1:
            raise(ValueError("x must be 1 or greater"))

        self.health -= x

    def restore_health(self, x):
        if type(x) is not int:
            raise(TypeError("x must be an integer"))
        elif x<1:
            raise(ValueError("x must be 1 or greater"))
        
        if self.health + x > self.base_health:
            self.health=self.base_health
        else:
            self.health += x

    def load_deck(self, file):
        self.deck.cards=[]
        with open(file) as f:
            for line in f:
                self.deck.cards.append(Card(line.strip(), self))
        self.deck.validate()
        self.deck.shuffle()
        
class Board():

    def __init__(self, owner):

        self.cards=[]
        self.owner=owner

    def can_play(self):
        if len(self.cards)>5:
            return False
        else:
            return True

    def play(self, card):
        self.cards.append(card)
        card.warcry()



