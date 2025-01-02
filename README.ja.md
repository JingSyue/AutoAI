<div align="center">

[英語](./README.en.md)\|[簡体字中国語](./README.zh-CN.md)\|[アラビア語](./README.ar.md)\|[フランス語](./README.fr.md)\|[日本語](./README.ja.md)

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

## 📁 ディレクトリ構造

### 🎮 ポーカーエンジン

-   関連プロジェクト
-   [Pyポーカーエンジン](https://github.com/ishikota/PyPokerEngine)

### 📊 テストチャート

-   3人プレイ
-   4人プレイ

### 📋結果

-   [demo video](https://youtu.be/sFaKtDhwvUw?feature=shared)

### 💾 ストアデータセット

-   **chart.py**
    -   ポジション 0 のプレーヤーは、このカテゴリを使用してチャートを保存および表示します。
    -   AutoAI.py からのテスト結果の保存
-   **data_set.py**
    -   (NC モデルのみゲーム データを保存する関数を呼び出します)
-   **NC_3_players_data_set.csv**
    -   3 プレイヤー ポーカー ゲームをプレイするために NC データを保存します
-   **NC_4_players_data_set.csv**
    -   4 プレイヤー ポーカー ゲームをプレイするための NC データを保存する

### 🤖 AIモデル

-   **NCモデル**: CNN AI模型 (3人、4人資料集個別訓練)
-   **NC2モデル**: CNN AI模型(3+4人混合訓練)
-   **OCモデル**: CNN で訓練された AI モデル
-   **RFモデル**:ランダムフォレストで訓練されたAIモデル

### 🎯 AutoAI.py

-   啟動遊戲介面的主程式
-   展示用

## ⚙️実行方法は？

1.  モジュールをrequirement.txtにインストールします。

```bash
pip install -r requirement.txt
```

(requirement.txt に一部のパッケージが不足している可能性があります。エラー メッセージから他の必要なパッケージをすべてインストールしてください)

2.  AutoAI アーカイブの場合**いいえ**Fにインストールされています:\\、次のパスを変更してください

### 次の Python ファイルのパスを変更します。

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

3.  AutoAI.pyをコンパイルして実行します
4.  ゲームの初期値を設定します (スモール ブラインドより大きい必要があります)
5.  「プレーヤーアルゴリズムを表示」ボタンをクリックします。
6.  希望のアルゴリズムを選択します
7.  「ポーカー ゲームを実行」ボタンをクリックします。

## ⚠️ 注意事項

-   🚫 同じゲーム内で同じ AI を選択しないでください
-   ⚠️プレイ人数は3～4人程度でお願いします
-   ⏳ ゲームの実行には時間がかかります。進行状況は VS Code ターミナルで確認できます。
