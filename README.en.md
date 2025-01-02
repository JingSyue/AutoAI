<div align="center">

[English](./README.en.md)\|[简体中文](./README.zh-CN.md)\|[Arabic](./README.ar.md)\|[French](./README.fr.md)\|[Japanese](./README.ja.md)

</div>
<div align="center">
  <h1>AutoAI</h1>
  <a href='#-目錄結構'>
    <img src="./image/ui.png" alt="icon" style="margin: 20px 0;"/>
  </a>
  <p>自動化AI德州撲克牌局</p>
  <p>
    <a href="https://youtu.be/sFaKtDhwvUw?feature=shared">演示 Demo</a> 
  </p>
</div>

## 📁 Directory structure

### 🎮 PokerEngine

-   Related projects
-   [PyPokerEngine](https://github.com/ishikota/PyPokerEngine)

### 📊 testchart

-   3players
-   4players

### 📋 result

-   [demo video](https://youtu.be/sFaKtDhwvUw?feature=shared)

### 💾 store_data_set

-   **chart.py**
    -   The player in position 0 will use this category to store and display charts
    -   Storing test results from AutoAI.py
-   **data_set.py**
    -   (Only NC models will call functions to store game data)
-   **NC_3_players_data_set.csv**
    -   Save NC data for playing 3-player poker games
-   **NC_4_players_data_set.csv**
    -   Store NC data for playing 4-player poker games

### 🤖 AI Models

-   **NCmodel**: CNN AI model (individual training on 3-person and 4-person data sets)
-   **NC2model**: CNN AI model (3+4 people mixed training)
-   **OCmodel**: CNN trained AI model
-   **RFmodel**:AI model trained by random forest

### 🎯 AutoAI.py

-   Start the main program of the game interface
-   for display

## ⚙️ How to execute?

1.  Install the module in requirement.txt

```bash
pip install -r requirement.txt
```

(requirement.txt可能缺少某些套件，請從錯誤訊息安裝所有其他需要的套件)

2.  If AutoAI archive**no**Installed in F:\\, please modify the following path

### Modify the path in the following Python file

#### NC_AutoAImodel.py

```python
def predict(self):
    if self.get_players()==3:
        with open('F:\\AutoAI\\NCmodel\\model-3p\\model3.config', 'r') as json_file: #路徑
            json_string = json_file.read()
        model = Sequential()
        model = model_from_json(json_string)
        model.load_weights('F:\\AutoAI\\NCmodel\\model-3p\\model3.weight', by_name=False) #路徑
    elif self.get_players()==4:
        with open('F:\\AutoAI\\NCmodel\\model-4p\\model4.config', 'r') as json_file: #路徑
            json_string = json_file.read()
        model = Sequential()
        model = model_from_json(json_string)
        model.load_weights('F:\\AutoAI\\NCmodel\\model-4p\\model4.weight', by_name=False) #路徑
```

#### NC2_AutoAImodel.py

```python
def predict(self):
    with open('F:\\AutoAI\\NCmodel\\model-3+4p\\model3+4.config', 'r') as json_file: #路徑
            json_string = json_file.read()
    model = Sequential()
    model = model_from_json(json_string)
    model.load_weights('F:\\AutoAI\\NCmodel\\model-3+4p\\model3+4.weight', by_name=False) #路徑
```

#### OC_AutoAImodel.py

```python
def predict(self):
    with open('F:\\AutoAI\\OCmodel\\model.config', 'r') as text_file: #路徑
        json_string = text_file.read()
    model = Sequential()
    model = model_from_json(json_string)
    model.load_weights('F:\\AutoAI\\OCmodel\\model.weight', by_name=False) #路徑
```

#### RF_AutoAImodel.py

```python
def predict(self):
    model = joblib.load(r"F:\AutoAI\RFmodel\my_random_forest.joblib") #路徑
```

3.  Compile and execute AutoAI.py
4.  Set the initial value of the game (should be greater than the small blind)
5.  Click the Show Player Algorithm button
6.  Select the desired algorithm
7.  Click the Run Poker Game button

## ⚠️ Notes

-   🚫 Don’t choose the same AI in the same game
-   ⚠️The number of players should be 3-4 people
-   ⏳ It takes some time to execute the game. You can check the progress in the VS Code terminal.
