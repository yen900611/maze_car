class MLPlay:
    def __init__(self, ai_name,*args,**kwargs):
        self.player_no = ai_name
        self.r_sensor_value = 0
        self.l_sensor_value = 0
        self.f_sensor_value = 0
        self.control_list = {"left_PWM" : 0, "right_PWM" : 0}
        # print("Initial ml script")

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
