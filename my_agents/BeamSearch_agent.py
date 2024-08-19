import random
import copy
import numpy as np
import math
import sys
 
# ------------------------------------------------------------
# Player information
# ------------------------------------------------------------
class Player:
    def __init__(self, hp, mana, cards_remaining, rune, draw):
        self.hp = hp
        self.mana = mana
        self.cards_remaining = cards_remaining  # the number of cards in the player's deck
        self.rune = rune  # the next remaining rune of a player
        self.draw = draw  # the additional number of drawn cards

# ------------------------------------------------------------
# Card information
# ------------------------------------------------------------
class Card:
    def __init__(self, card_id, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw):
        self.card_id = card_id
        self.instance_id = instance_id
        self.location = location
        self.card_type = card_type
        self.cost = cost
        self.attack = attack
        self.defense = defense
        self.abilities = abilities
        self.my_health_change = my_health_change
        self.opponent_health_change = opponent_health_change
        self.card_draw = card_draw
        self.breakthrough = False
        self.charge = False
        self.drain = False
        self.guard = False
        self.lethal = False
        self.ward = False
        for c in abilities:
            if c == 'B': self.breakthrough = True
            if c == 'C': self.charge = True
            if c == 'D': self.drain = True
            if c == 'G': self.guard = True
            if c == 'L': self.lethal = True
            if c == 'W': self.ward = True

    def value(self):
        value = 0
        value += self.attack + self.defense
        if self.breakthrough:
            value += 2
        if self.charge:
            value += 1
        if self.drain:
            value += 2
        if self.guard:
            value += 2
        if self.lethal:
            value += 2
        if self.ward:
            value += 2
        return value

# ------------------------------------------------------------
# Draft class
# ------------------------------------------------------------
class Draft:
    def __init__(self):
        self.picked_card_type = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.prefer_card_type = [5, 4, 4, 3, 3, 3, 2, 2, 2, 2]

        self.TYPE_CREATURE = 0
        self.TYPE_GREEN = 1
        self.TYPE_RED = 2
        self.TYPE_BLUE = 3

    def pick_card(self, cards):
        best_card = self.select_bestcard(cards)
        if cards[best_card].card_type == self.TYPE_CREATURE and cards[best_card].cost < 2:
            self.picked_card_type[0] += 1
        elif cards[best_card].card_type == self.TYPE_CREATURE and cards[best_card].cost < 3:
            self.picked_card_type[1] += 1
        elif cards[best_card].card_type == self.TYPE_CREATURE and cards[best_card].cost < 4:
            self.picked_card_type[2] += 1
        elif cards[best_card].card_type == self.TYPE_CREATURE and cards[best_card].cost < 5:
            self.picked_card_type[3] += 1
        elif cards[best_card].card_type == self.TYPE_CREATURE and cards[best_card].cost < 6:
            self.picked_card_type[4] += 1
        elif cards[best_card].card_type == self.TYPE_CREATURE and cards[best_card].cost < 7:
            self.picked_card_type[5] += 1
        elif cards[best_card].card_type == self.TYPE_CREATURE:
            self.picked_card_type[6] += 1
        elif cards[best_card].card_type == self.TYPE_GREEN:
            self.picked_card_type[7] += 1
        elif cards[best_card].card_type == self.TYPE_RED:
            self.picked_card_type[8] += 1
        else:
            self.picked_card_type[9] += 1

        return best_card

    # ------------------------------------------------------------
    # Algorithm to select the best card.
    # First select the card with more abilities.
    # If all cards have the same number of abilities: random
    # It is random, but the types (on picked_card_type) with more gaps are more probables
    def select_bestcard(self, l_cards):
        l_percent = []
        for card in l_cards:
            if card.card_type == self.TYPE_CREATURE:
                if card.cost < 2:
                    p = self.prefer_card_type[0] - self.picked_card_type[0]
                elif card.cost < 3:
                    p = self.prefer_card_type[1] - self.picked_card_type[1]
                elif card.cost < 4:
                    p = self.prefer_card_type[2] - self.picked_card_type[2]
                elif card.cost < 5:
                    p = self.prefer_card_type[3] - self.picked_card_type[3]
                elif card.cost < 6:
                    p = self.prefer_card_type[4] - self.picked_card_type[4]
                elif card.cost < 7:
                    p = self.prefer_card_type[5] - self.picked_card_type[5]
                else:
                    p = self.prefer_card_type[6] - self.picked_card_type[6]
                if card.guard:
                    p += 6
            elif card.card_type == self.TYPE_GREEN:
                p = self.prefer_card_type[7] - self.picked_card_type[7]
            elif card.card_type == self.TYPE_RED:
                p = self.prefer_card_type[8] - self.picked_card_type[8]
            else:
                p = self.prefer_card_type[9] - self.picked_card_type[9]

            if p < 0:
                p = 0
            l_percent.append(p)
        if np.sum(l_percent) == 0:
            n = random.randint(0, 2)
        else:
            result = random.uniform(0, np.sum(l_percent))
            if result <= l_percent[0]:
                n = 0
            elif result <= (l_percent[0] + l_percent[1]):
                n = 1
            else:
                n = 2
        return n
   
# ------------------------------------------------------------
# State information
# ------------------------------------------------------------
class State:
    def __init__(self, player1, player2, opponent_hand, l_opponent_actions, l_cards):
        self.player1 = player1
        self.player2 = player2
        self.opponent_hand = opponent_hand
        self.l_opponent_actions = l_opponent_actions
        self.l_cards = l_cards

        self.LOCATION_IN_HAND = 0
        self.LOCATION_PLAYER_SIDE = 1
        self.LOCATION_OPPONENT_SIDE = -1

        self.TYPE_CREATURE = 0
        self.TYPE_GREEN = 1
        self.TYPE_RED = 2
        self.TYPE_BLUE = 3

        self.l_actions = []
        self.l_turn = []                       # Added declaration

        self.l_cards_on_player_hand = []       # list of cards on player hand
        self.l_cards_on_player_board = []      # list of cards on the player board
        self.l_guard_creatures_on_player_hand = []  # list of guard creatures on player hand
        self.l_charger_creatures_on_player_hand = []  # list of charger creatures on player hand
        self.l_breakthrough_creatures_on_player_hand = []  # list of breakthrough creatures on player hand
        self.l_drain_creatures_on_player_hand = [] # list of drain creatures on player hand
        self.l_lethal_creatures_on_player_hand = [] # list of lethal creatures on player hand
        self.l_ward_creatures_on_player_hand = []  # list of ward creatures on player hand

        self.l_green_objects_on_player_hand = []  # list of green objects on player hand
        self.l_blue_objects_on_player_hand = []  # list of blue objects on player hand
        self.l_red_objects_on_player_hand = []  # list of red objects on player hand

        self.l_player_cards_guard = []         # list of guard cards on player board
        self.l_player_cards_lethal = []        # list of lethal cards on player board
        self.l_player_cards_drain = []         # list of drain cards on player board
        self.l_player_cards_breakthrough = []  # list of breakthrough cards on player board
        self.l_player_cards_charger = []       # list of charger cards on player
        self.l_player_cards_ward = []          # list of ward cards on player board

        self.l_cards_on_opponent_board = []    # list of cards on the opponent board
        self.l_opponent_cards_guard = []       # list of guard cards on opponent board
        self.l_opponent_cards_lethal = []      # list of lethal cards on opponent board
        self.l_opponent_cards_drain = []       # list of drain cards on opponent board
        self.l_opponet_cards_breakthrough = [] # list of breakthrough cards on opponent board
        self.l_opponent_cards_charger = []     # list of charger cards on opponent board
        self.l_opponent_cards_ward = []        # list of ward cards on opponent board

        self.l_cards_can_attack = []           # list of cards that can attack

        self.cover = False # True if the player has a guard card on the board
        if not self.is_draft_phase():
            self.classify_cards()
    
    # ---------------------------------------
    # Classify each card in the corresponding list (only if cost <= player mana)
    # Can attack cards on the players lane (already summoned)
    # Can be summoned criatures on the hand
    # Can be used items on the hand
    def classify_cards(self):
        for card in self.l_cards:
            if card.location == self.LOCATION_IN_HAND:
                if card.card_type == self.TYPE_CREATURE:
                    self.l_cards_on_player_hand.append(card)
                    if card.guard:
                        self.l_guard_creatures_on_player_hand.append(card)
                    if card.charge:
                        self.l_charger_creatures_on_player_hand.append(card)
                    if card.breakthrough:
                        self.l_breakthrough_creatures_on_player_hand.append(card)
                    if card.drain:
                        self.l_drain_creatures_on_player_hand.append(card)
                    if card.lethal:
                        self.l_lethal_creatures_on_player_hand.append(card)
                    if card.ward:
                        self.l_ward_creatures_on_player_hand.append(card)
                elif card.card_type == self.TYPE_GREEN:
                    self.l_green_objects_on_player_hand.append(card)
                elif card.card_type == self.TYPE_RED:
                    self.l_red_objects_on_player_hand.append(card)
                elif card.card_type == self.TYPE_BLUE:
                    self.l_blue_objects_on_player_hand.append(card)
            elif card.location == self.LOCATION_PLAYER_SIDE:
                self.l_cards_on_player_board.append(card)
                self.l_cards_can_attack.append(card)
                if card.guard:
                    self.l_player_cards_guard.append(card)
                    self.cover = True
                if card.lethal:
                    self.l_player_cards_lethal.append(card)
                if card.drain:
                    self.l_player_cards_drain.append(card)
                if card.breakthrough:
                    self.l_player_cards_breakthrough.append(card)
                if card.charge:
                    self.l_player_cards_charger.append(card)
                if card.ward:
                    self.l_player_cards_ward.append(card)
            elif card.location == self.LOCATION_OPPONENT_SIDE:
                self.l_cards_on_opponent_board.append(card)
                if card.guard:
                    self.l_opponent_cards_guard.append(card)
                if card.lethal:
                    self.l_opponent_cards_lethal.append(card)
                if card.drain:
                    self.l_opponent_cards_drain.append(card)
                if card.breakthrough:
                    self.l_opponet_cards_breakthrough.append(card)
                if card.charge:
                    self.l_opponent_cards_charger.append(card)
                if card.ward:
                    self.l_opponent_cards_ward.append(card)
    # ---------------------------------------
    # return true is the game is in the draft phase
    def is_draft_phase(self):
        return self.player1.mana == 0
    
    # ---------------------------------------
    # return the value of the cards on the player board
    def player_cardvalue(self):
        value = 0
        for c in self.l_cards_on_player_board:
            value += c.value()
        return value

    # ---------------------------------------
    # return the value of the cards on the opponent board
    def opponent_cardvalue(self):
        value = 0
        for c in self.l_cards_on_opponent_board:
            value += c.value()
        return value

