from pypokerengine.players import BasePokerPlayer
import numpy as np
import itertools
import random
import joblib
from keras.models import Sequential
from keras.models import model_from_json
import tensorflow as tf
from tensorflow import keras
from collections import Counter
import sys
import matplotlib.pyplot as plt
import warnings
import math
from testchart.chart import *

class OC_AutoAImodel(BasePokerPlayer):  # Do not forget to make parent class as "BasePokerPlayer"
    #  we define the logic to make an action through this method. (so this method would be the core of your AI)
    def declare_action(self, valid_actions, hole_card, round_state):
        # valid_actions format => [raise_action_info, call_action_info, fold_action_info]

        if self.first_action==1:
            self.set_blind_order(self.get_position(round_state['next_player']))
        
        action_predict= self.predict_action(valid_actions)
        action=action_predict['action']
        amount=action_predict['amount']
        print("action predict in old cnn")
        self.print_game_data()
        return action, amount   # action returned here is sent to the poker engine

    def receive_game_start_message(self, game_info):
        self.set_players(game_info['player_num'])
        self.ROUND_RESULT_CHART=Chart(self.get_players(),game_info['rule']['max_round'])
        self.sb=game_info['rule']['small_blind_amount']
        return None

    def receive_round_start_message(self, round_count, hole_card, seats):
        self.new_game_data()
        self.first_action=1
        self.hand1=self._convert_suite_and_face(hole_card[0])
        self.hand2=self._convert_suite_and_face(hole_card[1])
        hands=[self.hand1.copy(),self.hand2.copy()]
        self.set_hands(hands)
        self.set_hand_level(hands)
        self.in_chips=np.zeros(self.get_players())
        self.player_amounts = {}
        #self.print_game_data()
        return None

    def receive_street_start_message(self, street, round_state):
        if street=="flop":
            self.flop1=self._convert_suite_and_face(round_state['community_card'][0])
            self.flop2=self._convert_suite_and_face(round_state['community_card'][1])
            self.flop3=self._convert_suite_and_face(round_state['community_card'][2])
            self.set_flops(self.flop1.copy(),self.flop2.copy(),self.flop3.copy())
        if street=="turn":
            self.turn=self._convert_suite_and_face(round_state['community_card'][3])
            self.set_turn(self.turn.copy())
        if street=="river":
            self.river=self._convert_suite_and_face(round_state['community_card'][4])
            self.set_river(self.river.copy())
        #self.print_game_data()
        return None

    def receive_game_update_message(self, action, round_state):
        player_uuid = action['player_uuid']
        amount = action['amount']
        self.set_player_chips(player_uuid,amount)
        #self.print_game_data()
        return None

    def receive_round_result_message(self, winners, hand_info, round_state):
        if self.position==0:
            self.ROUND_RESULT_CHART.round_result_chart(winners,round_state)
        return None
    
    #data transformation
    def new_game_data(self):
        self.game_data = np.full((13, 13), 0)
        #flop1,2,3,turn,river initial=-1 
        self.game_data[1:6, :] = -1
        self.in_chips=np.zeros(4)# Old Cnn is for two players but 2 more for extention
        self.in_chips_level=np.zeros(4)
        self.strength=0
        self.riverReceived=0
        self.chips_to_call=-1
        #noted that for multi players 1 v.s 1's blind order is set randomly
        return None
    
    def set_player_chips(self,player_uuid,amount):
        if player_uuid not in self.player_amounts:
            self.player_amounts[player_uuid] = 0
        # Update the sum of the amount for the player.
        self.player_amounts[player_uuid]+=amount
        index=0
        for player, chips in self.player_amounts.items():
            self.in_chips[index]=chips
            self.store_chips_level(index)
            index+=1
        #print(f"Player {player_uuid} has a total amount of {self.player_amounts[player_uuid]}")
        return None
    
    def predict_action(self,valid_actions):
        predict_action=valid_actions[1]
        action=self.predict()
        self.to_call=0
        
        for valid_action in valid_actions:
            if valid_action['action'] =="call":
                self.to_call=valid_action['amount']
            if valid_action['action'] == action['action']:
                predict_action=valid_action
                print("this is predict action",predict_action)
                break


        if predict_action['action']=='raise' and predict_action['amount']!=0:
            if 11<=self.strength<=12:#all in
                predict_action={'action':'raise','amount':predict_action['amount']['max']}
            elif 4<=self.strength<=10:
                predict_action={'action':'raise','amount':min(self.to_call+4*self.sb,predict_action['amount']['max'])}
            elif 2<=self.strength<=3:
                predict_action={'action':'raise','amount':min(self.to_call+3*self.sb,predict_action['amount']['max'])}
            else:
                predict_action={'action':'raise','amount':min(self.to_call+2*self.sb,predict_action['amount']['max'])}
            return predict_action
        
        
        elif predict_action['action']=='call': 
            predict_action=valid_action

        print("this is predict action",predict_action)
        return predict_action
        
    def predict(self):
        
        if self.strength<3 and self.riverReceived==1:
            predict_action={'action':'fold' ,"amount":0}
            return predict_action
        else:
            with open('F:\\AutoAI\\OCmodel\\model.config', 'r') as text_file: #path
                json_string = text_file.read()
            model = Sequential()
            model = model_from_json(json_string)
            model.load_weights('F:\\AutoAI\\OCmodel\\model.weight', by_name=False) #path
            # read my data
            input=np.array(self.game_data)
            X2 = input.astype('float32')  
            X1 = X2.reshape(1,13,13,1)
            predictions = model.predict(X1)
            predict = np.argmax(predictions,1)
            action_number = predict[0]
            print("Old CNN predict number:",action_number)
            predict_action=self.get_predict_action(action_number)
            print("Old CNN predict action:",predict_action)
        return predict_action
    
    def get_predict_action(self,action):
        if action==0:#raise
            predict_action={'action':'raise' ,"amount":50}
            return predict_action
        elif action==1:#call
            predict_action={'action':'call' ,"amount":50}
            return predict_action
        elif action==2:#check
            predict_action={'action':'call' ,"amount":0}
            return predict_action
        else:
            predict_action={'action':'check' ,"amount":0}
            return predict_action
    
    def print_in_chips(self):
        print("old cnn in_chips: ",self.in_chips)
        return None

    def store_chips_level(self,player_id):
        if self.in_chips[player_id-1]<=1:
            self.in_chips_level[player_id-1]=0
        elif self.in_chips[player_id-1]<17:
            self.in_chips_level[player_id-1]=1
        elif self.in_chips[player_id-1]<30:
            self.in_chips_level[player_id-1]=2
        elif self.in_chips[player_id-1]<45:
            self.in_chips_level[player_id-1]=3
        elif self.in_chips[player_id-1]<57:
            self.in_chips_level[player_id-1]=4
        elif self.in_chips[player_id-1]<80:
            self.in_chips_level[player_id-1]=5
        elif self.in_chips[player_id-1]<125:
            self.in_chips_level[player_id-1]=6
        elif self.in_chips[player_id-1]<200:
            self.in_chips_level[player_id-1]=7
        elif self.in_chips[player_id-1]<225:
            self.in_chips_level[player_id-1]=8
        elif self.in_chips[player_id-1]<290:
            self.in_chips_level[player_id-1]=9
        elif self.in_chips[player_id-1]<400:
            self.in_chips_level[player_id-1]=10 
        elif self.in_chips[player_id-1]<650:
            self.in_chips_level[player_id-1]=11
        elif self.in_chips[player_id-1]>=650: 
            self.in_chips_level[player_id-1]=12 
        self.store_chips_level_to_game_data(1,self.in_chips_level[0])
        self.store_chips_level_to_game_data(2,self.in_chips_level[1])
        return None

    def store_chips_level_to_game_data(self,player_id,chips_level):
        self.game_data[player_id+8][:]=0
        self.game_data[player_id+8][int(chips_level)]=1
        return None

    def get_position(self,next_player_position):
        #next player 0 1 2
        #this player 2 0 1
        if self.get_players()==3:
            position_array=np.array([2,0,1])
            return position_array[next_player_position]
        #next player 0 1 2 3
        #this player 3 0 1 2
        elif self.get_players()==4:
            position_array=np.array([3,0,1,2])
            return position_array[next_player_position]
        return 0

    def set_blind_order(self,position): #ai itself is small blind 0110 else 0011
        #0 for small blind 1 for big blind
        self.position=position
        if self.position==0:
            self.game_data[11,0:4]=[0,1,1,0]
        else:
            self.game_data[11,0:4]=[0,0,1,1]

        self.first_action+=1
        return None
    
    def set_turn(self,turn):
        #print("old_cnn receive turn from ai model: ",turn)
        self.turn=turn
        self.store_to_game_data(turn,4)
        #print("game_data_from new_cnn after turn: ",self.game_data)
        cards=[self.hand1,self.hand2,self.flop1,self.flop2,self.flop3,self.turn]
        self.get_highest_strength(cards)
        #print("strength from set turn: ",self.get_highest_strength(cards))
        return None
    
    def set_river(self,river):
        #print("old_cnn receive river from ai model: ",river)
        self.riverReceived=1
        self.river=river
        self.store_to_game_data(river,5)
        cards=[self.hand1,self.hand2,self.flop1,self.flop2,self.flop3,self.turn,self.river]
        self.get_highest_strength(cards)
        #print("strength from set river: ",self.get_highest_strength(cards))
        return None

    def set_flops(self,flop1,flop2,flop3):
        #print("old_cnn receive flops from ai model: ",flop1,flop2,flop3)
        self.flop1=flop1
        self.flop2=flop2
        self.flop3=flop3
        self.store_to_game_data(flop1,1)
        self.store_to_game_data(flop2,2)
        self.store_to_game_data(flop3,3)
        cards=[self.hand1,self.hand2,self.flop1,self.flop2,self.flop3]
        self.get_highest_strength(cards)
        #print("strength from set flops: ",self.get_highest_strength(cards))
        return None
    
    def get_highest_strength(self,all_cards):
        strength = self.set_strength(all_cards)
        self.strength = max(self.strength, strength)
        self.store_strength_to_game_data(self.strength)
        return self.strength
    
    def print_game_data(self):
        print("game data from old cnn: \n",self.game_data)
        return None

    def get_players(self):
        return self.player_count
    
    def set_hand_level(self,cards):
        #You can change the hand level simply by changing the array value 
        self.level_array = np.array([[1,1,1,1,1,3,3,3,3,2,2,2,4], 
                                     [1,1,1,1,2,3,3,4,4,4,4,4,5], 
                                     [1,2,1,1,2,3,4,4,4,4,4,5,5],
                                     [2,3,3,1,2,3,4,4,4,4,5,5,5],
                                     [3,3,3,3,1,2,3,4,4,5,5,5,5],
                                     [3,4,4,3,3,2,2,3,4,5,5,5,5],
                                     [4,4,4,4,4,3,2,2,3,4,5,5,5],
                                     [4,4,4,5,4,4,4,2,3,3,4,5,5],
                                     [4,4,5,5,5,5,4,4,2,3,4,4,5],
                                     [4,5,5,5,5,5,5,4,4,3,4,4,5],
                                     [4,5,5,5,5,5,5,5,5,5,3,4,5],
                                     [4,5,5,5,5,5,5,5,5,5,5,3,5],
                                     [5,5,5,5,5,5,5,5,5,5,5,5,3]])
        #print("level array in old cnn:\n",self.level_array)   
        hand1=cards[0]
        hand2=cards[1]
        #hand face 1 trans to 14
        if(hand1['face']==1):
            hand1['face']=14
        if(hand2['face']==1):
            hand2['face']=14
        #hand1 is random variable always bigger than hand2
        if(cards[0]['face']>cards[1]['face']):
            hand1=cards[0]
            hand2=cards[1]
        else:
            hand1=cards[1]
            hand2=cards[0]
        #print("set_hand_level hand1,hand2:",hand1," ", hand2)
        suit_same=0
        if(hand1['suite']==hand2['suite']):
            suit_same=1
        self.level=self.set_level(hand1['face'],hand2['face'],suit_same)
        #print("level from set_hand_level: ",self.level)
        self.store_level_to_game_data(self.level)
        return None
    
    def store_level_to_game_data(self,level):
        if(level<=3):
            self.game_data[8][level-1:level-1+level]=[1]
        elif(level>3):
            self.game_data[8][level*3-7:level*3-7+level]=[1]
        return None

    def set_level(self,hand1,hand2,suit_same):
        #find hand1 and hand2 in level array
        if(suit_same):
            level=self.level_array[14-hand1][14-hand2]
        else:
            level=self.level_array[14-hand2][14-hand1]
        return level

    def _convert_suite_and_face(self,card):
        card_converted={'suite':'suite','face':0}
        if card[0]=='S':
            card_converted['suite']='spade'
        elif card[0]=='C':
            card_converted['suite']='club'
        elif card[0]=='D':
            card_converted['suite']='diamond'
        elif card[0]=='H':
            card_converted['suite']='heart'
        
        if card[1]=='T':
            card_converted['face']=10
        elif card[1]=='J':
            card_converted['face']=11
        elif card[1]=='Q':
            card_converted['face']=12
        elif card[1]=='K':
            card_converted['face']=13
        elif card[1]=='A':
            card_converted['face']=1
        else:
            card_converted['face']=int(card[1])
        return card_converted
    
    def set_players(self,player_count):
        self.player_count=player_count
        return None
    
    def set_hands(self,hands):
        #print("old_cnn receive hand1 and hand2 from ai model: ",hands)
        self.hand1=hands[0]
        self.hand2=hands[1]
        self.store_to_game_data(hands[0],6)
        self.store_to_game_data(hands[1],7)
        #once you know the hands value you can update strength
        cards=[self.hand1,self.hand2]
        #print("strength from set hands: ",self.set_strength(cards))
        self.get_highest_strength(cards)
        self.store_strength_to_game_data(self.set_strength(cards))
        return None
    
    def store_to_game_data(self,cards,row):
        #row 1 means storing to array row index 1
        #1~3: flop1~3
        #4: turn
        #5: river
        #6: hand0
        #7: hand1
        #print("in old cnn id 2 store to game data: cards, r: ",cards,row)
        r=row
        face=cards['face']
        suite=cards['suite']
        #card1 face 1 trans to 14
        if(face==1):
            face=14

        #[row][culumn]
        if(suite=='club'):#club=1
            self.game_data[r, :] = 0
            self.game_data[r][face-2]=1

        elif(suite=='diamond'):#diamond=2
            self.game_data[r, :] = 0
            self.game_data[r][face-2]=2

        elif(suite=='heart'):#heart=3
            self.game_data[r, :] = 0
            self.game_data[r][face-2]=3

        elif(suite=='spade'):#spade=4
            self.game_data[r, :] = 0
            self.game_data[r][face-2]=4
        return None
    
    def set_strength(self,cards):
        if len(cards)<=2:
            if self.find_one_pair(cards):
                return 1
            else:
                return 0
        if self.count_continuous_faces(cards)==4:#strength 12 still need one card to be straight
            return 12
        if self.count_continuous_faces(cards)==3:
            face_array=[card.get('face') for card in cards]
            if max(self.longest_subsequence(cards))+2 in face_array or max(self.longest_subsequence(cards))-4 in face_array:
                return 12
        if self.is_straight_still_need_one_card(cards):
            return 12
        
        if self.count_same_suites(cards)==3 :
            return 11
        if self.count_same_suites(cards)==4:
            return 10
        if len(cards)>=5 and self.find_straight_flush(cards):
            return 8
        if self.count_same_faces(cards)==4:
            return 7
        if self.find_fullhouse(cards)==1:
            return 6
        if self.count_same_suites(cards)>=5:
            return 5
        if self.count_continuous_faces(cards)>=4:
            if self.count_continuous_faces(cards)>=5:
                return 4
            elif self.find_card_with_value(cards,1)['face']==1:
                if self.face_A_is_straight(cards):
                    return 4
        if self.count_same_faces(cards)==3:
            return 3
        if self.find_two_pairs(cards):
            return 2
        if self.find_one_pair(cards):
            return 1
        else:
            return 0
        
    def store_strength_to_game_data(self,strength):
        self.game_data[0][:] = [0]
        self.strength=strength
        self.game_data[0][strength]=1
        return None
    
