# ------------------------------------------------------------
# ------------------------------------------------------------
# MinMaxAgent for CodinGame: Legends of Code and Magic
# Version 1.0
# Coropyright: MIT License
# Author: George from Newcastle university
# ------------------------------------------------------------
# ------------------------------------------------------------

import random
import copy
import numpy as np
import math
import sys

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
    
    def use_mana(self, strategy):
        if strategy == 1:
            # Summon two lanes balanced
            summon_turn = SummonBalanced(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif strategy == 2:
            # Summon only left
            summon_turn = SummonAll(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif strategy == 3:
            # Summon only right
            summon_turn = SummonAll(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif strategy == 4:
            # Summon trying cover two lanes with guard and after summon two lanes balanced
            # summon_turn = scb.SummonCoverOrBalanced(self.turn_state)
            summon_turn = Cover(self.turn_state)
            self.l_turn += summon_turn.l_turn
            self.use_mana(1)
        elif strategy == 5:
            # Summon trying cover two lanes with guard and after summon only left
            # summon_turn = scl.SummonCoverOrLeft(self.turn_state)
            summon_turn = Cover(self.turn_state)
            self.l_turn += summon_turn.l_turn
            self.use_mana(2)
        elif strategy == 6:
            # Summon trying cover two lanes with guard and after summon only right
            # summon_turn = scr.SummonCoverOrRight(self.turn_state)
            summon_turn = Cover(self.turn_state)
            self.l_turn += summon_turn.l_turn
            self.use_mana(3)
        elif strategy == 7:
            # Summon two lanes balanced with cost <
            self.turn_state.l_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=False)
            self.use_mana(1)
        elif strategy == 8:
            # Summon two lanes balanced with cost >
            self.turn_state.l_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=True)
            self.use_mana(1)
        elif strategy == 9:
            # Summon only left with cost <
            self.turn_state.l_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=False)
            self.use_mana(2)
        elif strategy == 10:
            # Summon only left with cost >
            self.turn_state.l_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=True)
            self.use_mana(2)
        elif strategy == 11:
            # Summon only right with cost <
            self.turn_state.l_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=False)
            self.use_mana(3)
        elif strategy == 12:
            # Summon only right with cost >
            self.turn_state.l_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=True)
            self.use_mana(3)
        elif strategy == 13:
            # Summon trying cover two lanes with guard and after summon two lanes balanced with cost <
            # summon_turn = scb.SummonCoverOrBalanced(self.turn_state)
            self.turn_state.l_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=False)
            self.turn_state.l_guard_creatures_on_player_hand.sort(key=lambda x: x.cost, reverse=False)
            self.use_mana(4)
        elif strategy == 14:
            # Summon trying cover two lanes with guard and after summon two lanes balanced with cost >
            # summon_turn = scb.SummonCoverOrBalanced(self.turn_state)
            self.turn_state.l_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=True)
            self.turn_state.l_guard_creatures_on_player_hand.sort(key=lambda x: x.cost, reverse=True)
            self.use_mana(4)
        elif strategy == 15:
            # Summon trying cover two lanes with guard and after summon only left with cost <
            self.turn_state.l_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=False)
            self.turn_state.l_guard_creatures_on_player_hand.sort(key=lambda x: x.cost, reverse=False)
            self.use_mana(5)
        elif strategy == 16:
            # Summon trying cover two lanes with guard and after summon only left with cost >
            self.turn_state.l_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=True)
            self.turn_state.l_guard_creatures_on_player_hand.sort(key=lambda x: x.cost, reverse=True)
            self.use_mana(5)
        elif strategy == 17:
            # Summon trying cover two lanes with guard and after summon only right with cost <
            self.turn_state.l_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=False)
            self.turn_state.l_guard_creatures_on_player_hand.sort(key=lambda x: x.cost, reverse=False)
            self.use_mana(6)
        elif strategy == 18:
            # Summon trying cover two lanes with guard and after summon only right with cost >
            self.turn_state.l_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=True)
            self.turn_state.l_guard_creatures_on_player_hand.sort(key=lambda x: x.cost, reverse=True)
            self.use_mana(6)
        elif strategy == 19:
            # Summon left and after summon right and use objects G-R-B
            self.use_mana(2)
            self.use_mana(3)
            self.use_mana(30)
        elif strategy == 20:
            # Summon right and after summon left and use objects G-R-B
            self.use_mana(3)
            self.use_mana(2)
            self.use_mana(30)
        elif strategy == 21:
            # Cover/balanced cost < and use objects G-R-B
            self.use_mana(13)
            self.use_mana(30)
        elif strategy == 22:
            # Cover/balanced cost < and use objects B-R-G
            self.use_mana(13)
            self.use_mana(27)
        elif strategy == 23:
            # Use objects G-R-B and cover/balanced cost <
            self.use_mana(30)
            self.use_mana(13)
        elif strategy == 24:
            # use abjects G-R-B and cover/balanced cost <
            self.use_mana(30)
            self.use_mana(13)
        elif strategy == 25:
            # use objects B-R-G and balanced cost <
            self.use_mana(35)
            self.use_mana(7)
        elif strategy == 26:
            # balanced cost > and use objects G-R-B
            self.turn_state.l_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=True)
            self.turn_state.l_guard_creatures_on_player_hand.sort(key=lambda x: x.cost, reverse=True)
            self.use_mana(1)
            self.use_mana(30)
        elif strategy == 27:
            # Summon/Use style alexAgent
            summon_turn = SummonUse(self.turn_state)
            self.l_turn += summon_turn.l_turn

        elif strategy == 28:
            # Only use green objects
            summon_turn = UseGreen(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif strategy == 29:
            # Only use red objects
            summon_turn = UseRed(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif strategy == 36:
            # Only use blue objects
            summon_turn = UseBlue(self.turn_state)
            self.l_turn += summon_turn.l_turn
        elif strategy == 30:
            # Only use green, red and blue objects
            self.use_mana(28)
            self.use_mana(29)
            self.use_mana(36)
        elif strategy == 31:
            # Only use green, blue and red objects
            self.use_mana(28)
            self.use_mana(36)
            self.use_mana(29)
        elif strategy == 32:
            # Only use red, green and blue objects
            self.use_mana(29)
            self.use_mana(28)
            self.use_mana(36)
        elif strategy == 33:
            # Only use red, blue and green objects
            self.use_mana(29)
            self.use_mana(35)
            self.use_mana(28)
        elif strategy == 34:
            # Only use blue, green and red objects
            self.use_mana(36)
            self.use_mana(28)
            self.use_mana(29)
        elif strategy == 35:
            # Only use blue, red and green objects
            self.use_mana(36)
            self.use_mana(29)
            self.use_mana(28)

    def attack(self, strategy):
        if strategy == 1:
            # Attack the head if I can
            attack_turn = AttackHead(self.turn_state)
            self.l_turn += attack_turn.l_turn
        elif strategy == 2:
            # Attack the enemy cards before attack head
            attack_turn = AttackCards(self.turn_state)
            self.l_turn += attack_turn.l_turn
        elif strategy == 3:
            # Attack the enemy cards before attack head our cards sort by attack >
            self.turn_state.l_cards_can_attack.sort(key=lambda x: x.attack, reverse=True)
            self.attack(2)
        elif strategy == 4:
            # Attack the enemy cards before attack head his cards sort by defense <
            self.turn_state.l_cards_on_opponent_board.sort(key=lambda x: x.defense, reverse=False)
            self.turn_state.l_opponent_cards_guard.sort(key=lambda x: x.defense, reverse=False)
            self.attack(2)
        elif strategy == 5:
            # Attack the enemy cards before attack head our cards sort by attack > and  his cards sort by defense <
            self.turn_state.l_cards_can_attack.sort(key=lambda x: x.attack, reverse=True)
            self.turn_state.l_cards_on_opponent_board.sort(key=lambda x: x.defense, reverse=False)
            self.turn_state.l_opponent_cards_guard.sort(key=lambda x: x.defense, reverse=False)
            self.attack(2)
        elif strategy == 6:
            # Attack the drain cards after guards and head
            attack_turn = AttackGuards(self.turn_state)
            self.l_turn += attack_turn.l_turn
            attack_turn = AttackDrains(self.turn_state)
            self.l_turn += attack_turn.l_turn
            self.attack(1)
        elif strategy == 7:
            # Attack the lethal cards after guards and head
            attack_turn = AttackGuards(self.turn_state)
            self.l_turn += attack_turn.l_turn
            attack_turn = AttackLethals(self.turn_state)
            self.l_turn += attack_turn.l_turn
            self.attack(1)
        elif strategy == 8:
            # Attack the guards, drain, lethal and head
            attack_turn = AttackGuards(self.turn_state)
            self.l_turn += attack_turn.l_turn
            attack_turn = AttackDrains(self.turn_state)
            self.l_turn += attack_turn.l_turn
            attack_turn = AttackLethals(self.turn_state)
            self.l_turn += attack_turn.l_turn
            self.attack(1)
        elif strategy == 9:
            # Attack the guards, drain, lethal and head sort our cards by attack > and  his cards sort by defense <
            self.turn_state.l_cards_can_attack.sort(key=lambda x: x.attack, reverse=True)
            self.turn_state.l_cards_on_opponent_board.sort(key=lambda x: x.defense, reverse=False)
            self.turn_state.l_opponent_cards_guard.sort(key=lambda x: x.defense, reverse=False)
            self.attack(8)

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
# ------------------------------------------------------------
# Summon strategies class
# ------------------------------------------------------------
# ------------------------------------------------------------
# Summon all creatures
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
        if c.guard:
            self.state.cover = True
        self.state.l_cards_on_player_board.append(c)
        self.state.player2.hp += c.opponent_health_change
        self.state.player1.hp += c.my_health_change
        self.state.player1.draw += c.card_draw
        self.state.player1.mana -= c.cost
        self.state.l_cards_on_player_hand.remove(c)

# ------------------------------------------------------------
# Summon balanced
# ------------------------------------------------------------
class SummonBalanced(SummonAll):
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
# Summon and use
# ------------------------------------------------------------
class SummonUse:
    def __init__(self, state):

        self.state :State = state
        self.l_turn = []
        self.l_cards_on_player_board = []
        self.l_cards_on_opponent_board = []
        self.get_turn()
    
    def get_turn(self):
        self.l_cards_on_player_board += self.state.l_cards_on_player_board
        self.l_cards_on_opponent_board += self.state.l_cards_on_opponent_board
        if len(self.l_cards_on_player_board) < 6:
            self.state.l_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=False)
        else:
            self.state.l_cards_on_player_hand.sort(key=lambda x: x.cost, reverse=True)

        l_cards_can_summon_after = []
        if self.state.cover is not True and len(self.state.l_cards_on_player_board) < 6:
            self.cover()

        while len(self.state.l_cards_on_player_hand) > 0:
            c = self.state.l_cards_on_player_hand[0]
            if c.cost > self.state.player1.mana:
                self.state.l_cards_on_player_hand.remove(c)
                continue
            if c.card_type == self.state.TYPE_CREATURE and len(self.l_cards_on_player_board) >= 6:
                self.state.l_cards_on_player_hand.remove(c)
                l_cards_can_summon_after.append(c)
                continue
            if c.card_type == self.state.TYPE_GREEN and len(self.l_cards_on_player_board) == 0:
                self.state.l_cards_on_player_hand.remove(c)
                continue
            if c.card_type == self.state.TYPE_RED and len(self.l_cards_on_opponent_board) == 0:
                self.state.l_cards_on_player_hand.remove(c)
                continue
            if c.card_type == self.state.TYPE_CREATURE:
                self.summon(c)
            elif c.card_type == self.state.TYPE_GREEN:
                self.use_green(c)
            elif c.card_type == self.state.TYPE_RED:
                self.use_red(c)
            elif c.card_type == self.state.TYPE_BLUE:
                self.use_blue(c)
        self.state.l_cards_on_player_hand = l_cards_can_summon_after
    
    def summon(self, c):
        self.l_turn.append("SUMMON " + str(c.instance_id) + ";")
        if c.charge:
            self.state.l_cards_can_attack.append(c)
        self.state.l_cards_on_player_board.append(c)

        self.l_cards_on_player_board.append(c)
        self.state.player2.hp += c.opponent_health_change
        self.state.player1.hp += c.my_health_change
        self.state.player1.draw += c.card_draw
        self.state.player1.mana -= c.cost
        if c in self.state.l_cards_on_player_hand:
            self.state.l_cards_on_player_hand.remove(c)

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
                self.state.l_cards_on_player_board.append(c)
                self.l_cards_on_player_board.append(c)
                self.state.player2.hp += c.opponent_health_change
                self.state.player1.hp += c.my_health_change
                self.state.player1.draw += c.card_draw
                self.state.player1.mana -= c.cost
                if c in self.state.l_guard_creatures_on_player_hand:
                    self.state.l_guard_creatures_on_player_hand.remove(c)
                if c in self.state.l_cards_on_player_hand:
                    self.state.l_cards_on_player_hand.remove(c)
                self.state.cover = True
                return
        
    def use_blue(self, c):
        if c.defense < 0 and len(self.l_cards_on_opponent_board) > 0:
            best_difference = 30
            c_attack = self.l_cards_on_opponent_board[0]
            for enemyCard in self.l_cards_on_opponent_board:
                difference = abs(enemyCard.defense + c.defense)
                if difference == 0:
                    c_attack = enemyCard
                    break
                elif difference < best_difference:
                    best_difference = difference
                    c_attack = enemyCard
            self.l_turn.append("USE " + str(c.instance_id) + " " + str(c_attack.instance_id) + ";")
            c_attack.defense += c.defense
            c_attack.attack += c.attack
            self.state.player2.hp += c.opponent_health_change
            self.state.player1.hp += c.my_health_change
            self.state.player1.draw += c.card_draw
            if c_attack.defense <= 0:
                if c_attack in self.state.l_opponent_cards_guard:
                    self.state.l_opponent_cards_guard.remove(c_attack)
                if c_attack in self.state.l_opponent_cards_drain:
                    self.state.l_opponent_cards_drain.remove(c_attack)
                if c_attack in self.state.l_opponent_cards_lethal:
                    self.state.l_opponent_cards_lethal.remove(c_attack)
                self.state.l_cards_on_opponent_board.remove(c_attack)
                if c_attack in self.l_cards_on_opponent_board:
                    self.l_cards_on_opponent_board.remove(c_attack)
        else:
            self.l_turn.append("USE " + str(c.instance_id) + " -1;")
            self.state.player2.hp += c.defense
            self.state.player2.hp += c.opponent_health_change
            self.state.player1.hp += c.my_health_change
            self.state.player1.draw += c.card_draw
        self.state.player1.mana -= c.cost
        if c in self.state.l_blue_objects_on_player_hand:
            self.state.l_blue_objects_on_player_hand.remove(c)
        if c in self.state.l_cards_on_player_hand:
            self.state.l_cards_on_player_hand.remove(c)
    
    def use_green(self, c):
        self.l_cards_on_player_board.sort(key=lambda x: x.cost, reverse=True)
        self.l_turn.append("USE " + str(c.instance_id) + " " + str(self.l_cards_on_player_board[0].instance_id) + ";")
        self.l_cards_on_player_board[0].defense += c.defense
        self.l_cards_on_player_board[0].attack += c.attack
        if c.breakthrough:
            self.l_cards_on_player_board[0].breakthrough = True
        if c.charge:
            self.l_cards_on_player_board[0].charge = True
            if self.l_cards_on_player_board[0] not in self.state.l_cards_can_attack:
                self.state.l_cards_can_attack.append(self.l_cards_on_player_board[0])
        if c.drain:
            self.l_cards_on_player_board[0].drain = True
        if c.guard:
            self.l_cards_on_player_board[0].guard = True
        if c.lethal:
            self.l_cards_on_player_board[0].lethal = True
        if c.ward:
            self.l_cards_on_player_board[0].ward = True
        self.state.player2.hp += c.opponent_health_change
        self.state.player1.hp += c.my_health_change
        self.state.player1.draw += c.card_draw
        self.state.player1.mana -= c.cost
        if c in self.state.l_green_objects_on_player_hand:
            self.state.l_green_objects_on_player_hand.remove(c)
        if c in self.state.l_cards_on_player_hand:
            self.state.l_cards_on_player_hand.remove(c)
    
    def use_red(self, c):
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
                if best_coincidence_card in self.state.l_opponent_cards_guard:
                    self.state.l_opponent_cards_guard.remove(best_coincidence_card)
                if best_coincidence_card in self.state.l_opponent_cards_drain:
                    self.state.l_opponent_cards_drain.remove(best_coincidence_card)
                if best_coincidence_card in self.state.l_opponent_cards_lethal:
                    self.state.l_opponent_cards_lethal.remove(best_coincidence_card)
                self.l_cards_on_opponent_board.remove(best_coincidence_card)
                self.state.l_cards_on_opponent_board.remove(best_coincidence_card)
        else:
            best_difference = 100
            c_attack = self.l_cards_on_opponent_board[0]
            for enemyCard in self.l_cards_on_opponent_board:
                difference = abs(enemyCard.defense + c.defense)
                if difference == 0:
                    c_attack = enemyCard
                    break
                elif difference < best_difference:
                    best_difference = difference
                    c_attack = enemyCard
            self.l_turn.append("USE " + str(c.instance_id) + " " + str(c_attack.instance_id) + ";")
            c_attack.defense += c.defense
            c_attack.attack += c.attack
            self.state.player2.hp += c.opponent_health_change
            self.state.player1.hp += c.my_health_change
            self.state.player1.draw += c.card_draw
            if c_attack.defense <= 0:
                if c_attack in self.state.l_opponent_cards_guard:
                    self.state.l_opponent_cards_guard.remove(c_attack)
                if c_attack in self.state.l_opponent_cards_drain:
                    self.state.l_opponent_cards_drain.remove(c_attack)
                if c_attack in self.state.l_opponent_cards_lethal:
                    self.state.l_opponent_cards_lethal.remove(c_attack)
                self.l_cards_on_opponent_board.remove(c_attack)
                self.state.l_cards_on_opponent_board.remove(c_attack)
        self.state.player1.mana -= c.cost
        if c in self.state.l_red_objects_on_player_hand:
            self.state.l_red_objects_on_player_hand.remove(c)
        if c in self.state.l_cards_on_player_hand:
            self.state.l_cards_on_player_hand.remove(c)

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
        if c.charge:
            self.l_cards_on_player_board[0].charge = True
            if self.l_cards_on_player_board[0] not in self.state.l_cards_can_attack:
                self.state.l_cards_can_attack.append(self.l_cards_on_player_board[0])
        if c.drain:
            self.l_cards_on_player_board[0].drain = True
        if c.guard:
            self.l_cards_on_player_board[0].guard = True
        if c.lethal:
            self.l_cards_on_player_board[0].lethal = True
        if c.ward:
            self.l_cards_on_player_board[0].ward = True
        self.state.player2.hp += c.opponent_health_change
        self.state.player1.hp += c.my_health_change
        self.state.player1.draw += c.card_draw
        self.state.player1.mana -= c.cost
        self.state.l_green_objects_on_player_hand.remove(c)

# ------------------------------------------------------------
# Use Red Objects
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
                self.l_cards_on_opponent_board.remove(c_attack)
        self.state.player1.mana -= c.cost
        self.state.l_red_objects_on_player_hand.remove(c)

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
            self.state.l_cards_on_player_board.remove(c)

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
            self.state.l_opponent_cards_lethal.remove(self.state.l_opponent_cards_lethal[n])
        if c.defense <= 0:
            self.state.l_cards_on_player_board.remove(c)
    
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
        self.l_guard_creatures_on_player_hand = []  # list of guard creatures on player hand

        self.l_green_objects_on_player_hand = []  # list of green objects on player hand
        self.l_blue_objects_on_player_hand = []  # list of blue objects on player hand
        self.l_red_objects_on_player_hand = []  # list of red objects on player hand

        self.l_cards_on_player_board = []      # list of cards on the player board
        self.l_cards_on_opponent_board = []    # list of cards on the opponent board

        self.l_player_cards_guard = []         # list of guard cards on player board
        self.l_opponent_cards_guard = []       # list of guard cards on opponent board

        self.l_player_cards_lethal = []        # list of lethal cards on player board
        self.l_opponent_cards_lethal = []      # list of lethal cards on opponent board

        self.l_player_cards_drain = []         # list of drain cards on player board
        self.l_opponent_cards_drain = []       # list of drain cards on opponent board

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
            elif card.location == self.LOCATION_OPPONENT_SIDE:
                self.l_cards_on_opponent_board.append(card)
                if card.guard:
                    self.l_opponent_cards_guard.append(card)
                if card.lethal:
                    self.l_opponent_cards_lethal.append(card)
                if card.drain:
                    self.l_opponent_cards_drain.append(card)

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

    # ---------------------------------------
    # return the value of the cards on the player hand
    def evaluate_state(self):
        if self.player1.hp <= 0:
            return -1000  # Lose
        if self.player2.hp <= 0:
            return 1000  # Win

        evaluation = (self.player1.hp - self.player2.hp)  # Health difference
        evaluation += (self.player_cardvalue() - self.opponent_cardvalue())  # Board control
        return evaluation
    
    # ---------------------------------------
    # return true if the state is terminal
    def is_terminal(self):
        return self.player1.hp <= 0 or self.player2.hp <= 0
    
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
# Player information
# ------------------------------------------------------------
class Player:
    def __init__(self, hp, mana, cards_remaining, rune, draw):
        self.hp = hp
        self.mana = mana
        self.cards_remaining = cards_remaining  # the number of cards in the player's deck
        self.rune = rune  # the next remaining rune of a player
        self.draw = draw  # the additional number of drawn cards

class MinMaxAgent:
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

        self.depth = 2 # depth of the search tree

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
        best_eval, best_turn_actions = self.minimax(self.state, self.depth, True)
        if len(best_turn_actions) == 0:
            print("PASS")
        else:
            turn_string = "".join(best_turn_actions)
            print(turn_string)
    
    # ----------------------------------------------
    # Calculate reward
    # ----------------------------------------------
    def reward(self):
        return self.state.player1.hp - self.last_state.player1.hp + self.last_state.player2.hp - self.state.player2.hp

    # ----------------------------------------------
    # MinMax Cores
    # ----------------------------------------------
    def minimax(self, state, depth, maximizing_player):

        if depth == 0 or state.is_terminal():
            return state.evaluate_state(), []

        best_action_list = []
        if maximizing_player:
            max_eval = -math.inf
            for move in self.get_possible_moves(state):
                new_state, action_list = self.simulate_turn(state, move)
                eval, _ = self.minimax(new_state, depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
                    best_action_list = action_list
            return max_eval, best_action_list
        else:
            min_eval = math.inf
            for move in self.get_possible_moves(state):
                new_state, action_list = self.simulate_turn(state, move)
                eval, _ = self.minimax(new_state, depth - 1, True)
                if eval < min_eval:
                    min_eval = eval
                    best_action_list = action_list
            return min_eval, best_action_list
    
    # ----------------------------------------------
    # Get possible moves
    # ----------------------------------------------
    def get_possible_moves(self, state):
        moves = []
        for x in range(1, 10):
            summon_strategy = random.randint(3, 27)
            attack_strategy = random.randint(1, 9)
            moves.append((summon_strategy, attack_strategy))
        return moves

    def simulate_turn(self, state, move):
        summon_strategy, attack_strategy = move
        turn = Turn(copy.deepcopy(state), summon_strategy, attack_strategy)
        return turn.turn_state, turn.l_turn
    
if __name__ == '__main__':
    agent = MinMaxAgent()

    while True:
        agent.read_input()
        agent.act()