# ------------------------------------------------------------
# Summon strategies class
# ------------------------------------------------------------
class SummonAll:
    def __init__(self, state):
        self.state :State = state
        self.l_turn = []
        self.get_turn()

    def get_turn(self):
        l_cards_can_summon_after = []
        while len(self.state.l_cards_on_player_hand) > 0:
            c = self.state.l_cards_on_player_hand[0]
            if c.cost > self.state.player1.mana:
                self.state.l_cards_on_player_hand.remove(c)
                continue
            if c.card_type == self.state.TYPE_CREATURE and len(self.state.l_cards_on_player_board) >= 6:
                l_cards_can_summon_after.append(c)
                self.state.l_cards_on_player_hand.remove(c)
                continue
            elif c.card_type == self.state.TYPE_CREATURE:
                self.summon(c)
            else:
                self.state.l_cards_on_player_hand.remove(c)
        self.state.l_cards_on_player_hand = l_cards_can_summon_after

    def summon(self, c):
        self.l_turn.append("SUMMON " + str(c.instance_id) + ";")
        if c.charge:
            self.state.l_cards_can_attack.append(c)
            self.state.l_player_cards_charger.append(c)
            self.state.l_charger_creatures_on_player_hand.remove(c)
        if c.breakthrough:
            self.state.l_player_cards_breakthrough.append(c)
            self.state.l_breakthrough_creatures_on_player_hand.remove(c)
        if c.drain:
            self.state.l_player_cards_drain.append(c)
            self.state.l_drain_creatures_on_player_hand.remove(c)
        if c.lethal:
            self.state.l_player_cards_lethal.append(c)
            self.state.l_lethal_creatures_on_player_hand.remove(c)
        if c.ward:
            self.state.l_player_cards_ward.append(c)
            self.state.l_ward_creatures_on_player_hand.remove(c)
        if c.guard:
            self.state.l_player_cards_guard.append(c)
            self.state.l_guard_creatures_on_player_hand.remove(c)
            self.state.cover = True
        self.state.l_cards_on_player_board.append(c)
        self.state.player2.hp += c.opponent_health_change
        self.state.player1.hp += c.my_health_change
        self.state.player1.draw += c.card_draw
        self.state.player1.mana -= c.cost
        self.state.l_cards_on_player_hand.remove(c)

# ------------------------------------------------------------
# Cover with guard
# ------------------------------------------------------------
class Cover:
    def __init__(self, state):

        self.state :State = state
        self.l_turn = []
        self.get_turn()

    def get_turn(self):
        if self.state.cover is not True and len(self.state.l_cards_on_player_board) < 6:
            self.cover()
        return self.l_turn

    def cover(self):
        while len(self.state.l_guard_creatures_on_player_hand) > 0:
            c = self.state.l_guard_creatures_on_player_hand[0]
            if c.cost > self.state.player1.mana or c not in self.state.l_cards_on_player_hand:
                self.state.l_guard_creatures_on_player_hand.remove(c)
                continue
            else:
                self.l_turn.append("SUMMON " + str(c.instance_id) + ";")
                if c.charge:
                    self.state.l_cards_can_attack.append(c)
                    self.state.l_player_cards_charger.append(c)
                    self.state.l_charger_creatures_on_player_hand.remove(c)
                if c.breakthrough:
                    self.state.l_player_cards_breakthrough.append(c)
                    self.state.l_breakthrough_creatures_on_player_hand.remove(c)
                if c.drain:
                    self.state.l_player_cards_drain.append(c)
                    self.state.l_drain_creatures_on_player_hand.remove(c)
                if c.lethal:
                    self.state.l_player_cards_lethal.append(c)
                    self.state.l_lethal_creatures_on_player_hand.remove(c)
                if c.ward:
                    self.state.l_player_cards_ward.append(c)
                    self.state.l_ward_creatures_on_player_hand.remove(c)
                if c.guard:
                    self.state.l_player_cards_guard.append(c)
            self.state.l_cards_on_player_board.append(c)
            self.state.player2.hp += c.opponent_health_change
            self.state.player1.hp += c.my_health_change
            self.state.player1.draw += c.card_draw
            self.state.player1.mana -= c.cost
            self.state.l_guard_creatures_on_player_hand.remove(c)
            self.state.l_cards_on_player_hand.remove(c)
            self.state.cover = True
            return

# ------------------------------------------------------------
# Charge strategy
# ------------------------------------------------------------
class Charge:
    def __init__(self, state):
        self.state :State = state
        self.l_turn = []
        self.get_turn()

    def get_turn(self):
        if len(self.state.l_charger_creatures_on_player_hand) > 0:
            self.charge()
        return self.l_turn

    def charge(self):
        for c in self.state.l_charger_creatures_on_player_hand:
            if c.cost > self.state.player1.mana or c not in self.state.l_cards_on_player_hand:
                continue
            self.l_turn.append("SUMMON " + str(c.instance_id) + ";")
            if c.breakthrough:
                self.state.l_player_cards_breakthrough.append(c)
                self.state.l_breakthrough_creatures_on_player_hand.remove(c)
            if c.drain:
                self.state.l_player_cards_drain.append(c)
                self.state.l_drain_creatures_on_player_hand.remove(c)
            if c.lethal:
                self.state.l_player_cards_lethal.append(c)
                self.state.l_lethal_creatures_on_player_hand.remove(c)
            if c.ward:
                self.state.l_player_cards_ward.append(c)
                self.state.l_ward_creatures_on_player_hand.remove(c)
            if c.guard:
                self.state.l_player_cards_guard.append(c)
                self.state.l_guard_creatures_on_player_hand.remove(c)
                self.state.cover = True
            self.state.l_player_cards_charger.append(c)
            self.state.l_cards_on_player_board.append(c)
            self.state.player2.hp += c.opponent_health_change
            self.state.player1.hp += c.my_health_change
            self.state.player1.draw += c.card_draw
            self.state.player1.mana -= c.cost
            self.state.l_charger_creatures_on_player_hand.remove(c)
            self.state.l_cards_on_player_hand.remove(c)
            self.state.l_cards_can_attack.append(c)

