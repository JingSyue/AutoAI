import numpy as np
import csv
from datetime import datetime
import pandas as pd


#used for storing training data
class Store_data_set():
    def __init__(self,player_number):
        self.player_number=player_number
        return None
    
    def store_data(self,poker_data):
        flattened_data = np.array(poker_data).flatten() 
        if self.player_number==4:
            with open('store_data_set\\NC_4_players_data_set.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(flattened_data)
        elif self.player_number==3:
            with open('store_data_set\\NC_3_players_data_set.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(flattened_data)
        #print('poker_data',poker_data)
        return None
    
