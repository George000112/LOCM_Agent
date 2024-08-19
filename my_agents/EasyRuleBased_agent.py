# ------------------------------------------------------------
# ------------------------------------------------------------
# Easy Rule-Based Agent for CodinGame: Legends of Code and Magic
# Version: 1.0
# Coropyright: MIT License
# Author: George from Newcastle university
# ------------------------------------------------------------
# ------------------------------------------------------------
import sys
import math
# prepare for the after improvement
class Action:
    def __init__(self, card_number_and_action):
        split_action = card_number_and_action.split()
        if split_action[1] == "PASS":
            self.action_card_id = None
            self.action = split_action[1]
            self.action_first_object = None
            self.action_second_object = None
        elif split_action[1] == "SUMMON":
            self.action_card_id = int(split_action[0])
            self.action = split_action[1]
            self.action_first_object = int(split_action[2])
            self.action_second_object = None
        elif split_action[1] == "ATTACK":
            self.action_card_id = int(split_action[0])
            self.action = split_action[1]
            self.action_first_object = int(split_action[2])
            self.action_second_object = int(split_action[3])
        elif split_action[1] == "USE":
            self.action_card_id = int(split_action[0])
            self.action = split_action[1]
            self.action_first_object = int(split_action[2])
            self.action_second_object = int(split_action[3])
        else:
            print("action type error")

class Card:
    def __init__(self, card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw):
        self.card_number = card_number
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
        self.remaining_defense = defense
        self.can_attack = True  # Charge is different