# ------------------------------------------------------------
# Drain strategy
# ------------------------------------------------------------
class Drain:
    def __init__(self, state):
        self.state :State = state
        self.l_turn = []
        self.get_turn()

    def get_turn(self):
        if len(self.state.l_drain_creatures_on_player_hand) > 0:
            self.drain()
        return self.l_turn

    def drain(self):
        for c in self.state.l_drain_creatures_on_player_hand:
            if c.cost > self.state.player1.mana or c not in self.state.l_cards_on_player_hand:
                continue
            self.l_turn.append("SUMMON " + str(c.instance_id) + ";")
            if c.charge:
                self.state.l_cards_can_attack.append(c)
                self.state.l_player_cards_charger.append(c)
                self.state.l_charger_creatures_on_player_hand.remove(c)
            if c.breakthrough:
                self.state.l_player_cards_breakthrough.append(c)
                self.state.l_breakthrough_creatures_on_player_hand.remove(c)
            if c.lethal:
                self.state.l_player_cards_lethal.append(c)
                self.state.l_lethal_creatures_on_player_hand.remove(c)
            if c.ward:
                self.state.l_player_cards_ward.append(c)
                self.state.l_ward_creatures_on_player_hand.remove(c)
            if c.guard:
                self.state.l_player_cards_guard.append(c)
                self.state.l_guard_creatures_on_player_hand.remove(c)
                self.state.cover = True
            self.state.l_player_cards_drain.append(c)
            self.state.l_cards_on_player_board.append(c)
            self.state.player2.hp += c.opponent_health_change
            self.state.player1.hp += c.my_health_change
            self.state.player1.draw += c.card_draw
            self.state.player1.mana -= c.cost
            self.state.l_drain_creatures_on_player_hand.remove(c)
            self.state.l_cards_on_player_hand.remove(c)

# ------------------------------------------------------------
# Breakthrough strategy
# ------------------------------------------------------------
class Breakthrough:
    def __init__(self, state):
        self.state :State = state
        self.l_turn = []
        self.get_turn()

    def get_turn(self):
        if len(self.state.l_breakthrough_creatures_on_player_hand) > 0:
            self.breakthrough()
        return self.l_turn

    def breakthrough(self):
        for c in self.state.l_breakthrough_creatures_on_player_hand:
            if c.cost > self.state.player1.mana or c not in self.state.l_cards_on_player_hand:
                continue
            self.l_turn.append("SUMMON " + str(c.instance_id) + ";")
            if c.charge:
                self.state.l_cards_can_attack.append(c)
                self.state.l_player_cards_charger.append(c)
                self.state.l_charger_creatures_on_player_hand.remove(c)
            if c.drain:
                self.state.l_player_cards_drain.append(c)
                self.state.l_drain_creatures_on_player_hand.remove(c)
            if c.lethal:
                self.state.l_player_cards_lethal.append(c)
                self.state.l_lethal_creatures_on_player_hand.remove(c)
            if c.guard:
                self.state.l_player_cards_guard.append(c)
                self.state.l_guard_creatures_on_player_hand.remove(c)
                self.state.cover = True
            if c.ward:
                self.state.l_player_cards_ward.append(c)
                self.state.l_ward_creatures_on_player_hand.remove(c)
            self.state.l_player_cards_breakthrough.append(c)
            self.state.l_cards_on_player_board.append(c)
            self.state.player2.hp += c.opponent_health_change
            self.state.player1.hp += c.my_health_change
            self.state.player1.draw += c.card_draw
            self.state.player1.mana -= c.cost
            self.state.l_breakthrough_creatures_on_player_hand.remove(c)
            self.state.l_cards_on_player_hand.remove(c)
            self.state.l_cards_can_attack.append(c)

# ------------------------------------------------------------
# Lethal strategy
# ------------------------------------------------------------
class Lethal:
    def __init__(self, state):
        self.state :State = state
        self.l_turn = []
        self.get_turn()

    def get_turn(self):
        if len(self.state.l_lethal_creatures_on_player_hand) > 0:
            self.lethal()
        return self.l_turn

    def lethal(self):
        for c in self.state.l_lethal_creatures_on_player_hand:
            if c.cost > self.state.player1.mana or c not in self.state.l_cards_on_player_hand:
                continue
            self.l_turn.append("SUMMON " + str(c.instance_id) + ";")
            if c.charge:
                self.state.l_cards_can_attack.append(c)
                self.state.l_player_cards_charger.append(c)
                self.state.l_charger_creatures_on_player_hand.remove(c)
            if c.breakthrough:
                self.state.l_player_cards_breakthrough.append(c)
                self.state.l_breakthrough_creatures_on_player_hand.remove(c)
            if c.drain:
                self.state.l_player_cards_drain.append(c)
                self.state.l_drain_creatures_on_player_hand.remove(c)
            if c.guard:
                self.state.l_player_cards_guard.append(c)
                self.state.l_guard_creatures_on_player_hand.remove(c)
                self.state.cover = True
            if c.ward:
                self.state.l_player_cards_ward.append(c)
                self.state.l_ward_creatures_on_player_hand.remove(c)
            self.state.l_player_cards_lethal.append(c)
            self.state.l_cards_on_player_board.append(c)
            self.state.player2.hp += c.opponent_health_change
            self.state.player1.hp += c.my_health_change
            self.state.player1.draw += c.card_draw
            self.state.player1.mana -= c.cost
            self.state.l_lethal_creatures_on_player_hand.remove(c)
            self.state.l_cards_on_player_hand.remove(c)
            self.state.l_cards_can_attack.append(c)

# ------------------------------------------------------------
# Ward strategy
# ------------------------------------------------------------
class Ward:
    def __init__(self, state):
        self.state :State = state
        self.l_turn = []
        self.get_turn()

    def get_turn(self):
        if len(self.state.l_ward_creatures_on_player_hand) > 0:
            self.ward()
        return self.l_turn

    def ward(self):
        for c in self.state.l_ward_creatures_on_player_hand:
            if c.cost > self.state.player1.mana or c not in self.state.l_cards_on_player_hand:
                continue
            self.l_turn.append("SUMMON " + str(c.instance_id) + ";")
            if c.charge:
                self.state.l_cards_can_attack.append(c)
                self.state.l_player_cards_charger.append(c)
                self.state.l_charger_creatures_on_player_hand.remove(c)
            if c.breakthrough:
                self.state.l_player_cards_breakthrough.append(c)
                self.state.l_breakthrough_creatures_on_player_hand.remove(c)
            if c.drain:
                self.state.l_player_cards_drain.append(c)
                self.state.l_drain_creatures_on_player_hand.remove(c)
            if c.lethal:
                self.state.l_player_cards_lethal.append(c)
                self.state.l_lethal_creatures_on_player_hand.remove(c)
            if c.guard:
                self.state.l_player_cards_guard.append(c)
                self.state.l_guard_creatures_on_player_hand.remove(c)
                self.state.cover = True
            self.state.l_player_cards_ward.append(c)
            self.state.l_cards_on_player_board.append(c)
            self.state.player2.hp += c.opponent_health_change
            self.state.player1.hp += c.my_health_change
            self.state.player1.draw += c.card_draw
            self.state.player1.mana -= c.cost
            self.state.l_ward_creatures_on_player_hand.remove(c)
            self.state.l_cards_on_player_hand.remove(c)

