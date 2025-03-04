# motor_control.py
import RPi.GPIO as GPIO
import time

class MotorController:
    """
    Controls:
      - Four motors in an X-drive configuration
      - A spinner (weapon) ESC
    Using RPi.GPIO software PWM at a chosen frequency.

    DISCLAIMER: 
    - If your driver requires forward/reverse signals, you'll need
      separate direction pins or a specialized ESC that interprets
      a servo-style signal. This code only sets a single PWM duty cycle
      (0-100%) per pin, clamping negative speeds to 0.
    """

    def __init__(self, motor_pins, spinner_pin, pwm_freq=1000):
        """
        :param motor_pins: list of 4 GPIO pins for the drive motors
        :param spinner_pin: pin for the weapon spinner
        :param pwm_freq: PWM frequency in Hz
        """
        GPIO.setmode(GPIO.BCM)

        self.motor_pins = motor_pins
        self.spinner_pin = spinner_pin
        self.pwm_freq = pwm_freq

        # Motor PWM
        self.motor_pwm = []
        for pin in self.motor_pins:
            GPIO.setup(pin, GPIO.OUT)
            pwm_obj = GPIO.PWM(pin, self.pwm_freq)
            pwm_obj.start(0)  # 0% duty initially
            self.motor_pwm.append(pwm_obj)

        # Spinner PWM
        GPIO.setup(self.spinner_pin, GPIO.OUT)
        self.spinner_pwm = GPIO.PWM(self.spinner_pin, self.pwm_freq)
        self.spinner_pwm.start(0)

    def set_motor_speed(self, index, speed):
        """
        speed in [-1..+1]. Negative is clamped to 0 if your driver can't reverse.
        We'll map [-1..+1] to [0..100%] duty cycle.
        """
        if 0 <= index < len(self.motor_pwm):
            duty = (speed + 1.0) / 2.0 * 100.0  # -1->0, 0->50, +1->100
            if duty < 0:
                duty = 0
            if duty > 100:
                duty = 100
            self.motor_pwm[index].ChangeDutyCycle(duty)

    def start_spinner(self):
        """
        Run the spinner at 100% duty. If your ESC interprets this as max throttle,
        it will spin continuously.
        """
        self.spinner_pwm.ChangeDutyCycle(100)

    def stop_spinner(self):
        """
        Set spinner to 0% duty, effectively stopping or disarming it.
        """
        self.spinner_pwm.ChangeDutyCycle(0)

    def xdrive_move(self, x, y, rotate):
        """
        For X-drive (4 wheels at 45 deg):
            m0 =  y + x + rotate
            m1 =  y - x - rotate
            m2 = -y + x - rotate
            m3 = -y - x + rotate
        Then clamp each to [-1..+1].
        """
        m0 =  y + x + rotate
        m1 =  y - x - rotate
        m2 = -y + x - rotate
        m3 = -y - x + rotate

        max_val = max(abs(m0), abs(m1), abs(m2), abs(m3))
        if max_val > 1.0:
            m0 /= max_val
            m1 /= max_val
            m2 /= max_val
            m3 /= max_val

        self.set_motor_speed(0, m0)
        self.set_motor_speed(1, m1)
        self.set_motor_speed(2, m2)
        self.set_motor_speed(3, m3)

    def search_spin(self):
        """
        If no target is found in auton mode, we can rotate in place slowly.
        """
        self.xdrive_move(0, 0, 0.3)

    def stop_all(self):
        """
        Zero duty on all drive motors.
        """
        for pwm_obj in self.motor_pwm:
            pwm_obj.ChangeDutyCycle(0)

    def shutdown(self):
        """
        Stop everything and clean up GPIO resources.
        """
        self.stop_all()
        self.stop_spinner()
        for pwm_obj in self.motor_pwm:
            pwm_obj.stop()
        self.spinner_pwm.stop()
        GPIO.cleanup()
