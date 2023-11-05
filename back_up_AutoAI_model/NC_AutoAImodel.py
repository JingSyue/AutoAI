from pypokerengine.players import BasePokerPlayer
import numpy as np
import itertools
import random
import warnings
import joblib
from keras.models import Sequential
from keras.models import model_from_json
import tensorflow as tf
from tensorflow import keras

class NC_AutoAImodel(BasePokerPlayer):  
    def declare_action(self, valid_actions, hole_card, round_state):
        # valid_actions format => [raise_action_info, call_action_info, fold_action_info]
        
        if self.first_action==1:
            self.set_blind_order(self.get_position(round_state['next_player']))
        
        action_predict= self.predict_action(valid_actions)
        action=action_predict['action']
        amount=action_predict['amount']
        print("action predict in new cnn")
        #self.print_game_data()
        return action, amount   # action returned here is sent to the poker engine

    def receive_game_start_message(self, game_info):
        self.set_players(game_info['player_num'])
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
        #print("set community cards in New CNN: ",self.game_data)
        return None

    def receive_game_update_message(self, action, round_state):
        player_uuid = action['player_uuid']
        amount = action['amount']
        self.set_player_action(action)
        self.set_player_chips(player_uuid,amount)
        return None

    def receive_round_result_message(self, winners, hand_info, round_state):
        return None
    
    #data transformation
    def set_player_chips(self,player_uuid,amount):
        if player_uuid not in self.player_amounts:
            self.player_amounts[player_uuid] = 0
        # Update the sum of the amount for the player.
        self.player_amounts[player_uuid]+=amount
        # You can print the updated data for debugging or further processing.
        max_player = max(self.player_amounts, key=lambda player_uuid: self.player_amounts[player_uuid])
        index=0
        for player, chips in self.player_amounts.items():
            if chips < self.player_amounts[max_player] / 3:
                chip_strength = 1
            elif chips < (2 * self.player_amounts[max_player] / 3):
                chip_strength = 2
            else:
                chip_strength = 3
            self.store_chips_to_game_data(index, chip_strength)
            index+=1
        #print(f"Player {player_uuid} has a total amount of {self.player_amounts[player_uuid]}")
        return None

    def store_chips_to_game_data(self,index,chip_strength):
        #print("index: ",index,chip_strength)
        #chip strength 3:001,2:010,1:100
        self.game_data[9][index*3:index*3+3] = [0, 0, 0]
        self.game_data[9][index*3+chip_strength-1] = 1
        #self.print_game_data()
        return None
    
    def set_player_action(self,action):
        if(self.get_players()==3):
            indices = np.argwhere(self.game_data[10] == -1)
            if indices.size > 0:
                index = indices[0][0]
                self.game_data[10][index] = self.get_action(action)
                if self.get_action(action)==8: # action==fold
                    self.set_fold_in_bs(index%3+1)
                
        elif(self.get_players()==4):
            indices = np.argwhere(self.game_data[10] == -1)
            if indices.size > 0:
                index = indices[0][0]
                self.game_data[10][index] = self.get_action(action)
                if self.get_action(action)==8: # action==fold
                    self.set_fold_in_bs(index%4+1)
        #self.print_game_data()
        return None

    def set_fold_in_bs(self,player_number):
        self.game_data[11][3*player_number-2:3*player_number]=0
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

    def get_action(self,action):
        if(action['action']=="post small blind"):
            return 0
        elif(action['action']=="post big blind"):
            return 1
        elif(action['action']=="raise"):
            return 2
        elif(action['action']=="call" and action['amount']>0):
            return 3
        #action 4 = check
        elif(action['action']=="call" and action['amount']==0):
            return 4
        elif(action['action']=="fold"):
            return 8
        return -1

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
    
    def set_hands(self,hands):
        #print("new_cnn receive hand1 and hand2 from ai model: ",hands)
        self.hand1=hands[0]
        self.hand2=hands[1]
        self.store_to_game_data(hands[0],6)
        self.store_to_game_data(hands[1],7)
        #once you know the hands value you can update strength
        cards=[self.hand1,self.hand2]
        #print("strength from set hands: ",self.set_strength(cards))
        self.store_strength_to_game_data(self.set_strength(cards))
        #self.print_game_data()
        return None
    
    def set_players(self,player_count):
        self.player_count=player_count
        return None

    def get_players(self):
        return self.player_count

    def print_game_data(self):
        print("game data from new cnn: \n",self.game_data)
        return None
    
    def store_to_game_data(self,cards,row):
        #row 1 means storing to array row index 1
        #1~3: flop1~3
        #4: turn
        #5: river
        #6: hand0
        #7: hand1
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
    # Count the occurrences of each face value and suit
        face_counts = {}
        suit_counts = {}
        for card in cards:
            face = card['face']
            suit = card['suite']

            face_counts[face] = face_counts.get(face, 0) + 1
            suit_counts[suit] = suit_counts.get(suit, 0) + 1

        # Check for flush
        flush = any(count >= 5 for count in suit_counts.values())

        # Check for straight
        straight = False
        faces = sorted(face_counts.keys())

        if len(faces) >= 5:
            for i in range(len(faces) - 4):
                if faces[i] + 4 == faces[i + 4]:
                    straight = True
                    break

        # Check for straight flush and royal flush
        straight_flush = straight and flush
        royal_flush = straight_flush and 1 in faces and 10 in faces and 11 in faces and 12 in faces and 13 in faces

        # Determine the strength based on the hand
        if royal_flush:
            return 12
        elif straight_flush:
            return 11
        elif any(count == 4 for count in face_counts.values()):
            return 10
        elif set(face_counts.values()) == {2, 3}:
            return 9
        elif flush:
            return 8
        elif straight:
            return 7
        elif any(count == 3 for count in face_counts.values()):
            return 6
        elif len(face_counts) == 3 and set(face_counts.values()) == {1,2,2}:
            return 5
        elif any(count == 2 for count in face_counts.values()):
            return 4
        elif len(faces) >= 5:
            return 3
        elif len(faces) >= 4:
            return 2
        elif len(faces) >= 3:
            return 1
        else:
            return 0
        
    def store_strength_to_game_data(self,strength):
        self.game_data[0][:] = [0]
        self.strength=strength
        self.game_data[0][strength]=1
        return None
    
    def new_game_data(self):
        if(self.get_players()==3):
            self.game_data = np.full((12, 13), 0)
            #flop1,2,3,turn,river initial=-1 
            self.game_data[1:6, :] = -1
            #action initial=-1
            self.game_data[10][0]=0
            self.game_data[10][1]=1
            self.game_data[10:11,2:]=-1
            self.game_data[11]=-1
            self.in_chips=np.zeros(3)
            
        elif(self.get_players()==4):
            self.game_data = np.full((12, 13), 0)
            #flop1,2,3,turn,river initial=-1 
            self.game_data[1:6, :] = -1
            #action initial=-1
            self.game_data[10][0]=0
            self.game_data[10][1]=1
            self.game_data[10:11,2:]=-1
            self.game_data[11]=-1
            self.in_chips=np.zeros(4)
        return None

    def card_convert(self,card):
        card_converted=card
        #note that card face A should be sent in as 1 
        if card_converted['face']==1:
            card_converted['face']=14
        card_converted=card
        if card['suite']=="club":
            card_converted['face']=-4+(card['face']-1)*4
        elif card['suite']=="diamond":
            card_converted['face']=-3+(card['face']-1)*4
        elif card['suite']=="heart":
            card_converted['face']=-2+(card['face']-1)*4
        elif card['suite']=="spade":
            card_converted['face']=-1+(card['face']-1)*4
        return card_converted['face']

    def set_flops(self,flop1,flop2,flop3):
        #print("new_cnn receive flops from ai model: ",flop1,flop2,flop3)
        self.store_to_game_data(flop1,1)
        self.store_to_game_data(flop2,2)
        self.store_to_game_data(flop3,3)
        cards=[self.hand1,self.hand2,self.flop1,self.flop2,self.flop3]
        #print("strength from set flops: ",self.get_highest_strength(cards))
        return None
    
    def get_highest_strength(self,all_cards):
        combinations = itertools.combinations(all_cards, 5)
        max_strength = 0

        for combination in combinations:
            strength = self.set_strength(combination)
            max_strength = max(max_strength, strength)

        self.strength=max_strength
        self.store_strength_to_game_data(max_strength)
        return max_strength
    
    def set_turn(self,turn):
        #print("new_cnn receive turn from ai model: ",turn)
        self.store_to_game_data(turn,4)
        #print("game_data_from new_cnn after turn: ",self.game_data)
        cards=[self.hand1,self.hand2,self.flop1,self.flop2,self.flop3,self.turn]
        #print("strength from set turn: ",self.get_highest_strength(cards))
        return None

    def set_river(self,river):
        #print("new_cnn receive river from ai model: ",river)
        self.store_to_game_data(river,5)
        cards=[self.hand1,self.hand2,self.flop1,self.flop2,self.flop3,self.turn,self.river]
        #print("strength from set river: ",self.get_highest_strength(cards))
        return None

    def set_blind_order(self,position): 
        #ai itself is small blind 0 else 1
        #0 for small blind 1 for big blind
        self.position=position
        if self.get_players()==3:
            if self.position==0:
                indices_values = [(0, 1), (3, -1), (6, 0), (12, 2)]
                for index, value in indices_values:
                    self.game_data[11][index] = value
            elif self.position==1:
                indices_values = [(0, -1), (3, 0), (6, 1), (12, 1)]
                for index, value in indices_values:
                    self.game_data[11][index] = value
            elif self.position==2:
                indices_values = [(0, 0), (3, 1), (6, -1), (12, 3)]
                for index, value in indices_values:
                    self.game_data[11][index] = value

        elif self.get_players()==4:
            if self.position==0:
                indices_values = [(0, -1), (3, -1), (6, 0), (9, 1),(12, 2)]
                for index, value in indices_values:
                    self.game_data[11][index] = value
            elif self.position==1:
                indices_values = [(0, -1), (3, 0), (6, 1), (9, -1),(12, 1)]
                for index, value in indices_values:
                    self.game_data[11][index] = value
            elif self.position==2:
                indices_values = [(0, 1), (3, -1), (6, -1), (9, 0),(12, 3)]
                for index, value in indices_values:
                    self.game_data[11][index] = value
            elif self.position==3:
                indices_values = [(0, 0), (3, 1), (6, -1), (9, -1),(12, 4)]
                for index, value in indices_values:
                    self.game_data[11][index] = value

        #print("new_cnn blind/show in blind: ",self.game_data[11])
        self.first_action+=1
        #self.print_game_data()
        return None
    
    #decide which level and store level are seperate functions, considering old cnn and new cnn store data differently
    #You can see more info in the document
    def store_level_to_game_data(self,level):
        self.game_data[8][2*level-2:2*level+1] = [1]
        return None
            
    def set_level(self,hand1,hand2,suit_same):
        #find hand1 and hand2 in level array
        if(suit_same):
            level=self.level_array[14-hand1][14-hand2]
        else:
            level=self.level_array[14-hand2][14-hand1]
        return level
    
    def set_hand_level(self,cards):
        #You can change the hand level simply by changing the array value 
        self.level_array = np.array([[1,1,2,2,3,3,3,3,3,3,3,3,3], 
                                     [1,1,2,3,3,4,5,6,6,6,6,6,6], 
                                     [2,2,1,3,4,4,5,6,6,6,6,6,6],
                                     [3,3,3,2,4,4,5,6,6,6,6,6,6],
                                     [4,4,4,4,2,4,4,5,6,6,6,6,6],
                                     [4,5,5,5,5,3,4,5,5,6,6,6,6],
                                     [4,6,6,5,5,5,3,4,5,6,6,6,6],
                                     [4,6,6,6,6,5,5,4,4,5,6,6,6],
                                     [4,6,6,6,6,6,5,5,4,4,5,6,6],
                                     [4,6,6,6,6,6,6,6,5,4,5,6,6],
                                     [5,6,6,6,6,6,6,6,6,6,4,5,6],
                                     [5,6,6,6,6,6,6,6,6,6,6,4,6],
                                     [5,6,6,6,6,6,6,6,6,6,6,6,4]])
        #print("level array:\n",level_array)   
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
            if 8<=self.strength<=12:#all in
                predict_action={'action':'raise','amount':predict_action['amount']['max']}
            elif 4<=self.strength<=7:
                predict_action={'action':'raise','amount':min(self.to_call+3*self.sb,predict_action['amount']['max'])}
            elif 2<=self.strength<=3:
                predict_action={'action':'raise','amount':min(self.to_call+2*self.sb,predict_action['amount']['max'])}
            else:
                predict_action={'action':'raise','amount':min(self.to_call+self.sb,predict_action['amount']['max'])}
            return predict_action
        
        #call and check will see the amount to_call if to_call is too large then it will fold
        elif predict_action['action']=='call': 
            if self.strength==0 and self.to_call>8*self.sb:
                predict_action={'action':'fold','amount':0}
        else:
            predict_action=valid_action

        print("this is predict action",predict_action)
        return predict_action
    
    def predict(self):
        with open('F:\\AutoAI\\NCmodel\\model.config', 'r') as json_file: #path
            json_string = json_file.read()
        model = Sequential()
        model = model_from_json(json_string)
        model.load_weights('F:\\AutoAI\\NCmodel\\model.weight', by_name=False) #path
        input=np.array(self.game_data)
        X2 = input.astype('float32')  
        X1 = X2.reshape(1,12,13,1)
        predictions = model.predict(X1)
        predict = np.argmax(predictions,1)
        action_number = predict[0]
        print("New CNN predict number:",action_number)
        predict_action=self.get_predict_action(action_number)
        print("New CNN predict action:",predict_action)
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