# ------------------------------------------------------------
# Use green objects
# ------------------------------------------------------------
class UseGreen:
    def __init__(self, state):

        self.state : State = state
        self.l_turn = []
        self.l_cards_on_player_board = []
        self.get_turn()

    def get_turn(self):
        l_cards_can_summon_after = []
        if len(self.state.l_cards_on_player_board) > 0:
            self.l_cards_on_player_board += self.state.l_cards_on_player_board

        while len(self.state.l_green_objects_on_player_hand) > 0:
            c = self.state.l_green_objects_on_player_hand[0]
            if c.cost > self.state.player1.mana:
                self.state.l_green_objects_on_player_hand.remove(c)
                continue
            if len(self.l_cards_on_player_board) == 0:
                l_cards_can_summon_after.append(c)
                self.state.l_green_objects_on_player_hand.remove(c)
                continue
            else:
                self.use(c)
        self.state.l_green_objects_on_player_hand = l_cards_can_summon_after

    def use(self, c):
        self.l_cards_on_player_board.sort(key=lambda x: x.cost, reverse=True)
        self.l_turn.append("USE " + str(c.instance_id) + " " + str(self.l_cards_on_player_board[0].instance_id) + ";")
        self.l_cards_on_player_board[0].defense += c.defense
        self.l_cards_on_player_board[0].attack += c.attack
        if c.breakthrough:
            self.l_cards_on_player_board[0].breakthrough = True
            if self.l_cards_on_player_board[0] not in self.state.l_player_cards_breakthrough:
                self.state.l_player_cards_breakthrough.append(self.l_cards_on_player_board[0])
        if c.charge:
            self.l_cards_on_player_board[0].charge = True
            if self.l_cards_on_player_board[0] not in self.state.l_cards_can_attack:
                self.state.l_cards_can_attack.append(self.l_cards_on_player_board[0])
        if c.drain:
            self.l_cards_on_player_board[0].drain = True
            if self.l_cards_on_player_board[0] not in self.state.l_player_cards_drain:
                self.state.l_player_cards_drain.append(self.l_cards_on_player_board[0])
        if c.guard:
            self.l_cards_on_player_board[0].guard = True
            if self.l_cards_on_player_board[0] not in self.state.l_player_cards_guard:
                self.state.l_player_cards_guard.append(self.l_cards_on_player_board[0])
                self.state.cover = True
        if c.lethal:
            self.l_cards_on_player_board[0].lethal = True
            if self.l_cards_on_player_board[0] not in self.state.l_player_cards_lethal:
                self.state.l_player_cards_lethal.append(self.l_cards_on_player_board[0])
        if c.ward:
            self.l_cards_on_player_board[0].ward = True
            if self.l_cards_on_player_board[0] not in self.state.l_player_cards_ward:
                self.state.l_player_cards_ward.append(self.l_cards_on_player_board[0])
        self.state.player2.hp += c.opponent_health_change
        self.state.player1.hp += c.my_health_change
        self.state.player1.draw += c.card_draw
        self.state.player1.mana -= c.cost
        self.state.l_green_objects_on_player_hand.remove(c)

# ------------------------------------------------------------
# Use red objects
# ------------------------------------------------------------
class UseRed:
    def __init__(self, state):

        self.state :State = state
        self.l_turn = []
        self.l_cards_on_opponent_board = []
        self.get_turn()

    def get_turn(self):
        if len(self.state.l_cards_on_opponent_board) > 0:
            self.l_cards_on_opponent_board += self.state.l_cards_on_opponent_board
            
        l_cards_can_summon_after = []
        while len(self.state.l_red_objects_on_player_hand) > 0:
            c = self.state.l_red_objects_on_player_hand[0]
            if c.cost > self.state.player1.mana:
                self.state.l_red_objects_on_player_hand.remove(c)
                continue
            if len(self.l_cards_on_opponent_board) == 0:
                l_cards_can_summon_after.append(c)
                self.state.l_red_objects_on_player_hand.remove(c)
                continue
            else:
                self.use(c)
        self.state.l_red_objects_on_player_hand = l_cards_can_summon_after

    def use(self, c):
        best_coincidences = 0
        best_coincidence_card = self.l_cards_on_opponent_board[0]
        for enemyCard in self.l_cards_on_opponent_board:
            coincidences = 0
            if enemyCard.breakthrough and c.breakthrough:
                coincidences += 1
            if enemyCard.charge and c.charge:
                coincidences += 1
            if enemyCard.drain and c.drain:
                coincidences += 1
            if enemyCard.guard and c.guard:
                coincidences += 1
            if enemyCard.lethal and c.lethal:
                coincidences += 1
            if enemyCard.ward and c.ward:
                coincidences += 1
            if coincidences > best_coincidences:
                best_coincidences = coincidences
                best_coincidence_card = enemyCard

        if best_coincidences > 0:
            self.l_turn.append("USE " + str(c.instance_id) + " " + str(best_coincidence_card.instance_id) + ";")
            best_coincidence_card.defense += c.defense
            best_coincidence_card.attack += c.attack
            if best_coincidence_card.breakthrough and c.breakthrough:
                best_coincidence_card.breakthrough = False
            if best_coincidence_card.charge and c.charge:
                best_coincidence_card.charge = False
            if best_coincidence_card.drain and c.drain:
                best_coincidence_card.drain = False
            if best_coincidence_card.guard and c.guard:
                best_coincidence_card.guard = False
            if best_coincidence_card.lethal and c.lethal:
                best_coincidence_card.lethal = False
            if best_coincidence_card.ward and c.ward:
                best_coincidence_card.ward = False
            self.state.player2.hp += c.opponent_health_change
            self.state.player1.hp += c.my_health_change
            self.state.player1.draw += c.card_draw
            if best_coincidence_card.defense <= 0:
                self.state.l_cards_on_opponent_board.remove(best_coincidence_card)
                if best_coincidence_card in self.state.l_opponent_cards_guard:
                    self.state.l_opponent_cards_guard.remove(best_coincidence_card)
                if best_coincidence_card in self.state.l_opponent_cards_drain:
                    self.state.l_opponent_cards_drain.remove(best_coincidence_card)
                if best_coincidence_card in self.state.l_opponent_cards_lethal:
                    self.state.l_opponent_cards_lethal.remove(best_coincidence_card)
                if best_coincidence_card in self.state.l_opponet_cards_breakthrough:
                    self.state.l_opponet_cards_breakthrough.remove(best_coincidence_card)
                if best_coincidence_card in self.state.l_opponent_cards_charger:
                    self.state.l_opponent_cards_charger.remove(best_coincidence_card)
                if best_coincidence_card in self.state.l_opponent_cards_ward:
                    self.state.l_opponent_cards_ward.remove(best_coincidence_card)
                self.l_cards_on_opponent_board.remove(best_coincidence_card)
        else:
            best_difference = 100
            c_attack = self.l_cards_on_opponent_board[0]
            for enemyCard in self.l_cards_on_opponent_board:
                diference = abs(enemyCard.defense + c.defense)
                if diference == 0:
                    c_attack = enemyCard
                    break
                elif diference < best_difference:
                    best_difference = diference
                    c_attack = enemyCard
            self.l_turn.append("USE " + str(c.instance_id) + " " + str(c_attack.instance_id) + ";")
            c_attack.defense += c.defense
            c_attack.attack += c.attack
            self.state.player2.hp += c.opponent_health_change
            self.state.player1.hp += c.my_health_change
            self.state.player1.draw += c.card_draw
            if c_attack.defense <= 0:
                self.state.l_cards_on_opponent_board.remove(c_attack)
                if c_attack in self.state.l_opponent_cards_guard:
                    self.state.l_opponent_cards_guard.remove(c_attack)
                if c_attack in self.state.l_opponent_cards_drain:
                    self.state.l_opponent_cards_drain.remove(c_attack)
                if c_attack in self.state.l_opponent_cards_lethal:
                    self.state.l_opponent_cards_lethal.remove(c_attack)
                if c_attack in self.state.l_opponet_cards_breakthrough:
                    self.state.l_opponet_cards_breakthrough.remove(c_attack)
                if c_attack in self.state.l_opponent_cards_charger:
                    self.state.l_opponent_cards_charger.remove(c_attack)
                if c_attack in self.state.l_opponent_cards_ward:
                    self.state.l_opponent_cards_ward.remove(c_attack)
                self.l_cards_on_opponent_board.remove(c_attack)
        self.state.player1.mana -= c.cost
        self.state.l_red_objects_on_player_hand.remove(c)

