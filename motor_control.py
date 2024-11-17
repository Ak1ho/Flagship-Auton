# motor_control.py
import RPi.GPIO as GPIO
import time

class MotorControl:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        # Define GPIO pins for ESCs
        self.ESC_PINS = {
            'wheel_1': 17, #these are test pins
            'wheel_2': 18,
            'wheel_3': 27,
            'wheel_4': 22,
            'weapon': 23
        }

        # Setup GPIO pins
        for pin in self.ESC_PINS.values():
            GPIO.setup(pin, GPIO.OUT)

        # Initialize PWM signals
        self.pwms = {}
        for name, pin in self.ESC_PINS.items():
            pwm = GPIO.PWM(pin, 50)  # 50 Hz
            pwm.start(7.5)  # Neutral signal for ESCs
            self.pwms[name] = pwm

    def set_speed(self, name, speed):
        # Convert speed (-100 to 100) to duty cycle
        duty_cycle = self.speed_to_duty_cycle(speed)
        self.pwms[name].ChangeDutyCycle(duty_cycle)

    def speed_to_duty_cycle(self, speed):
        # Map speed (-100 to 100) to duty cycle (5% to 10%)
        # Neutral (stop) is at 7.5%
        return 7.5 + (speed / 100) * 2.5

    def move_towards(self, direction):
        # Implement movement logic based on direction
        # For simplicity, we'll move forward
        speed = 50  # Adjust speed as needed
        self.set_speed('wheel_1', speed)
        self.set_speed('wheel_2', speed)
        self.set_speed('wheel_3', speed)
        self.set_speed('wheel_4', speed)

    def search_pattern(self):
        # Rotate in place to search for the robot
        speed = 30
        self.set_speed('wheel_1', speed)
        self.set_speed('wheel_2', -speed)
        self.set_speed('wheel_3', speed)
        self.set_speed('wheel_4', -speed)

    def set_wheel_speeds(self, speeds):
        # Speeds is a dictionary with keys 'wheel_1', 'wheel_2', etc.
        for wheel, speed in speeds.items():
            self.set_speed(wheel, speed)

    def set_weapon_speed(self, speed):
        self.set_speed('weapon', speed)

    def activate_weapon(self, speed):
        self.set_speed('weapon', speed)

    def stop_motors(self):
        for pwm in self.pwms.values():
            pwm.ChangeDutyCycle(7.5)  # Neutral signal

    def cleanup(self):
        self.stop_motors()
        GPIO.cleanup()
