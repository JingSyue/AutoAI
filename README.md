# AutoAI 
## Directoies/Files usage
### back_up_AutoAI_model
- used for backup only, please execute in other files
### PokerEngine
- game logic 
### Automodel_format documents
- documents
### image
- background image for interface
### NCmodel
- 112th trained AI model 
### OCmodel 
- 111th trained AI model
### RFmodel
- 110th trained AI model
### AutoAI.py
- program to start the game

## How to run it?
1. pip install modules in the requirement.txt
(requirement.txt may lack some packages. Install all the other packages from the error message)
2. change the path if AutoAI file is not installed in F:\\
    ### Change paths to  in the following python files 
    #### NC_AutoAImodel.py
    ```python
        def predict(self):
        with open('F:\\AutoAI\\NCmodel\\model.config', 'r') as json_file: #path
            json_string = json_file.read()
        model = Sequential()
        model = model_from_json(json_string)
        model.load_weights('F:\\AutoAI\\NCmodel\\model.weight', by_name=False) #path
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

4. set the game initial value

5. press Show Player Algorithm button

6. select the Algorithm U want

7. press Run Poker Game button 

(It will take some time to run the game, U can see the process in the vs code terminal.)
(Most bugs can be fixed by restarting Auto.py)
Note:Due to the AI model settings NC_model can only play 3 or 4 players poker games.
For example, NC+RF+OC can run. But NC+RF can't.


## Some issues might occur in vs code when starting the game
### Error message:
Connection to server got closed. Server will not be restarted.
2023-11-03 14:52:51.405 [info] [Info  - 下午2:52:51] (21832) Pylance language server 2023.11.10 (pyright 088ebaa5) starting
2023-11-03 14:52:51.406 [info] [Info  - 下午2:52:51] (21832) Server root directory: C:\Users\User\.vscode\extensions\ms-python.vscode-pylance-2023.11.10\dist
2023-11-03 14:52:51.419 [info] [Info  - 下午2:52:51] (21832) Starting service instance "<default>"
2023-11-03 14:52:51.430 [info] [Error - 下午2:52:51] (21832) Error reading settings: Error: Request workspace/configuration failed with message: Not allowed to resolve environment in an untrusted workspace
2023-11-03 14:52:51.481 [info] [Info  - 下午2:52:51] (21832) No source files found.
2023-11-03 14:52:51.539 [info] [Error - 下午2:52:51] (21832) Error reading settings: Error: Request workspace/configuration failed with message: Not allowed to resolve environment in an untrusted workspace
2023-11-03 14:52:51.574 [info] [Info  - 下午2:52:51] (21832) No source files found.
2023-11-03 14:52:54.798 [info] [Error - 下午2:52:54] Server process exited with code 1.
2023-11-03 14:52:54.798 [info] [Error - 下午2:52:54] Connection to server got closed. Server will not be restarted.
2023-11-03 14:52:54.799 [info] [Error - 下午2:52:54] Handling connection close failed
2023-11-03 14:52:54.799 [info] TypeError: e.clear is not a function
	at _.cleanUp (c:\Users\User\.vscode\extensions\ms-python.python-2023.20.0\out\client\extension.js:2:2412859)
	at _.handleConnectionClosed (c:\Users\User\.vscode\extensions\ms-python.python-2023.20.0\out\client\extension.js:2:2417283)
	at _.handleConnectionClosed (c:\Users\User\.vscode\extensions\ms-python.python-2023.20.0\out\client\extension.js:2:2578252)
	at c:\Users\User\.vscode\extensions\ms-python.python-2023.20.0\out\client\extension.js:2:2416709
	at o.invoke (c:\Users\User\.vscode\extensions\ms-python.python-2023.20.0\out\client\extension.js:2:2363387)
	at s.fire (c:\Users\User\.vscode\extensions\ms-python.python-2023.20.0\out\client\extension.js:2:2364152)
	at te (c:\Users\User\.vscode\extensions\ms-python.python-2023.20.0\out\client\extension.js:2:2349784)
	at o.invoke (c:\Users\User\.vscode\extensions\ms-python.python-2023.20.0\out\client\extension.js:2:2363387)
	at s.fire (c:\Users\User\.vscode\extensions\ms-python.python-2023.20.0\out\client\extension.js:2:2364152)
	at d.fireClose (c:\Users\User\.vscode\extensions\ms-python.python-2023.20.0\out\client\extension.js:2:2372012)
	at ChildProcess.<anonymous> (c:\Users\User\.vscode\extensions\ms-python.python-2023.20.0\out\client\extension.js:2:2384364)
	at ChildProcess.emit (node:events:525:35)
	at maybeClose (node:internal/child_process:1091:16)
	at ChildProcess._handle.onexit (node:internal/child_process:302:5)

### How to solve it?
1. Go to VS Code's settings by clicking on the gear icon in the bottom left corner and selecting "Settings."
2. Search for "Trust" in the settings search bar.
Check your "Security: Workspace Trust" settings and ensure that it's set to "Trusted."
If it's set to "Restricted," you might need to change it to "Trusted."
3. Add the file path in the trusted workspace in vs code setting
see more info on 
# https://learn.microsoft.com/zh-tw/visualstudio/ide/reference/trust-settings?view=vs-2022