# ------------------------------------------------------------
# Use blue objects
# ------------------------------------------------------------
class UseBlue:
    def __init__(self, state):

        self.state :State = state
        self.l_turn = []
        self.l_cards_on_opponent_board = []
        self.get_turn()

    def get_turn(self):
        if len(self.state.l_cards_on_opponent_board) > 0:
            self.l_cards_on_opponent_board += self.state.l_cards_on_opponent_board
            
        l_cards_can_summon_after = []
        while len(self.state.l_blue_objects_on_player_hand) > 0:
            c = self.state.l_blue_objects_on_player_hand[0]
            if c.cost > self.state.player1.mana:
                self.state.l_blue_objects_on_player_hand.remove(c)
                continue
            else:
                self.use(c)
        self.state.l_blue_objects_on_player_hand = l_cards_can_summon_after

    def use(self, c):
        if c.defense < 0 and len(self.l_cards_on_opponent_board) > 0:
            best_difference = 30
            c_attack = self.l_cards_on_opponent_board[0]
            for enemyCard in self.l_cards_on_opponent_board:
                diference = abs(enemyCard.defense + c.defense)
                if diference == 0:
                    c_attack = enemyCard
                    break
                elif diference < best_difference:
                    best_difference = diference
                    c_attack = enemyCard
            self.l_turn.append("USE " + str(c.instance_id) + " " + str(c_attack.instance_id) + ";")
            c_attack.defense += c.defense
            c_attack.attack += c.attack
            self.state.player2.hp += c.opponent_health_change
            self.state.player1.hp += c.my_health_change
            self.state.player1.draw += c.card_draw
            if c_attack.defense <= 0:

                self.state.l_cards_on_opponent_board.remove(c_attack)
                if c_attack in self.state.l_opponent_cards_guard:
                    self.state.l_opponent_cards_guard.remove(c_attack)
                if c_attack in self.state.l_opponent_cards_drain:
                    self.state.l_opponent_cards_drain.remove(c_attack)
                if c_attack in self.state.l_opponent_cards_lethal:
                    self.state.l_opponent_cards_lethal.remove(c_attack)
                if c_attack in self.state.l_opponet_cards_breakthrough:
                    self.state.l_opponet_cards_breakthrough.remove(c_attack)
                if c_attack in self.state.l_opponent_cards_charger:
                    self.state.l_opponent_cards_charger.remove(c_attack)
                if c_attack in self.state.l_opponent_cards_ward:
                    self.state.l_opponent_cards_ward.remove(c_attack)
                self.l_cards_on_opponent_board.remove(c_attack)
        else:
            self.l_turn.append("USE " + str(c.instance_id) + " -1;")
            self.state.player2.hp += c.defense
            self.state.player2.hp += c.opponent_health_change
            self.state.player1.hp += c.my_health_change
            self.state.player1.draw += c.card_draw
        self.state.player1.mana -= c.cost
        self.state.l_blue_objects_on_player_hand.remove(c)


# ------------------------------------------------------------
# Attack strategies class
# ------------------------------------------------------------
# ------------------------------------------------------------
# Destroy all cards before attack head
# ------------------------------------------------------------
class AttackCards:
    def __init__(self, state):

        self.state :State = state
        self.l_turn = []
        self.get_turn()
    def get_turn(self):
        while len(self.state.l_cards_can_attack) > 0:
            self.attack(0)

    def attack(self, n):
        c = self.state.l_cards_can_attack[n]
        if len(self.state.l_opponent_cards_guard) > 0:
            self.attack_guard(c, 0)
        elif len(self.state.l_cards_on_opponent_board) > 0:
            self.attack_cards(c, 0)
        else:
            self.l_turn.append("ATTACK " + str(c.instance_id) + " -1;")
            self.state.player2.hp -= c.attack
            if c.drain:
                self.state.player1.hp += c.attack
        self.state.l_cards_can_attack.remove(c)

    def attack_guard(self, c, n):
        self.l_turn.append(
            "ATTACK " + str(c.instance_id) + " " + str(self.state.l_opponent_cards_guard[n].instance_id) + ";")
        if self.state.l_opponent_cards_guard[n].ward:
            self.state.l_opponent_cards_guard[n].ward = False
        elif c.lethal:
            self.state.l_opponent_cards_guard[n].defense = 0
            if c.drain:
                self.state.player1.hp += c.attack
        else:
            self.state.l_opponent_cards_guard[n].defense -= c.attack
            if c.drain:
                self.state.player1.hp += c.attack
        c.defense -= self.state.l_opponent_cards_guard[n].attack
        if self.state.l_opponent_cards_guard[n].defense <= 0:
            if c.breakthrough:
                self.state.player2.hp += self.state.l_opponent_cards_guard[n].defense
            if self.state.l_opponent_cards_guard[n] in self.state.l_opponent_cards_drain:
                self.state.l_opponent_cards_drain.remove(self.state.l_opponent_cards_guard[n])
            if self.state.l_opponent_cards_guard[n] in self.state.l_opponent_cards_lethal:
                self.state.l_opponent_cards_lethal.remove(self.state.l_opponent_cards_guard[n])
            self.state.l_cards_on_opponent_board.remove(self.state.l_opponent_cards_guard[n])
            self.state.l_opponent_cards_guard.remove(self.state.l_opponent_cards_guard[n])
        if c.defense <= 0:
            self.state.l_cards_on_player_board.remove(c)
    
    def attack_cards(self, c, n):
        self.l_turn.append(
            "ATTACK " + str(c.instance_id) + " " + str(self.state.l_cards_on_opponent_board[n].instance_id) + ";")
        if self.state.l_cards_on_opponent_board[n].ward:
            self.state.l_cards_on_opponent_board[n].ward = False
        elif c.lethal:
            self.state.l_cards_on_opponent_board[n].defense = 0
            if c.drain:
                self.state.player1.hp += c.attack
        else:
            self.state.l_cards_on_opponent_board[n].defense -= c.attack
            if c.drain:
                self.state.player1.hp += c.attack
        c.defense -= self.state.l_cards_on_opponent_board[n].attack
        if self.state.l_cards_on_opponent_board[n].defense <= 0:
            if c.breakthrough:
                self.state.player2.hp += self.state.l_cards_on_opponent_board[n].defense
            if self.state.l_cards_on_opponent_board[n] in self.state.l_opponent_cards_drain:
                self.state.l_opponent_cards_drain.remove(self.state.l_cards_on_opponent_board[n])
            if self.state.l_cards_on_opponent_board[n] in self.state.l_opponent_cards_lethal:
                self.state.l_opponent_cards_lethal.remove(self.state.l_cards_on_opponent_board[n])

            self.state.l_cards_on_opponent_board.remove(self.state.l_cards_on_opponent_board[n])
        if c.defense <= 0:
            if c in self.state.l_cards_on_player_board:
                self.state.l_cards_on_player_board.remove(c)
            # self.state.l_cards_on_player_board.remove(c)

# ------------------------------------------------------------
# Attack head if you can
# ------------------------------------------------------------
class AttackHead:
    def __init__(self, state):

        self.state :State= state
        self.l_turn = []
        self.get_turn()
    
    def get_turn(self):
        while len(self.state.l_cards_can_attack) > 0:
            self.attack(0)
    
    def attack(self, n):
        c = self.state.l_cards_can_attack[n]
        if len(self.state.l_opponent_cards_guard) > 0:
            self.l_turn.append(
                "ATTACK " + str(c.instance_id) + " " + str(self.state.l_opponent_cards_guard[0].instance_id) + ";")
            if self.state.l_opponent_cards_guard[0].ward:
                self.state.l_opponent_cards_guard[0].ward = False
            elif c.lethal:
                self.state.l_opponent_cards_guard[0].defense = 0
                if c.drain:
                    self.state.player1.hp += c.attack
            else:
                self.state.l_opponent_cards_guard[0].defense -= c.attack
                if c.drain:
                    self.state.player1.hp += c.attack
            c.defense -= self.state.l_opponent_cards_guard[0].attack
            if self.state.l_opponent_cards_guard[0].defense <= 0:
                if c.breakthrough:
                    self.state.player2.hp += self.state.l_opponent_cards_guard[0].defense
                if self.state.l_opponent_cards_guard[0] in self.state.l_opponent_cards_drain:
                    self.state.l_opponent_cards_drain.remove(self.state.l_opponent_cards_guard[0])
                if self.state.l_opponent_cards_guard[0] in self.state.l_opponent_cards_lethal:
                    self.state.l_opponent_cards_lethal.remove(self.state.l_opponent_cards_guard[0])
                if self.state.l_opponent_cards_guard[0] in self.state.l_opponet_cards_breakthrough:
                    self.state.l_opponet_cards_breakthrough.remove(self.state.l_opponent_cards_guard[0])
                if self.state.l_opponent_cards_guard[0] in self.state.l_opponent_cards_charger:
                    self.state.l_opponent_cards_charger.remove(self.state.l_opponent_cards_guard[0])
                if self.state.l_opponent_cards_guard[0] in self.state.l_opponent_cards_ward:
                    self.state.l_opponent_cards_ward.remove(self.state.l_opponent_cards_guard[0])
                
                self.state.l_cards_on_opponent_board.remove(self.state.l_opponent_cards_guard[0])
                self.state.l_opponent_cards_guard.remove(self.state.l_opponent_cards_guard[0])
            if c.defense <= 0:
                self.state.l_cards_on_player_board.remove(c)
        else:
            self.l_turn.append("ATTACK " + str(c.instance_id) + " -1;")
            self.state.player2.hp -= c.attack
            if c.drain:
                self.state.player1.hp += c.attack
        self.state.l_cards_can_attack.remove(c)

