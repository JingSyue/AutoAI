<div align="center">

[Anglais](./README.en.md)\|[Chinois simplifié](./README.zh-CN.md)\|[arabe](./README.ar.md)\|[Français](./README.fr.md)\|[japonais](./README.ja.md)

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

## 📁 Structure du répertoire

### 🎮 PokerEngine

-   Projets associés
-   [Moteur PyPoker](https://github.com/ishikota/PyPokerEngine)

### 📊 carte de test

-   3 joueurs
-   4 joueurs

### 📋 résultat

-   [vidéo de démonstration](https://youtu.be/sFaKtDhwvUw?feature=shared)

### 💾 store_data_set

-   **chart.py**
    -   Le joueur en position 0 utilisera cette catégorie pour stocker et afficher des graphiques
    -   Stockage des résultats de test d'AutoAI.py
-   **data_set.py**
    -   (Seuls les modèles NC appelleront des fonctions pour stocker les données de jeu)
-   **NC_3_players_data_set.csv**
    -   Enregistrez les données NC pour jouer à des jeux de poker à 3 joueurs
-   **NC_4_players_data_set.csv**
    -   Stockez les données NC pour jouer à des jeux de poker à 4 joueurs

### 🤖 AI Models

-   **Modèle CN**: Modèle CNN AI (formation individuelle sur des ensembles de données de 3 et 4 personnes)
-   **Modèle NC2**: Modèle CNN AI (formation mixte 3+4 personnes)
-   **Modèle OC**: Modèle d'IA formé par CNN
-   **Modèle RF**:Modèle d'IA entraîné par une forêt aléatoire

### 🎯 AutoAI.py

-   Démarrez le programme principal de l'interface de jeu
-   pour l'affichage

## ⚙️ Comment exécuter ?

1.  Installez le module dans require.txt

```bash
pip install -r requirement.txt
```

(il peut manquer certains packages dans le fichier require.txt, veuillez installer tous les autres packages requis à partir du message d'erreur)

2.  Si l'archive AutoAI**Non**Installé en F :\\, veuillez modifier le chemin suivant

### Modifiez le chemin dans le fichier Python suivant

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

3.  Compilez et exécutez AutoAI.py
4.  Fixer la valeur initiale du jeu (doit être supérieure au small blind)
5.  Cliquez sur le bouton Afficher l'algorithme du joueur
6.  Sélectionnez l'algorithme souhaité
7.  Cliquez sur le bouton Exécuter une partie de poker

## ⚠️ Remarques

-   🚫 Ne choisissez pas la même IA dans le même jeu
-   ⚠️Le nombre de joueurs doit être de 3 à 4 personnes
-   ⏳ L'exécution du jeu prend un certain temps. Vous pouvez vérifier la progression dans le terminal VS Code.