class Player:
    def __init__(self, player_health=None, player_mana=None, player_deck=None, player_rune=None, player_draw=None):
        self.health = player_health
        self.mana = player_mana
        self.deck = player_deck # Number of cards in hand
        self.rune = player_rune # Number of runes
        self.draw = player_draw # Number of cards drawn from your hand
        self.my_cards = []  # only myself
        self.action_list = [] # only opponent
    def update_action(self): # only opponent
        opponent_hand, opponent_actions = [int(i) for i in input().split()]
        for i in range(opponent_actions):
            card_number_and_action = input()
            # print(f"Debug messages...{card_number_and_action}", file=sys.stderr, flush=True)
            self.action_list.append(Action(card_number_and_action))
    def update_cards(self, increase_cards=None, decrease_cards=None): # only myself
        if increase_cards:
            self.my_cards.extend(increase_cards)
        if decrease_cards:
            for card in decrease_cards:
                self.my_cards.remove(card)
    
    def action(self, this_cards_list, turn, opponent_player=None): # only myself
        # In the first 30 rounds, draw the most cost-effective cards, 
        # and try to keep the card types and costs even.
        actions = []
        if turn <= 30:
            ideal_mana_curve = [0] * 13 # Maximum 13 costs
            for cost in range(1, 7):
                ideal_mana_curve[cost] = max(0, (6 - abs(cost - 3)))  # Similar to Gaussian distribution

            mana_curve = [0] * 13
            for card in self.my_cards:
                if card.cost < 13:
                    mana_curve[card.cost] += 1

            best_card_index = -1
            best_card_value = -1
            best_card_score = float('inf')
            for i, card in enumerate(this_cards_list):
                ability_score = sum([1 if ability in card.abilities else 0 for ability in "BCDGWL"])
                card_score = card.attack + card.defense + ability_score
                
                if card.cost < 13:
                    new_mana_curve = mana_curve[:]
                    new_mana_curve[card.cost] += 1
                    diff = sum(abs(new_mana_curve[j] - ideal_mana_curve[j]) for j in range(13))
                    
                    if diff < best_card_score or (diff == best_card_score and card_score > best_card_value):
                        best_card_index = i
                        best_card_value = card_score
                        best_card_score = diff

            actions.append(f"PICK {best_card_index}")
            self.update_cards(increase_cards=[this_cards_list[best_card_index]])
        # After more than 30 rounds, the battle phase begins
        else:
            summon_actions = []
            attack_actions = []
            use_actions = []
            my_board = [card for card in this_cards_list if card.location == 1]
            opponent_board = [card for card in this_cards_list if card.location == -1]
            my_creature = [card for card in this_cards_list if card.location == 0 and card.card_type == 0]
            my_item = {"G": [card for card in this_cards_list if card.location == 0 and card.card_type == 1],\
                       "R": [card for card in this_cards_list if card.location == 0 and card.card_type == 2],\
                       "B": [card for card in this_cards_list if card.location == 0 and card.card_type == 3]}
            my_creature.sort(key=lambda card: (card.cost, len(card.abilities)), reverse=True)
            
            # first, summon the charge creatures
            for card in my_creature:
                if 'C' in card.abilities and card.cost <= self.mana and len(my_board) < 6:
                    actions.append(f"SUMMON {card.instance_id}")
                    my_board.append(card)
                    self.mana -= card.cost

            # use items to enhance creatures ability
            my_board.sort(key=lambda card: (card.attack, card.defense, 'D' in card.abilities,), reverse=True)
            for card_type, card_list in my_item.items():
                if card_type == "G": # Green item
                    for card in card_list:
                        for target_card in my_board:
                            if card.cost <= self.mana:
                                use_actions.append(f"USE {card.instance_id} {target_card.instance_id}")
                                self.mana -= card.cost
                                target_card.attack += card.attack
                                target_card.remaining_defense += card.defense
                                break
                elif card_type == "R":  # Red item
                    for card in card_list:
                        for target_card in opponent_board:
                            if card.cost <= self.mana:
                                use_actions.append(f"USE {card.instance_id} {target_card.instance_id}")
                                self.mana -= card.cost
                                target_card.attack += card.attack
                                target_card.remaining_defense += card.defense
                                if target_card.remaining_defense <= 0:
                                    opponent_board.remove(target_card)
                                break
                elif card_type == "B":  # Blue item
                    for card in card_list:
                        if card.cost <= self.mana:
                            use_actions.append(f"USE {card.instance_id} -1")
                            self.mana -= card.cost
                            self.health += card.my_health_change
                            opponent_player.health += card.opponent_health_change

            # # Attack opponent's creatures and player
            my_board.sort(key=lambda card: ('L' in card.abilities, 'D' in card.abilities), reverse=True)
            opponent_guard = [card for card in opponent_board if 'G' in card.abilities]
            my_guard = [card for card in my_board if 'G' in card.abilities]
            # for my_card in my_board:
            #     if my_card.can_attack:
            #         if opponent_guard:
            #             target = min(opponent_guard, key=lambda c: c.remaining_defense)
            #         else:
            #             target = min(opponent_board, key=lambda c: (c.attack, -c.remaining_defense), default=None)
            #         if target:
            #             actions.append(f"ATTACK {my_card.instance_id} {target.instance_id}")
            #             my_card.remaining_defense -= target.attack
            #             target.remaining_defense -= my_card.attack
            #             my_card.can_attack = False
            #             if target.remaining_defense <= 0:
            #                 opponent_board.remove(target)
            #             if my_card.remaining_defense <= 0:
            #                 my_board.remove(my_card)
            #         else:
            #             actions.append(f"ATTACK {my_card.instance_id} -1")
            #             my_card.can_attack = False
            
            while opponent_guard and len(my_guard) != 0:
                if len(my_board) == 0: # avoid eternal loop
                    break
                for my_card in my_board:
                    if my_card.can_attack:
                        if opponent_guard:
                            weakest_guard = min(opponent_guard, key=lambda c: c.remaining_defense)
                            attack_actions.append(f"ATTACK {my_card.instance_id} {weakest_guard.instance_id}")
                            weakest_guard.remaining_defense -= my_card.attack
                            my_card.remaining_defense -= weakest_guard.attack
                            my_card.can_attack = False
                            if my_card.attack >= weakest_guard.remaining_defense:
                                opponent_guard.remove(weakest_guard)
                                opponent_board.remove(weakest_guard)
                            if my_card.remaining_defense <= 0:
                                my_board.remove(my_card)
                                break
                            
            # second, kill the opponet preferentially
            if not opponent_guard:
                total_my_attack = sum(card.attack for card in my_board)
                if total_my_attack >= opponent_player.health:
                    for my_card in my_board:
                        if my_card.can_attack:
                            attack_actions.append(f"ATTACK {my_card.instance_id} -1")
                            my_card.can_attack = False
                elif len(my_board) >= len(opponent_board):
                    for my_card in my_board:
                        if my_card.can_attack:
                            attack_actions.append(f"ATTACK {my_card.instance_id} -1")
                            my_card.can_attack = False
                else:
                    for my_card in my_board:
                        if my_card.can_attack and opponent_board:
                            target = min(opponent_board, key=lambda c: (c.attack, -c.remaining_defense))
                            attack_actions.append(f"ATTACK {my_card.instance_id} {target.instance_id}")
                            my_card.can_attack = False
                            my_card.remaining_defense -= target.attack
                            target.remaining_defense -= my_card.attack
                            if my_card.attack >= target.remaining_defense:
                                opponent_board.remove(target)
                            if my_card.remaining_defense <= 0:
                                my_board.remove(my_card)
                                break
            
            for card in my_creature:
                if card.cost <= self.mana and len(my_board) < 6:
                    actions.append(f"SUMMON {card.instance_id}")
                    my_board.append(card)
                    self.mana -= card.cost

            actions.extend(use_actions)
            actions.extend(attack_actions)
            actions.extend(summon_actions)
            if not actions:
                actions.append("PASS")

        print(";".join(actions))

turn = 0
oppent_info = []
all_cards_list = []
opponent_player = Player()
me_player = Player()

while True:
    turn += 1
    for i in range(2):
        player_health, player_mana, player_deck, player_rune, player_draw = [int(j) for j in input().split()]
        player = Player(player_health, player_mana, player_deck, player_rune, player_draw)
        if i == 0:
            me_player = player
        else:
            opponent_player = player

     # only opponent update action
    opponent_player.update_action()

    card_count = int(input())   
    # print(f"Debug messages...{card_count}", file=sys.stderr, flush=True)
    this_cards_list = []
    for i in range(card_count):
        inputs = input().split()
        card_number = int(inputs[0])
        instance_id = int(inputs[1])
        location = int(inputs[2])
        card_type = int(inputs[3])
        cost = int(inputs[4])
        attack = int(inputs[5])
        defense = int(inputs[6])
        abilities = inputs[7]
        my_health_change = int(inputs[8])
        opponent_health_change = int(inputs[9])
        card_draw = int(inputs[10])
        this_card = Card(card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw)
        all_cards_list.append(this_card)
        this_cards_list.append(this_card)

    # only myself update cards info.
    me_player.action(this_cards_list, turn, opponent_player) 
