<div align="center">
[English](./README.en.md) | [简体中文](./README.zh-CN.md) | [العربية](./README.ar.md) | [Français](./README.fr.md) | [日本語](./README.ja.md)
</div>
<div align="center">
  <h1>AutoAI</h1>
  <a href='#-目錄結構'>
    <img src="./image/ui.png" alt="icon" style="margin: 20px 0;"/>
  </a>
  <p>自動化AI德州撲克牌局</p>
  <p>
    <a href="https://youtu.be/sFaKtDhwvUw?feature=shared">演示 Demo</a> / 
  </p>
</div>

## 📁 目錄結構
### 🎮 PokerEngine
- 相關專案
- [PyPokerEngine](https://github.com/ishikota/PyPokerEngine)

### 📊 testchart
- 3players
- 4players

### 📋 result
- [demo video](https://youtu.be/sFaKtDhwvUw?feature=shared)

### 💾 store_data_set
- **chart.py**
  - 位置0的玩家將使用此類別來儲存與顯示圖表
  - 儲存來自AutoAI.py的測試結果
- **data_set.py**
  - (僅NC模型會呼叫函數來儲存遊戲資料)
- **NC_3_players_data_set.csv**
  - 儲存NC玩3人撲克遊戲的資料
- **NC_4_players_data_set.csv**
  - 儲存NC玩4人撲克遊戲的資料

### 🤖 AI Models
- **NCmodel**: CNN AI模型 (3人、4人資料集個別訓練)
- **NC2model**: CNN AI模型(3+4人混合訓練)
- **OCmodel**: CNN 訓練的AI模型
- **RFmodel**:隨機森林訓練的AI模型

### 🎯 AutoAI.py
- 啟動遊戲介面的主程式
- 用於展示

## ⚙️ 如何執行?

1. 安裝requirement.txt中的模組
```bash
pip install -r requirement.txt
```
(requirement.txt可能缺少某些套件，請從錯誤訊息安裝所有其他需要的套件)

2. 如果AutoAI檔案**不是**安裝在F:\\，請修改以下路徑

### 在以下Python檔案中修改路徑

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

3. 編譯並執行AutoAI.py
4. 設定遊戲初始值(應大於小盲注)
5. 點擊Show Player Algorithm按鈕
6. 選擇想要的演算法
7. 點擊Run Poker Game按鈕

## ⚠️ 注意事項
- 🚫 不要在同一場遊戲中選擇相同的AI
- ⚠️ 玩家人數應為3-4人
- ⏳ 執行遊戲需要一些時間，可以在VS Code終端機中查看進度