# ------------------------------------------------------------
# Attack only drain cards
# ------------------------------------------------------------
class AttackDrains:
    def __init__(self, state):

        self.state :State = state
        self.l_turn = []
        self.get_turn()

    def get_turn(self):
        while len(self.state.l_cards_can_attack) > 0 and len(self.state.l_opponent_cards_drain) > 0:
            self.attack(0)
    
    def attack(self, n):
        c = self.state.l_cards_can_attack[n]
        self.attack_drain(c, 0)
        self.state.l_cards_can_attack.remove(c)

    def attack_drain(self, c, n):
        self.l_turn.append(
            "ATTACK " + str(c.instance_id) + " " + str(self.state.l_opponent_cards_drain[n].instance_id) + ";")
        if self.state.l_opponent_cards_drain[n].ward:
            self.state.l_opponent_cards_drain[n].ward = False
        elif c.lethal:
            self.state.l_opponent_cards_drain[n].defense = 0
            if c.drain:
                self.state.player1.hp += c.attack
        else:
            self.state.l_opponent_cards_drain[n].defense -= c.attack
            if c.drain:
                self.state.player1.hp += c.attack
        c.defense -= self.state.l_opponent_cards_drain[n].attack
        if self.state.l_opponent_cards_drain[n].defense <= 0:
            if c.breakthrough:
                self.state.player2.hp += self.state.l_opponent_cards_drain[n].defense
            self.state.l_cards_on_opponent_board.remove(self.state.l_opponent_cards_drain[n])
            if self.state.l_opponent_cards_drain[n] in self.state.l_opponent_cards_guard:
                self.state.l_opponent_cards_guard.remove(self.state.l_opponent_cards_drain[n])
            if self.state.l_opponent_cards_drain[n] in self.state.l_opponent_cards_lethal:
                self.state.l_opponent_cards_lethal.remove(self.state.l_opponent_cards_drain[n])
            if self.state.l_opponent_cards_drain[n] in self.state.l_opponet_cards_breakthrough:
                self.state.l_opponet_cards_breakthrough.remove(self.state.l_opponent_cards_drain[n])
            if self.state.l_opponent_cards_drain[n] in self.state.l_opponent_cards_charger:
                self.state.l_opponent_cards_charger.remove(self.state.l_opponent_cards_drain[n])
            if self.state.l_opponent_cards_drain[n] in self.state.l_opponent_cards_ward:
                self.state.l_opponent_cards_ward.remove(self.state.l_opponent_cards_drain[n])
            self.state.l_opponent_cards_drain.remove(self.state.l_opponent_cards_drain[n])

        if c.defense <= 0:
            self.state.l_cards_on_player_board.remove(c)

# ------------------------------------------------------------
# Attack only guard cards
# ------------------------------------------------------------
class AttackGuards:
    def __init__(self, state):

        self.state :State = state
        self.l_turn = []
        self.get_turn()

    def get_turn(self):
        while len(self.state.l_cards_can_attack) > 0 and len(self.state.l_opponent_cards_guard) > 0:
            self.attack(0)
    
    def attack(self, n):
        c = self.state.l_cards_can_attack[n]
        self.attack_guard(c, 0)
        self.state.l_cards_can_attack.remove(c)

    def attack_guard(self, c, n):
        self.l_turn.append("ATTACK " + str(c.instance_id) + " " + str(self.state.l_opponent_cards_guard[n].instance_id) + ";")
        if self.state.l_opponent_cards_guard[n].ward:
            self.state.l_opponent_cards_guard[n].ward = False
        elif c.lethal:
            self.state.l_opponent_cards_guard[n].defense = 0
            if c.drain:
                self.state.player1.hp += c.attack
        else:
            self.state.l_opponent_cards_guard[n].defense -= c.attack
            if c.drain:
                self.state.player1.hp += c.attack
        c.defense -= self.state.l_opponent_cards_guard[n].attack
        if self.state.l_opponent_cards_guard[n].defense <= 0:
            if c.breakthrough:
                self.state.player2.hp += self.state.l_opponent_cards_guard[n].defense
            self.state.l_cards_on_opponent_board.remove(self.state.l_opponent_cards_guard[n])
            if self.state.l_opponent_cards_guard[n] in self.state.l_opponent_cards_drain:
                self.state.l_opponent_cards_drain.remove(self.state.l_opponent_cards_guard[n])
            if self.state.l_opponent_cards_guard[n] in self.state.l_opponent_cards_lethal:
                self.state.l_opponent_cards_lethal.remove(self.state.l_opponent_cards_guard[n])
            if self.state.l_opponent_cards_guard[n] in self.state.l_opponet_cards_breakthrough:
                self.state.l_opponet_cards_breakthrough.remove(self.state.l_opponent_cards_guard[n])
            if self.state.l_opponent_cards_guard[n] in self.state.l_opponent_cards_charger:
                self.state.l_opponent_cards_charger.remove(self.state.l_opponent_cards_guard[n])
            if self.state.l_opponent_cards_guard[n] in self.state.l_opponent_cards_ward:
                self.state.l_opponent_cards_ward.remove(self.state.l_opponent_cards_guard[n])
                
            self.state.l_opponent_cards_guard.remove(self.state.l_opponent_cards_guard[n])
        if c.defense <= 0:
            self.state.l_cards_on_player_board.remove(c)

# ------------------------------------------------------------
# Attack only lethal cards
# ------------------------------------------------------------
class AttackLethals:
    def __init__(self, state):

        self.state :State = state
        self.l_turn = []
        self.get_turn()
    
    def get_turn(self):
        while len(self.state.l_cards_can_attack) > 0 and len(self.state.l_opponent_cards_lethal) > 0:
            self.attack(0)
    
    def attack(self, n):
        c = self.state.l_cards_can_attack[n]
        self.attack_lethal(c, 0)
        self.state.l_cards_can_attack.remove(c)

    def attack_lethal(self, c, n):
        self.l_turn.append(
            "ATTACK " + str(c.instance_id) + " " + str(self.state.l_opponent_cards_lethal[n].instance_id) + ";")
        if self.state.l_opponent_cards_lethal[n].ward:
            self.state.l_opponent_cards_lethal[n].ward = False
        elif c.lethal:
            self.state.l_opponent_cards_lethal[n].defense = 0
            if c.drain:
                self.state.player1.hp += c.attack
        else:
            self.state.l_opponent_cards_lethal[n].defense -= c.attack
            if c.drain:
                self.state.player1.hp += c.attack
        c.defense -= self.state.l_opponent_cards_lethal[n].attack
        if self.state.l_opponent_cards_lethal[n].defense <= 0:
            if c.breakthrough:
                self.state.player2.hp += self.state.l_opponent_cards_lethal[n].defense
            self.state.l_cards_on_opponent_board.remove(self.state.l_opponent_cards_lethal[n])
            if self.state.l_opponent_cards_lethal[n] in self.state.l_opponent_cards_guard:
                self.state.l_opponent_cards_guard.remove(self.state.l_opponent_cards_lethal[n])
            if self.state.l_opponent_cards_lethal[n] in self.state.l_opponent_cards_drain:
                self.state.l_opponent_cards_drain.remove(self.state.l_opponent_cards_lethal[n])
            if self.state.l_opponent_cards_lethal[n] in self.state.l_opponet_cards_breakthrough:
                self.state.l_opponet_cards_breakthrough.remove(self.state.l_opponent_cards_lethal[n])
            if self.state.l_opponent_cards_lethal[n] in self.state.l_opponent_cards_charger:
                self.state.l_opponent_cards_charger.remove(self.state.l_opponent_cards_lethal[n])
            if self.state.l_opponent_cards_lethal[n] in self.state.l_opponent_cards_ward:
                self.state.l_opponent_cards_ward.remove(self.state.l_opponent_cards_lethal[n])
            self.state.l_opponent_cards_lethal.remove(self.state.l_opponent_cards_lethal[n])
        if c.defense <= 0:
            self.state.l_cards_on_player_board.remove(c)

