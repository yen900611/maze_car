# **Maze Car**

<img src="./asset/logo.svg" alt="logo" width="100"/>

![Maze_Car](https://img.shields.io/github/v/tag/yen900611/Maze_Car)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![MLGame](https://img.shields.io/badge/MLGame->9.5.3.*-<COLOR>.svg)](https://github.com/PAIA-Playful-AI-Arena/MLGame)
[![pygame](https://img.shields.io/badge/pygame-2.0.1-<COLOR>.svg)](https://github.com/pygame/pygame/releases/tag/2.0.1)

在錯綜復雜的棋盤迷宮中，如何讓你的自走車突破重圍，走到出口，而不會迷失在其之中。本遊戲也提供多元的關卡，隨著遊戲難度提升，迷宮的牆壁可是會移動，考驗各位玩家如何再多變的環境下，依然能夠逃出迷宮。

![](https://i.imgur.com/uDn6Foi.gif)

# 更新內容(3.3.1)
1. 更新程式碼內容，以運行於 MLGame 9.5.*以後版本
---
# 基礎介紹

## 啟動方式

- 直接啟動 [main.py](https://github.com/yen900611/Maze_Car/blob/master/main.py) 即可執行

### 遊戲參數設定

```python
# main.py

game = MazeCar.MazeCar(user_num=1, game_type="MAZE", map=4, time=200, sensor=3, sound=SOUND_OFF)`
```

- `user_num`：玩家數量，最多可以6個玩家同時進行同一場遊戲。
- `game_type`：自走車目前有三種遊戲模式：經典迷宮(`MAZE`)、移動迷宮(`MOVE_MAZE`)與小試身手(`PRACTICE`)。
- `map`：選擇要執行的地圖編號，不同的模式中，地圖不會共用編號。

- `time`：遊戲結束時間，單位為FPS，時間到會強制結束遊戲。
- `sensor`：感測器的數量，可以選擇3或5個。區別在於是否有右前方/左前方的感測器。

- `sound`：可輸入"on"或是"off"，控制是否播放遊戲音效。

## 玩法

- 使用鍵盤 上、下、左、右 (1P)與 Ｗ、Ａ、Ｓ、Ｄ (2P)控制自走車

## 目標

1. 在遊戲時間截止前到達迷宮的終點。

### 通關條件

1. 時間結束前，自走車碰到終點，即可過關。

### 失敗條件

1. 時間結束前，自走車尚未走到終點，即算失敗。

## 遊戲系統

1. 行動機制

    控制左右輪轉速，達到前進、後退、轉彎的目的。

    上鍵(W同)：左右輪固定輸出100

    下鍵(S同)：左右輪固定輸出-100

    左鍵(A同)：右輪輸出增加100

    右鍵(D同)：左輪輸出增加100

2. 感測器
    感測器測量的起點為自走車車身外圍，終點為直線距離上最靠的牆壁，實際距離如圖所示
    ![](https://i.imgur.com/QUmpOmz.png)


4. 物件大小
    使用Box2D的座標系統，單位為cm，每公分換算為4像素，
    ![](https://i.imgur.com/ghBEVyZ.png)


    - 自走車 12.5 x 10cm
    - 檢查點 15 x 15cm
    - 終點 15 x 15cm
4. 座標系統
    
    原點在迷宮區域的左上角，Ｘ軸向右為正，Y軸向上為正。
    ![](https://i.imgur.com/4dcUjgr.png)

---

# 進階說明

## 使用ＡＩ玩遊戲

```bash
python -m mlgame -i ml/ml_play_template.py ./ --map 1 --game_type MAZE --user_num 6 --time_to_play 450 --sensor_num 5 --sound off
```

## ＡＩ範例

```python
class MLPlay:
    def __init__(self, ai_name,*args,**kwargs):
        self.player_no = ai_name
        self.r_sensor_value = 0
        self.l_sensor_value = 0
        self.f_sensor_value = 0
        self.control_list = {"left_PWM" : 0, "right_PWM" : 0}
        # print("Initial ml script")
        print(kwargs)

    def update(self, scene_info: dict, *args, **kwargs):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"
        self.r_sensor_value = scene_info["R_sensor"]
        self.l_sensor_value = scene_info["L_sensor"]
        self.f_sensor_value = scene_info["F_sensor"]
        if self.f_sensor_value >15:
            self.control_list["left_PWM"] = 100
            self.control_list["right_PWM"] = 100
        else:
            self.control_list["left_PWM"] = 0
            self.control_list["right_PWM"] = 0
        return self.control_list

    def reset(self):
        """
        Reset the status
        """
        # print("reset ml script")
        pass

```

## 遊戲資訊

- `scene_info` 的資料格式如下

```json
{
    "frame": 16,
    "status": "GAME_ALIVE", 
    "x": 107.506, 
    "y": -112.5, 
    "angle": 0.0, 
    "R_sensor": 5.6, 
    "L_sensor": 4.7, 
    "F_sensor": 87.6, 
    "L_T_sensor": -1, 
    "R_T_sensor": -1, 
    "end_x": 12.5,
    "end_y": -12.5
}

```

* `frame`：遊戲畫面更新的編號
* `L_T_sensor`：玩家自己車子左前超聲波感測器的值，資料型態為數值，單位是公分。
* `R_T_sensor`：玩家自己車子右前超聲波感測器的值，資料型態為數值
* `L_sensor`：玩家自己車子左邊超聲波感測器的值，資料型態為數值
* `F_sensor`：玩家自己車子前面超聲波感測器的值，資料型態為數值
* `R_sensor`：玩家自己車子右邊超聲波感測器的值，資料型態為數值
* `x`：玩家自己車子的x座標，該座標系統原點位於迷宮左上角，x軸向右為正。
* `y`：玩家自己車子的y座標，該座標系統原點位於迷宮左上角，y軸向上為正。
* `end_x`：終點x座標，該座標系統原點位於迷宮左上角，x軸向右為正。
* `end_y`：終點y座標，該座標系統原點位於迷宮左上角，y軸向上為正。
* `angle`：玩家自己車子的朝向，車子向上為0度，數值逆時鐘遞增至360
* `status`： 目前遊戲的狀態
    - `GAME_ALIVE`：遊戲進行中
    - `GAME_PASS`：遊戲通關
    - `GAME_OVER`：遊戲結束

座標資訊請參考 `座標系統` 章節
## 動作指令

- 在 update() 最後要回傳一個字典，資料型態如下。
    ```python
    {
            'left_PWM': 0,
            'right_PWM': 0
    }
    ```
    其中`left_PWM`與`right_PWM`分別代表左輪與右輪的馬力，接受範圍為-255~255。


## 遊戲結果

- 最後結果會顯示在console介面中，若是PAIA伺服器上執行，會回傳下列資訊到平台上。

```json
{
    "frame_used": 121, 
    "state": "FINISH", 
    "attachment": [
        {
        "player": "2P", 
        "rank": 1, 
        "used_frame": 107, 
        "check_points": 0
        }, 
        {
        "player": "1P", 
        "rank": 2, 
        "used_frame": 121, 
        "check_points": 0
        }
    ]
}

```

- `frame_used`：表示遊戲使用了多少個frame
- `state`：表示遊戲結束的狀態
    - `FAIL`：遊戲失敗
    - `FINISH`：遊戲完成
- `attachment`：紀錄遊戲各個玩家的結果與分數等資訊
    - `player`：玩家編號
    - `rank`：排名
    - `used_frame`：個別玩家到達終點使用的frame數
    - `frame_limit`：該局遊戲所設定的時間上限
    - `frame_percent`：
        ![](https://i.imgur.com/QuI8HmM.png)
    - `total_checkpoints`：該地圖的總檢查點數量
    - `check_points`：玩家通過的檢查點數量
    - `remain_points`：玩家未通過的檢查點數量
    - `pass_percent`：
        ![](https://i.imgur.com/QuMt5Lu.png)

    - `remain_percent`：
        ![](https://i.imgur.com/mym3FVm.png)
---
# 地圖製作說明
[地圖製作教學](map_editor.md)


![](https://i.imgur.com/ubPC8Fp.jpg)
---
