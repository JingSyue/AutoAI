import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel
from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import seaborn as sns
from PokerEngine.api.game import setup_config, start_poker
from officialAutoAI.NC_AutoAImodel import *
from officialAutoAI.OC_AutoAImodel import *
from officialAutoAI.RF_AutoAImodel import *


# Create a function to run the poker game
def run_poker_game():
    max_round = int(max_round_entry.get())
    initial_stack = int(initial_stack_entry.get())
    small_blind_amount = int(small_blind_entry.get())

    global player_number
    player_number = int(player_number_entry.get())

    player_names = ["Player" + str(i) for i in range(1, player_number + 1)]
    config = setup_config(max_round=max_round, initial_stack=initial_stack, small_blind_amount=small_blind_amount)

    for name in player_names:
        algorithm = player_algorithms[name].get()
        if algorithm == "RF_AutoAImodel":
            config.register_player(name, algorithm=RF_AutoAImodel())
        elif algorithm == "OC_AutoAImodel":
            config.register_player(name, algorithm=OC_AutoAImodel())
        elif algorithm == "NC_AutoAImodel":
            config.register_player(name, algorithm=NC_AutoAImodel())

    game_result = start_poker(config, verbose=1)

    stack = {}
    for player in game_result['players']:
        stack[player['name']] = player['stack']

    max_stack_player = max(game_result['players'], key=lambda x: x['stack'])
    winner = max_stack_player['name']
    winner_stack = max_stack_player['stack']

    labels = [f"{player['name']} - {player_algorithms[player['name']].get()}" for player in game_result['players']]
    values = list(stack.values())

    plt.figure(figsize=(10, 6))
    sns.barplot(x=values, y=labels, palette='viridis')
    plt.xlabel('Stack Size')
    plt.ylabel('Algorithm')
    plt.title(f'Stack Size by Algorithm - Round {max_round}')
    plt.show()


def remove_algorithm_selection():
    # Function to remove the player selection elements
    if 'player_selection_frame' in globals():
        player_selection_frame.destroy()
        del globals()['player_selection_frame']

# Create a function to show the labels and comboboxes for player algorithms
def show_algorithm_selection():
    remove_algorithm_selection()
    global player_number
    player_number = int(player_number_entry.get())
    frame = ttk.Frame(root)
    frame.place(relx=0.5, rely=0.73, anchor="center")
    
    for i in range(1, player_number + 1):
        player_name = "Player" + str(i)
        algorithm_label = tk.Label(frame, text=f"{player_name} Algorithm:",font=("Helvetica", 15, "bold"))
        algorithm_label.grid(row=i , column=0, columnspan=1)
        algorithm_combobox = ttk.Combobox(frame, values=["RF_AutoAImodel", "OC_AutoAImodel", "NC_AutoAImodel"],font=("Helvetica", 15))
        algorithm_combobox.set("RF_AutoAImodel")
        algorithm_combobox.grid(row=i, column=1,columnspan=1)
        player_algorithms[player_name] = algorithm_combobox

    global player_selection_frame
    player_selection_frame = frame


root = tk.Tk()
root.title("Poker Game Interface")

# Set the window size to match the screen size
window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()
root.geometry(f"{window_width}x{window_height}")

# Load and resize the background image
bg_img = Image.open(r"image\bg.jpg")
bg_img = bg_img.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
bg_img = ImageTk.PhotoImage(bg_img)

# Create a Label to display the background image
bg_label = tk.Label(root, image=bg_img)
bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

# Define styles
style = ttk.Style()

# Configure button style with a new background color
style.configure("TButton", font=("Helvetica", 30, "bold"), background="#007ACC", foreground="black")

# Configure label style
style.configure("TLabel", font=("Helvetica", 20, "bold"))

# Configure combobox style
style.configure("TCombobox", font=("Helvetica", 40))

style.configure('TEntry', foreground = 'blue') 


# Create a frame to center-align elements
frame = ttk.Frame(root)
frame.place(relx=0.5, rely=0.6, anchor="center")

max_round_label = ttk.Label(frame, text="Max round :",width=20)
max_round_label.grid(row=0, column=0, sticky="e")
max_round_entry = ttk.Entry(frame)
max_round_entry.grid(row=0, column=1)

initial_stack_label = ttk.Label(frame, text="Initial stack:",width=20)
initial_stack_label.grid("",row=1, column=0, sticky="e")
initial_stack_entry = ttk.Entry(frame)
initial_stack_entry.grid(row=1, column=1)

small_blind_label = ttk.Label(frame, text="Small blind:",width=20)
small_blind_label.grid(row=2, column=0, sticky="e")
small_blind_entry = ttk.Entry(frame)
small_blind_entry.grid(row=2, column=1)

player_number_label = ttk.Label(frame, text="Player number:",width=20)
player_number_label.grid(row=3, column=0, sticky="e")
player_number_entry = ttk.Entry(frame)
player_number_entry.grid(row=3, column=1)

note_label = ttk.Label(frame, text="Note: player number should be 2 to 4 players",font=("Helvetica", 10, "bold"))
note_label.grid(row=4, columnspan=2)

show_button = ttk.Button(frame, text="Show Player Algorithms", command=show_algorithm_selection)
show_button.grid(row=5, columnspan=2, pady=(30, 0))

# Create a dictionary to store player algorithms
player_algorithms = {}

run_button = ttk.Button(frame, text="Run Poker Game", command=run_poker_game)
run_button.grid(row=7, columnspan=2, pady=(200, 0))

# Start the GUI main loop
root.mainloop()