# ------------------------------------------------------------
# Attack only breakthrough cards
# ------------------------------------------------------------
class AttackBreakthroughs:
    def __init__(self, state):

        self.state :State = state
        self.l_turn = []
        self.get_turn()
    
    def get_turn(self):
        while len(self.state.l_cards_can_attack) > 0 and len(self.state.l_opponent_cards_guard) > 0:
            self.attack(0)
    
    def attack(self, n):
        c = self.state.l_cards_can_attack[n]
        self.attack_breakthrough(c, 0)
        self.state.l_cards_can_attack.remove(c)

    def attack_breakthrough(self, c, n):
        self.l_turn.append(
            "ATTACK " + str(c.instance_id) + " " + str(self.state.l_opponet_cards_breakthrough[n].instance_id) + ";")
        if self.state.l_opponet_cards_breakthrough[n].ward:
            self.state.l_opponet_cards_breakthrough[n].ward = False
        elif c.lethal:
            self.state.l_opponet_cards_breakthrough[n].defense = 0
            if c.drain:
                self.state.player1.hp += c.attack
        else:
            self.state.l_opponet_cards_breakthrough[n].defense -= c.attack
            if c.drain:
                self.state.player1.hp += c.attack
        c.defense -= self.state.l_opponet_cards_breakthrough[n].attack
        if self.state.l_opponet_cards_breakthrough[n].defense <= 0:
            if c.breakthrough:
                self.state.player2.hp += self.state.l_opponet_cards_breakthrough[n].defense
            self.state.l_cards_on_opponent_board.remove(self.state.l_opponet_cards_breakthrough[n])
            if self.state.l_opponet_cards_breakthrough[n] in self.state.l_opponent_cards_guard:
                self.state.l_opponent_cards_guard.remove(self.state.l_opponet_cards_breakthrough[n])
            if self.state.l_opponet_cards_breakthrough[n] in self.state.l_opponent_cards_drain:
                self.state.l_opponent_cards_drain.remove(self.state.l_opponet_cards_breakthrough[n])
            if self.state.l_opponet_cards_breakthrough[n] in self.state.l_opponent_cards_lethal:
                self.state.l_opponent_cards_lethal.remove(self.state.l_opponet_cards_breakthrough[n])
            if self.state.l_opponet_cards_breakthrough[n] in self.state.l_opponent_cards_charger:
                self.state.l_opponent_cards_charger.remove(self.state.l_opponet_cards_breakthrough[n])
            if self.state.l_opponet_cards_breakthrough[n] in self.state.l_opponent_cards_ward:
                self.state.l_opponent_cards_ward.remove(self.state.l_opponet_cards_breakthrough[n])
            self.state.l_opponet_cards_breakthrough.remove(self.state.l_opponet_cards_breakthrough[n])
        if c.defense <= 0:
            self.state.l_cards_on_player_board.remove(c)

