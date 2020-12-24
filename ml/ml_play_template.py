class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        elif self.player == "player5":
            self.player_no = 4
        elif self.player == "player6":
            self.player_no = 5
        else:
            pass
        self.r_sensor_value = 0
        self.l_sensor_value = 0
        self.f_sensor_value = 0
        self.control_list = [{"left_PWM" : 0, "right_PWM" : 0}]
        print("Initial ml script")

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

    def reset(self):
        """
        Reset the status
        """
        print("reset ml script")
        pass
