import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

class Chart():
    def __init__(self, player_number,max_round):
        self.player_wins = {}
        self.round_count = 0
        self.round_stacks = {}
        self.player_number = player_number
        self.max_round=max_round
        
        
    def round_result_chart(self, winners, round_state):
        self.round_count += 1
        for winner in winners:
            winner_name = winner['name']
            winner_stack = winner['stack']
            if winner_name not in self.player_wins:
                self.player_wins[winner_name] = 1
            else:
                self.player_wins[winner_name] += 1

        for player in round_state['seats']:
            player_name = player['name']
            player_stack = player['stack']
            if player_name not in self.round_stacks:
                self.round_stacks[player_name] = [player_stack]
            else:
                self.round_stacks[player_name].append(player_stack)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        save_path = f'testchart\\{self.player_number}players\\round{self.round_count}stack{timestamp}.png'

        players = list(self.round_stacks.keys())
        x_values = np.linspace(0, 1, self.round_count)

        player_colors = {
            'RF': '#1f77b4',
            'NC2':'#9467bd',
            'NC': '#2ca02c',
            'OC': '#d62728'
        }
        
        if self.max_round==self.round_count or sum(1 for seat in round_state['seats'] if seat['stack'] != 0)==1:
            plt.figure(figsize=(30, 10))

            for i, player in enumerate(players):
                stacks = self.round_stacks[player]
                color = player_colors.get(player, 'gray')  # Get the color from the dictionary
                plt.plot(x_values, stacks, label=f'{player}', color=color,linewidth=10.0)

            plt.xlabel('Round',fontsize=30)
            plt.ylabel('Values',fontsize=30)
            plt.title('Player Stacks',fontsize=30)
            plt.xticks(x_values, [f'{i+1}' for i in range(self.round_count)])
            plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 10})
            plt.savefig(save_path, dpi=100)
            plt.show()
        
        
