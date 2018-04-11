from classes import *

class Brood_Leader_Alpha(Minion):

    def reset_stats(self):
        self.name="Brood Leader Alpha"
        self.text="Warcry: Give your other minions +1 Attack."

        self.rarity=2

        self.cost=4
        self.attack=3
        self.health=3
        self.base_health=3

    def warcry(self):
        for card in self.owner.board.cards:
            if card is not self:
                card.add_attack(1)
                
class Dizi_Rat(Minion):
    def reset_stats(self):

        self.name="Dizi Rat"

        self.rarity=1

        self.cost=1
        self.attack=1
        self.health=1
        self.base_health=1

    def deathbed(self):
        for minion in self.owner.board.cards+self.owner.opponent().board.cards:
            minion.take_damage(1)

class Dominion_Guard(Minion):
    def reset_stats(self):

        self.name="Dominion Guard"
        self.text="Taunt"

        self.rarity=1

        self.cost=2
        self.attack=2
        self.health=2
        self.base_health=2

    def set_traits(self):
        self.taunt=True

class Raging_Raider(Minion):
    def reset_stats(self):

        self.name="Raging Raider"
        self.text="Whenever this takes damage, gain +2 Attack."

        self.rarity=2

        self.cost=4
        self.attack=1
        self.health=5
        self.base_health=5

    def on_take_damage(self):
        self.attack+=2


class Vicious_Broodling(Minion):
    def reset_stats(self):

        self.name="Vicious Broodling"
        self.text="Warcry: Deal 2 damage to the opposing player."

        self.rarity=2

        self.cost=2
        self.attack=2
        self.health=1
        self.base_health=1

    def warcry(self):
        self.owner.opponent().take_damage(2)
