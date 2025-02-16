import time

class MotorController:
    def __init__(self,left_pins,right_pins,weapon_pin):
        self.left_pins=left_pins
        self.right_pins=right_pins
        self.weapon_pin=weapon_pin
    def set_speed(self,left,right):
        pass
    def spin_weapon(self,on=True):
        pass
    def stop(self):
        self.set_speed(0,0)
    def cleanup(self):
        self.stop()
