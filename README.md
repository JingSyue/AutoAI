# AutoAI 
## Directoies/Files usage
### PokerEngine
- poker game engine
- engine from https://github.com/ishikota/PyPokerEngine
### Automodel_format documents
- documents
### testchart
3players
4players
### result
demo video
final report

chart.py
- the player in the game whose position is 0 will use the class to store the chart and show it
- store test result from AutoAI.py
### store_data_set
- data_set.py
(only NC model will call the function to store game_data)
-NC_3_players_data_set.csv
store data from NC playing 3-player poker game
-NC_4_players_data_set.csv
store data from NC playing 4-player poker game
### image
- background image for interface
### NCmodel
- 113th trained AI model (3)(4)
### NC2model
- 113th trained AI model (3+4)
### OCmodel 
- 112th trained AI model
### RFmodel
- 111th trained AI model
### AutoAI.py
- program to start the game with interface
used for demo

## How to run it?
1. pip install modules in the requirement.txt
```pip install -r requirement.txt```
(requirement.txt may lack some packages. Install all the other packages from the error message)
2. change the path if AutoAI file is NOT installed in F:\\
    ### Change paths to  in the following python files 
    #### NC_AutoAImodel.py
    ```python
        def predict(self):
            if self.get_players()==3:
                with open('F:\\AutoAI\\NCmodel\\model-3p\\model3.config', 'r') as json_file: #path
                    json_string = json_file.read()
                model = Sequential()
                model = model_from_json(json_string)
                model.load_weights('F:\\AutoAI\\NCmodel\\model-3p\\model3.weight', by_name=False) #path
            elif self.get_players()==4:
                with open('F:\\AutoAI\\NCmodel\\model-4p\\model4.config', 'r') as json_file: #path
                    json_string = json_file.read()
                model = Sequential()
                model = model_from_json(json_string)
                model.load_weights('F:\\AutoAI\\NCmodel\\model-4p\\model4.weight', by_name=False) #path
    ```
     #### NC2_AutoAImodel.py
    ```python
        def predict(self):
            with open('F:\\AutoAI\\NCmodel\\model-3+4p\\model3+4.config', 'r') as json_file: #path
                    json_string = json_file.read()
            model = Sequential()
            model = model_from_json(json_string)
            model.load_weights('F:\\AutoAI\\NCmodel\\model-3+4p\\model3+4.weight', by_name=False) #path
    ```
    #### OC_AutiAImodel.py
    ```python
        def predict(self):
            with open('F:\\AutoAI\\OCmodel\\model.config', 'r') as text_file: #path
                json_string = text_file.read()
            model = Sequential()
            model = model_from_json(json_string)
            model.load_weights('F:\\AutoAI\\OCmodel\\model.weight', by_name=False) #path
    ```
    #### RF_AutoAImodel.py
    ```python
        def predict(self):
            model = joblib.load(r"F:\AutoAI\RFmodel\my_random_forest.joblib")#path
    ```
3. complile and run AutoAI.py

4. set the game initial value (it should be bigger than small bet)

5. press Show Player Algorithm button

6. select the Algorithm U want

7. press Run Poker Game button 

(It will take some time to run the game, U can see the process in the vs code terminal.)
(Most bugs can be fixed by restarting Auto.py)

Note:
1. DO NOT CHOOSE THE SAME AIs IN ONE GAME.
2. Player number should be 3~4 players.