# ------------------------------------------------------------
# Turn information
# ------------------------------------------------------------
class Turn:
    def __init__(self, state, summon_strategy, attack_strategy):
        self.state : State = state
        self.turn_state : State = copy.deepcopy(state)
        self.summon_strategy = summon_strategy
        self.attack_strategy = attack_strategy

        self.l_turn = []
        self.create_turn()
        self.reward = self.evaluate_state()
    
    def create_turn(self):
        self.use_mana(self.summon_strategy)
        self.attack(self.attack_strategy)
        if len(self.turn_state.l_cards_on_player_hand) + len(self.turn_state.l_green_objects_on_player_hand) + len(
                self.turn_state.l_blue_objects_on_player_hand) + len(self.turn_state.l_red_objects_on_player_hand) > 0:
            self.use_mana(self.summon_strategy)
            self.attack(self.attack_strategy)

    def summon_all(self):
        summon_turn = SummonAll(self.turn_state)
        self.l_turn += summon_turn.l_turn
    
    def summon_by_creature(self, creature="Guard"):
        if creature == "Guard":
            summon_turn = Cover(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif creature == "Charge":
            summon_turn = Charge(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif creature == "Drain":
            summon_turn = Drain(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif creature == "Breakthrough":
            summon_turn = Breakthrough(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif creature == "Lethal":
            summon_turn = Lethal(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif creature == "Ward":
            summon_turn = Ward(self.turn_state)
            self.l_turn += summon_turn.l_turn
    
    def summon_by_order(self, reverse=False):
        self.turn_state.l_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=reverse)
    
    def summon_by_creature_and_order(self, creature="Guard", reverse=False):
        self.summon_by_order(reverse)
        if creature == "Guard":
            self.turn_state.l_guard_creatures_on_player_hand.sort(key=lambda x: x.cost, reverse=reverse)
        elif creature == "Charge":
            self.turn_state.l_charger_creatures_on_player_hand.sort(key=lambda x: x.cost, reverse=reverse)
        elif creature == "Drain":
            self.turn_state.l_drain_creatures_on_player_hand.sort(key=lambda x: x.cost, reverse=reverse)
        elif creature == "Breakthrough":
            self.turn_state.l_breakthrough_creatures_on_player_hand.sort(key=lambda x: x.cost, reverse=reverse)
        elif creature == "Lethal":
            self.turn_state.l_lethal_creatures_on_player_hand.sort(key=lambda x: x.cost, reverse=reverse)
        elif creature == "Ward":
            self.turn_state.l_ward_creatures_on_player_hand.sort(key=lambda x: x.cost, reverse=reverse)
        self.summon_by_creature(creature)
        self.summon_all()
    
    def use_item(self, item="Green"):
        if item == "Green":
            summon_turn = UseGreen(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif item == "Red":
            summon_turn = UseRed(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif item == "Blue":
            summon_turn = UseBlue(self.turn_state)
            self.l_turn += summon_turn.l_turn

    # A High-level strategy to summon cards
    def use_item_and_creature(self, item="Green", creature="Guard"):
        self.use_item(item)
        self.summon_by_creature(creature)
    
    def use_creature_and_item(self, creature="Guard", item="Green"):
        self.summon_by_creature(creature)
        self.use_item(item)
    
    def use_creature_and_item_and_order(self, creature="Guard", item="Green", reverse=False):
        self.summon_by_creature_and_order(creature, reverse)
        self.use_item(item)
    
    def use_item_and_creature_and_order(self, item="Green", creature="Guard", reverse=False):
        self.use_item(item)
        self.summon_by_creature_and_order(creature, reverse)
    
    def use_item_and_creature_cross_by_list(self, item_list, creature_list):
        for item in item_list:
            for creature in creature_list:
                if self.turn_state.player1.mana <= 0:
                    return
                self.use_item_and_creature(item, creature)
    
    def use_item_and_creature_cross_by_list_and_order(self, item_list, creature_list, reverse=False):
        for item in item_list:
            for creature in creature_list:
                if self.turn_state.player1.mana <= 0:
                    return
                self.use_item_and_creature_and_order(item, creature, reverse)
    
    def use_creautre_and_item_cross_by_list(self, creature_list, item_list):
        for creature in creature_list:
            for item in item_list:
                if self.turn_state.player1.mana <= 0:
                    return
                self.use_creature_and_item(creature, item)
    
    def use_creautre_and_item_cross_by_list_and_order(self, creature_list, item_list, reverse=False):
        for creature in creature_list:
            for item in item_list:
                if self.turn_state.player1.mana <= 0:
                    return
                self.use_creature_and_item_and_order(creature, item, reverse)

    def use_mana(self, strategy):
        # Choose only high-level strategies
        if strategy == 1:
            # only summon creatures
            self.summon_all()
        elif strategy == 2:
            # use item and creature cross by list
            item_list = ["Green", "Red", "Blue"]
            random.shuffle(item_list)
            creature_list = ["Guard", "Charge", "Drain", "Breakthrough", "Lethal", "Ward"]
            random.shuffle(creature_list)
            self.use_item_and_creature_cross_by_list(item_list, creature_list)
        elif strategy == 3:
            # use item and creature cross by list and order
            item_list = ["Green", "Red", "Blue"]
            random.shuffle(item_list)
            creature_list = ["Guard", "Charge", "Drain", "Breakthrough", "Lethal", "Ward"]
            random.shuffle(creature_list)
            reverse = random.choice([True, False])
            self.use_item_and_creature_cross_by_list_and_order(item_list, creature_list, reverse=reverse)
        elif strategy == 4:
            # use creature and item cross by list
            item_list = ["Green", "Red", "Blue"]
            random.shuffle(item_list)
            creature_list = ["Guard", "Charge", "Drain", "Breakthrough", "Lethal", "Ward"]
            random.shuffle(creature_list)
            self.use_creautre_and_item_cross_by_list(creature_list, item_list)
        elif strategy == 5:
            # use creature and item cross by list and order
            item_list = ["Green", "Red", "Blue"]
            random.shuffle(item_list)
            creature_list = ["Guard", "Charge", "Drain", "Breakthrough", "Lethal", "Ward"]
            random.shuffle(creature_list)
            reverse = random.choice([True, False])
            self.use_creautre_and_item_cross_by_list_and_order(creature_list, item_list, reverse=reverse)
        elif strategy == 6:
            # only use items
            item_list = ["Green", "Red", "Blue"]
            random.shuffle(item_list)
            
            for item in item_list:
                self.use_item(item)
        elif strategy == 7:
            # only use creatures
            creature_list = ["Guard", "Charge", "Drain", "Breakthrough", "Lethal", "Ward"]
            random.shuffle(creature_list)
            for creature in creature_list:
                self.summon_by_creature(creature)

    def attack(self, strategy):
        def sort_our_cards_by_attack():
            self.turn_state.l_cards_can_attack.sort(key=lambda x: x.attack, reverse=True)
        
        def sort_opponent_cards_by_defense():
            self.turn_state.l_cards_on_opponent_board.sort(key=lambda x: x.defense, reverse=False)
            self.turn_state.l_opponent_cards_guard.sort(key=lambda x: x.defense, reverse=False)

        def attack_guards():
            attack_turn = AttackGuards(self.turn_state)
            self.l_turn += attack_turn.l_turn

        def attack_drains():
            attack_turn = AttackDrains(self.turn_state)
            self.l_turn += attack_turn.l_turn

        def attack_lethals():
            attack_turn = AttackLethals(self.turn_state)
            self.l_turn += attack_turn.l_turn

        def attack_breakthroughs():
            attack_turn = AttackBreakthroughs(self.turn_state)
            self.l_turn += attack_turn.l_turn

        if strategy == 1:
            attack_turn = AttackHead(self.turn_state)
            self.l_turn += attack_turn.l_turn
        elif strategy == 2:
            attack_turn = AttackCards(self.turn_state)
            self.l_turn += attack_turn.l_turn
        elif strategy == 3:
            sort_our_cards_by_attack()
            self.attack(2)
        elif strategy == 4:
            sort_opponent_cards_by_defense()
            self.attack(2)
        elif strategy == 5:
            sort_our_cards_by_attack()
            sort_opponent_cards_by_defense()
            self.attack(2)
        elif strategy == 6:
            attack_guards()
            attack_drains()
            self.attack(1)
        elif strategy == 7:
            attack_guards()
            attack_lethals()
            self.attack(1)
        elif strategy == 8:
            attack_guards()
            attack_breakthroughs()
            self.attack(1)
        elif strategy == 9:
            attack_guards()
            attack_drains()
            attack_lethals()
            self.attack(1)
        elif strategy == 10:
            attack_guards()
            attack_breakthroughs()
            attack_lethals()
            self.attack(1)
        elif strategy == 11:
            attack_guards()
            attack_breakthroughs()
            attack_drains()
            self.attack(1)
        elif strategy == 12:
            attack_guards()
            attack_breakthroughs()
            attack_drains()
            attack_lethals()
            self.attack(1)
        elif strategy == 13:
            sort_our_cards_by_attack()
            sort_opponent_cards_by_defense()
            self.attack(12)

    def evaluate_state(self):
        reward = 0
        if self.turn_state.player2.hp <= 0:
            return 1000
        reward += self.turn_state.player1.hp - self.state.player1.hp
        reward += self.turn_state.player1.draw - self.state.player1.draw
        reward += self.state.player2.hp - self.turn_state.player2.hp
        reward += self.turn_state.player_cardvalue() - self.state.player_cardvalue()
        reward += self.state.opponent_cardvalue() - self.turn_state.opponent_cardvalue()
        return reward

class BeamSearchAgent:
    def __init__(self):
        self.state = None
        self.last_state = None
        self.draft = Draft()
        self.summon_strategy = 0
        self.last_summon_strategy = 0
        self.attack_strategy = 0
        self.last_attack_strategy = 0
        self.LOCATION_IN_HAND = 0
        self.LOCATION_PLAYER_SIDE = 1
        self.LOCATION_OPPONENT_SIDE = -1

        self.TYPE_CREATURE = 0
        self.TYPE_GREEN = 1
        self.TYPE_RED = 2
        self.TYPE_BLUE = 3
    def read_input(self):
        player_health1, player_mana1, player_deck1, player_rune1, player_draw1 = map(int, input().split())
        player_health2, player_mana2, player_deck2, player_rune2, player_draw2 = map(int, input().split())

        opponent_hand, opponent_actions = map(int, input().split())
        l_opponent_actions = [input() for _ in range(opponent_actions)]

        card_count = int(input())
        l_cards = []
        l_cards = [Card(*(int(x) if i != 7 else x for i, x in enumerate(input().split()[:12]))) for _ in range(card_count)]

        player1 = Player(player_health1, player_mana1, player_deck1, player_rune1, player_draw1)
        player2 = Player(player_health2, player_mana2, player_deck2, player_rune2, player_draw2)

        self.last_state = copy.copy(self.state)
        self.last_summon_strategy = self.summon_strategy
        self.last_attack_strategy = self.attack_strategy

        self.state = State(player1, player2, opponent_hand, l_opponent_actions, l_cards)
    
    # ----------------------------------------------
    # Select best action to do depending on the phase
    # ----------------------------------------------
    def act(self):
        if self.state.is_draft_phase():
            self.ia_draft()
        else:
            self.ia_battle()
    
    # ----------------------------------------------
    # IA for pick
    # ----------------------------------------------
    def ia_draft(self):
        best_card = self.draft.pick_card(self.state.l_cards)
        print("PICK " + str(best_card))

    # ----------------------------------------------
    # IA for battle
    # ----------------------------------------------
    def ia_battle(self):
        best_reward = -math.inf
        best_turn = []
        for x in range(1, 120):
            self.summon_strategy = random.randint(1, 7)
            self.attack_strategy = random.choice([1, 3, 5, 6, 7, 8, 12, 13])
            # print("Strategies: " + str(self.summon_strategy) + " " + str(self.attack_strategy), file=sys.stderr)
            turn = Turn(self.state, self.summon_strategy, self.attack_strategy)
            # print("Reward: " + str(turn.reward), file=sys.stderr)
            turn_string = ""
            for action in turn.l_turn:
                turn_string += action
            # print("string: " + turn_string, file=sys.stderr)
            if turn.reward > best_reward:
                best_reward = turn.reward
                best_turn = turn.l_turn
            elif turn.reward == best_reward:
                if random.randint(0, 1):
                    best_reward = turn.reward
                    best_turn = turn.l_turn
        if len(best_turn) == 0:
            print("PASS")
        else:
            turn_string = ""
            for action in best_turn:
                turn_string += action
            print(turn_string)
    
    # ----------------------------------------------
    # Calculate reward
    # ----------------------------------------------
    def reward(self):
        return self.state.player1.hp - self.last_state.player1.hp + self.last_state.player2.hp - self.state.player2.hp

if __name__ == '__main__':
    agent = BeamSearchAgent()

    while True:
        agent.read_input()
        agent.act()
        