#functions for strength
    def count_same_suites(self,cards):
        suits_count = Counter(card['suite'] for card in cards)
        max_same_suit_count = max(suits_count.values(), default=0)
        return max_same_suit_count
    
    def get_max_faces(self,cards):
        max_face = -1
        for card in cards:
            if card['face'] > max_face:
                max_face = card['face']
        return max_face
    
    def get_min_faces(self,cards):
        min_face = 20 
        for card in cards:
            if card['face'] < min_face :
                min_face = card['face']
        return min_face
    
    def count_continuous_faces(self,cards):
        faces = set(card['face'] for card in cards)
        continuous_count = 0
        max_continuous_count = 0
        previous_face = None

        for face in sorted(faces):
            if previous_face is not None and face - previous_face == 1:
                continuous_count += 1
            else:
                continuous_count = 1
            max_continuous_count = max(max_continuous_count, continuous_count)

            previous_face = face
        return max_continuous_count
        
    def count_same_faces(self,cards):
        face_count = Counter(card['suite'] for card in cards)
        max_same_face_count = max(face_count.values(), default=0)
        return max_same_face_count
    
    def is_straight_flush(self,hand):
            sorted_hand = sorted(hand, key=lambda x: (x['face'], x['suite']))
            suite = sorted_hand[0]['suite']
            faces = [card['face'] if card['face'] != 1 else 14 for card in sorted_hand]
            
            if len(set(faces)) != 5:
                return False
            for i in range(1, 5):
                if sorted_hand[i]['suite'] != suite or faces[i] != faces[i - 1] + 1:
                    return False
            return True

    def find_straight_flush(self,cards):
        if len(cards) < 5:
            return False
        
        if self.find_card_with_value(cards,1):
            cards.append({'suite': self.find_card_with_value(cards,1)['suite'], 'face': 14})

        combinations = itertools.combinations(cards, 5)

        for combination in combinations:
            if self.is_straight_flush(combination):
                sorted_cards = sorted(combination, key=lambda x: (x['face'], x['suite']))
                print("Found a straight flush combination:")
                for card in sorted_cards:
                    if card['face']==14:
                        card['face']=1
                    print(card)
                return True
        print("No straight flush combination found.")
        return False
    
    def find_card_with_value(self,cards, value):
        for card in cards:
            if card['face'] == value:
                return card
        return None

    def face_A_is_straight(self,cards):
        cards.append({'suite': self.find_card_with_value(cards,1)['suite'], 'face': 14})
        if self.count_continuous_faces(cards)>=5:
            return True
        else:
            return False
    
    def find_fullhouse(self,cards):
        combinations = itertools.combinations(cards, 5)
        for combination in combinations:
            if self.is_fullhouse(combination):
                sorted_cards = sorted(combination, key=lambda x: (x['face'], x['suite']))
                print(sorted_cards)
                return True 
        return False

    def is_fullhouse(self,hand):
        ranks = [card['face'] for card in hand]
        rank_counts = {rank: ranks.count(rank) for rank in set(ranks)}
        if len(rank_counts) != 2 or 3 not in rank_counts.values() or 2 not in rank_counts.values():
            return False
        return True
    
    def find_two_pairs(self,cards):
        if len(cards) < 4:
            return False
        
        combinations = itertools.combinations(cards, 4)

        for combination in combinations:
            if self.is_two_pairs(combination):
                sorted_cards = sorted(combination, key=lambda x: (x['face'], x['suite']))
                print(sorted_cards)
                return True 
        return False
    
    def is_two_pairs(self,hand):
        ranks = [card['face'] for card in hand]
        rank_counts = {rank: ranks.count(rank) for rank in set(ranks)}
        if len(rank_counts) != 2 or not all(count >= 2 for count in rank_counts.values()):
            return False
        return True
    
    def find_one_pair(self,cards):
        if len(cards) < 2:
            return False
        
        combinations = itertools.combinations(cards, 2)

        for combination in combinations:
            if self.is_one_pair(combination):
                sorted_cards = sorted(combination, key=lambda x: (x['face'], x['suite']))
                print(sorted_cards)
                return True 
        return False
    
    def is_one_pair(self,hand):
        ranks = [card['face'] for card in hand]
        rank_counts = {rank: ranks.count(rank) for rank in set(ranks)}
        if len(rank_counts) != 1 or not all(count >= 2 for count in rank_counts.values()):
            return False
        return True

    def longest_subsequence(self,cards):
        a=[card.get('face') for card in cards]
        n=len(a)
        # stores the index of elements
        mp = {i:0 for i in range(13)}
        # stores the length of the longest
        # subsequence that ends with a[i]
        dp = [0 for i in range(n)]
    
        maximum = -sys.maxsize - 1
        # iterate for all element
        index = -1
        for i in range(n):
            
            # if a[i]-1 is present before
            # i-th index
            if ((a[i] - 1 ) in mp):
                
                # last index of a[i]-1
                lastIndex = mp[a[i] - 1] - 1
    
                # relation
                dp[i] = 1 + dp[lastIndex]
            else:
                dp[i] = 1
    
            # stores the index as 1-index as we
            # need to check for occurrence, hence
            # 0-th index will not be possible to check
            mp[a[i]] = i + 1
    
            # stores the longest length 
            if (maximum < dp[i]):
                maximum = dp[i]
                index = i
        # We know last element of sequence is
        # a[index]. We also know that length
        # of subsequence is "maximum". So We
        # print these many consecutive elements
        # starting from "a[index] - maximum + 1"
        # to a[index].
        sequence=[]
        for curr in range(a[index] - maximum + 1,a[index] + 1, 1):
            sequence.append(curr)
            print(curr, end = " ")
        return sequence

    def is_straight_still_need_one_card(self,cards):
        ranks=[card['face'] for card in cards]
        ranks=list(set(sorted(ranks)))
        if 1 in ranks:
            ranks.append(14)
        for card_rank in range(len(ranks)-3):
            if (ranks[card_rank+1]-ranks[card_rank]==1) and (ranks[card_rank+3]-ranks[card_rank+2]==1) and (ranks[card_rank+2]-ranks[card_rank+1]==2):
                return True
        return False
    