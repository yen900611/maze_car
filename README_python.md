# 遊戲專案
[Github Maze_Car](https://github.com/yen900611/Maze_Car)

## 執行方式
* 直接執行 預設是單人遊戲
`python main.py`
    * 車子前進、後退、左轉、右轉：1P - `UP`、`DOWN`、`LEFT`、`RIGHT`，2P - `W`、`S`、`A`、`D`
    

## 運行於MLGame之下
* 搭配[MLGame](https://github.com/LanKuDot/MLGame)執行，請將遊戲放在MLGame/games資料夾中，遊戲資料夾需命名為**Maze_Car**
    * 手動模式：
`python MLGame.py -m Maze_Car <the number of user> [game_mode] <map> [sound]`
    * 機器學習模式：
`python MLGame.py -i ml_play_template.py Maze_Car <the number of user> [game_mode] <map> [sound]`

### 遊戲參數

* `the number of user`：指定遊戲玩家人數，最少需一名玩家。單機手動模式最多兩名(鍵盤位置不足)，機器學習模式至多六名。
* `game_mode`：遊戲模式，目前只有迷宮模式，預設為"MAZE"。
* `map`：選擇不同的迷宮，目前提供2種迷宮地圖，並且會隨時增加，迷宮編號從1開始，預設為1號地圖。
* `time`：控制遊戲時間，單位為秒，時間到了之後即使有玩家還沒走出迷宮，遊戲仍然會結束。
* `sound`：音效設定，可選擇"on"或"off"，預設為"off"



### 撰寫玩遊戲的程式

程式範例在 [`ml/ml_play_template.py`](https://github.com/yen900611/RacingCar/blob/master/ml/ml_play_template.py)。


### 初始化參數
```python=2
def __init__(self, player):
    self.r_sensor_value = 0
    self.l_sensor_value = 0
    self.f_sensor_value = 0
    self.control_list = [{"left_PWM" : 0, "right_PWM" : 0}]
```
`"player"`: 字串。其值只會是 `"player1"` 、 `"player2"` 、 `"player3"` 、 `"player4"` 、`"player5"` 、 `"player6"` ，代表這個程式被哪一台車使用。


### 遊戲場景資訊

由遊戲端發送的字典物件，同時也是存到紀錄檔的物件。
```python=17
   def update(self, scene_info: dict):
        """
        Generate the command according to the received scene information
        """
        self.r_sensor_value = scene_info["R_sensor"]
        self.l_sensor_value = scene_info["L_sensor"]
        self.f_sensor_value = scene_info["F_sensor"]
        self.control_list[0]["left_PWM"] += 50
        self.control_list[0]["right_PWM"] += 50

        return self.control_list

```
以下是該字典物件的鍵值對應：

* `"frame"`：整數。紀錄的是第幾影格的場景資訊
* `status`：遊戲狀態
* `"L_sensor"`：玩家自己車子左邊超聲波感測器的值，資料型態為數值
* `"F_sensor"`：玩家自己車子前面超聲波感測器的值，資料型態為數值
* `"R_sensor"`：玩家自己車子右邊超聲波感測器的值，資料型態為數值

### 遊戲指令

傳給遊戲端用來控制自走車的指令。

玩家透過字典`{"left_PWM" : 0, "right_PWM" : 0}`回傳左右輪的馬力，範圍為-255~255，並將此字典放入清單中回傳。
例如：`[{"left_PWM" : 0, "right_PWM" : 0}]`

### 機器學習模式的玩家程式

自走車可以多人遊戲，所以在啟動機器學習模式時，需要利用 `-i <script_for_1P> -i <script_for_2P> -i <script_for_3P> -i <script_for_4P>` 指定最多六個不同的玩家程式。
* For example
`python MLGame.py -f 120 -i ml_play_template.py -i ml_play_template.py Maze_Car 2 MAZE 1 off`


![](https://i.imgur.com/ubPC8Fp.jpg)