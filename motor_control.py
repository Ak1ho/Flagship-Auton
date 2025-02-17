from gpiozero import PWMOutputDevice
import time

class MotorController:
    def __init__(
        self,
        left_forward_pin=17,
        left_backward_pin=18,
        right_forward_pin=22,
        right_backward_pin=23,
        spinner_pin=24,
        pwm_frequency=1000
    ):
        self.left_forward = PWMOutputDevice(left_forward_pin, frequency=pwm_frequency)
        self.left_backward = PWMOutputDevice(left_backward_pin, frequency=pwm_frequency)
        self.right_forward = PWMOutputDevice(right_forward_pin, frequency=pwm_frequency)
        self.right_backward = PWMOutputDevice(right_backward_pin, frequency=pwm_frequency)

        # Vertical spinner motor
        self.spinner = PWMOutputDevice(spinner_pin, frequency=pwm_frequency)

        # A quick safety stop
        self.stop_all()

    def stop_all(self):
        self.left_forward.value = 0
        self.left_backward.value = 0
        self.right_forward.value = 0
        self.right_backward.value = 0
        self.spinner.value = 0

    def drive_forward(self, speed=1.0):
        self.left_forward.value = speed
        self.left_backward.value = 0
        self.right_forward.value = speed
        self.right_backward.value = 0

    def drive_backward(self, speed=1.0):
        self.left_forward.value = 0
        self.left_backward.value = speed
        self.right_forward.value = 0
        self.right_backward.value = speed

    def turn_left(self, speed=1.0):
        self.left_forward.value = 0
        self.left_backward.value = speed
        self.right_forward.value = speed
        self.right_backward.value = 0

    def turn_right(self, speed=1.0):
        self.left_forward.value = speed
        self.left_backward.value = 0
        self.right_forward.value = 0
        self.right_backward.value = speed

    def spin_up(self, speed=1.0):
        self.spinner.value = speed

    def spin_down(self):
        self.spinner.value = 0

    def stop_drivetrain(self):
        self.left_forward.value = 0
        self.left_backward.value = 0
        self.right_forward.value = 0
        self.right_backward.value = 0
