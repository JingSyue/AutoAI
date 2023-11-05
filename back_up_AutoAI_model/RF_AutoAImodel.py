from pypokerengine.players import BasePokerPlayer
import numpy as np
import random
import json
import joblib
import tensorflow as tf
from tensorflow import keras


class RF_AutoAImodel(BasePokerPlayer):  # Do not forget to make parent class as "BasePokerPlayer"
    #  we define the logic to make an action through this method. (so this method would be the core of your AI)
    def declare_action(self, valid_actions, hole_card, round_state):
        # valid_actions format => [raise_action_info, call_action_info, fold_action_info]
        print("valid actions in RF: ",valid_actions)
        action_predict= self.predict_action(valid_actions)
        action=action_predict['action']
        amount=action_predict['amount']
        print("action predict in rf")
        return action, amount   # action returned here is sent to the poker engine

    def receive_game_start_message(self, game_info):
        self.game_data = np.zeros(15)
        self.game_data[10:16] = -1
        self.game_data[8]=0
        self.game_data[9]=1
        self.sb=game_info['rule']['small_blind_amount']
        self.in_chips=np.zeros(15)
        #print("small blind: ",self.sb)
        #print("game_data_from_old_rf: \n",self.game_data)
        return None

    def receive_round_start_message(self, round_count, hole_card, seats):
        #print("in RF_Auto receive_round_start_message hole card ",hole_card)
        #covert suite and face 
        self.hand1=self.convert_suite_and_face(hole_card[0])
        self.hand2=self.convert_suite_and_face(hole_card[1])
        hands=[self.hand1,self.hand2]
        self.set_hands(hands)
        return None

    def receive_street_start_message(self, street, round_state):  
        if street=="flop":
            self.flop1=self.convert_suite_and_face(round_state['community_card'][0])
            self.flop2=self.convert_suite_and_face(round_state['community_card'][1])
            self.flop3=self.convert_suite_and_face(round_state['community_card'][2])
            self.game_data[0]=self.card_convert(self.flop1.copy())
            self.game_data[1]=self.card_convert(self.flop2.copy())
            self.game_data[2]=self.card_convert(self.flop3.copy())
        if street=="turn":
            self.turn=self.convert_suite_and_face(round_state['community_card'][3])
            self.game_data[3]=self.card_convert(self.turn.copy())
        if street=="river":
            self.river=self.convert_suite_and_face(round_state['community_card'][4])
            self.game_data[4]=self.card_convert(self.river.copy())

        #print("set community cards in rf: ",self.game_data)
        return None

    def receive_game_update_message(self, action, round_state):
        self.set_action(action)
        self.set_chips(round_state['next_player']-1,action['amount'])
        return None

    def receive_round_result_message(self, winners, hand_info, round_state):
        self.game_data = np.zeros(15)
        self.game_data[10:16] = -1
        self.game_data[8]=0
        self.game_data[9]=1
        self.in_chips=np.zeros(15)
        return None
    
    #RF-------model------data------format----translation 
    def set_action(self,action):
        action_number=self.get_action(action)
        if np.count_nonzero(self.game_data == -1)!=0:
            self.game_data[np.argmax(self.game_data[10:16] == -1)+10]=action_number
        else:
            self.game_data[10:16] = -1
            self.set_action(action)
        #print("game_data_from_old_rf: \n",self.game_data)
        return None
    
    def set_chips(self,action_player_index,chips):
        self.in_chips[action_player_index]+=chips
        self.game_data[5]=np.amax(self.in_chips)
        return None

    def convert_suite_and_face(self,card):
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
        self.hand1=hands[0]
        self.hand2=hands[1]
        self.game_data[6]=self.card_convert(hands[0].copy())
        self.game_data[7]=self.card_convert(hands[1].copy())
        #print("set hands in RF Auto: ",self.game_data)
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
    
    def get_action(self,action):
        if(action['action']=='raise'):
            return 2
        elif(action['action']=='call' and action['amount']>0):
            return 3
        #action check=4
        elif(action['action']=='call' and action['amount']==0):
            return 4
        elif(action=="fold"):
            return 8
        elif(action=="allin"):
            return 9
        return -1
    
    def get_predict_action(self,action):
        if action==2:#raise
            predict_action={'action':'raise' ,"amount":50}
            return predict_action
        elif action==3:#call
            predict_action={'action':'call' ,"amount":50}
            return predict_action
        elif action==4:#check
            predict_action={'action':'call' ,"amount":0}
            return predict_action
        elif action==8:#fold
            predict_action={'action':'fold' ,"amount":0}
            return predict_action
        elif action==9:#all-in
            predict_action={'action':'raise','amount':0}
            return predict_action
        else:
            predict_action={'action':'check' ,"amount":0}
            return predict_action
    
    def predict_action(self,valid_actions):
        predict_action=valid_actions[1]
        action=self.predict()
        for valid_action in valid_actions:
            if valid_action['action'] == action['action']:
                predict_action=valid_action
                break
        if predict_action['action']=='raise' and predict_action['amount']!=0:
            predict_action={'action':'raise','amount':min(predict_action['amount']['max'],2*self.sb)}
            return predict_action
        elif predict_action['action']=='check':
            predict_action={'action':'call','amount':0}
        elif predict_action['action']=='raise' and predict_action['amount']==0:
            predict_action={'action':'raise','amount':predict_action['amount']['max']}
        else:
            predict_action=valid_action
            return predict_action
        
        
    def predict(self):
        model = joblib.load(r"F:\AutoAI\RFmodel\my_random_forest.joblib")#path
        action_number= int(float(model.predict(np.array(self.game_data).reshape(1, -1))))
        #print("RF predict number:",action_number)
        predict_action=self.get_predict_action(action_number)
        #print("RF predict action: ",predict_action)
        return predict_action 
    
