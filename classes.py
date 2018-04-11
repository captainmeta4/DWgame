import random

class Card():

    _nonce=1

    def __init__(self, name="", owner=None):
        self.owner=owner

        #assign card id
        self.id=Card._nonce
        Card._nonce+=1

        #find specific card and change class to adopt card stats and effects
        if name:
            self.__class__= eval("cards."+name.replace(" ","_"))
            

        self.reset_stats()
        self.default_traits()
        self.set_traits()

    def __str__(self):
        output="({}) {}/{} {}".format(self.cost, self.attack,self.health, self.name)
        if self.text:
            output+=" - {}".format(self.text)
        return output

    def reset_stats(self):
        raise Exception("stats not defined for this card")


    def is_type(self, s):
        if self.type==s:
            return True
        else:
            return False
    

class Minion(Card):

    def warcry(self, target=None):
        pass

    def deathbed(self):
        pass

    def on_start_of_turn(self):
        pass

    def on_end_of_turn(self):
        pass

    def on_take_damage(self):
        pass

    def on_deal_damage(self, target):
        pass

    def default_traits(self):
        self.taunt=False
        self.pending_destroy=False
        self.type="None"

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
        elif x<0:
            raise(ValueError("x must be 0 or greater"))

        if x==0:
            return
        
        self.owner.game.queue_up(self.on_take_damage)

        self.health = max(self.health-x, 0)
        
        if self.health==0:
            self.die()
            return


    def die(self):
        self.owner.board.cards.remove(self)
        self.owner.graveyard.add(self)
        self.owner.game.queue_up(self.deathbed)

    def fight(self, target):

        self_attack=self.attack
        target_attack=target.attack

        self.take_damage(target_attack)
        target.take_damage(self_attack)
        

        self.owner.game.execute_queue()


class Spell(Card):

    def effect(self, target=None):
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

    def add(self, card):
        self.cards.append(card)
        
class Graveyard():

    def __init__(self, owner):
        self.cards=[]
        self.owner=owner

    def print(self):
        for card in self.cards:
            print(card)

    def add(self, card):
        self.cards.append(card)


class Player():

    def __init__(self, game):

        self.game=game

        self.hand=Hand(self)
        self.deck=Deck(self)
        self.attack=0
        self.health=40
        self.base_health=40
        self.board=Board(self)
        self.graveyard=Graveyard(self)

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

    def summon(self, card):
        self.cards.append(card)



