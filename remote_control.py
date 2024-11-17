# remote_control.py
import pigpio
class RemoteControl:
    def __init__(self):
        self.pi = pigpio.pi()
        if not self.pi.connected:
            print("Error: Could not connect to pigpio daemon")
            exit()

        self.CHANNEL_PINS = {
            'throttle': 5,  # Adjust GPIO pins as needed
            'steering': 6,
            'weapon': 13
        }

        self.pulse_widths = {
            'throttle': 1500,
            'steering': 1500,
            'weapon': 1500
        }

        for channel, pin in self.CHANNEL_PINS.items():
            self.pi.set_mode(pin, pigpio.INPUT)
            self.pi.set_pull_up_down(pin, pigpio.PUD_DOWN)
            self.pi.callback(pin, pigpio.EITHER_EDGE, self._pulse_callback_factory(channel))

    def _pulse_callback_factory(self, channel):
        def _pulse_callback(gpio, level, tick):
            if level == 1:
                self._last_tick[channel] = tick
            else:
                pulse_width = pigpio.tickDiff(self._last_tick[channel], tick)
                if 1000 < pulse_width < 2000:
                    self.pulse_widths[channel] = pulse_width
        return _pulse_callback

    def update_controls(self):
        pass

    def get_motor_speeds(self):
        # Convert pulse widths to speed values (-100 to 100)
        throttle = self._map_pulse_to_speed(self.pulse_widths['throttle'])
        steering = self._map_pulse_to_speed(self.pulse_widths['steering'])

        # Calculate wheel speeds based on throttle and steering
        left_speed = throttle + steering
        right_speed = throttle - steering

        # Limit speeds to -100 to 100
        left_speed = max(min(left_speed, 100), -100)
        right_speed = max(min(right_speed, 100), -100)

        speeds = {
            'wheel_1': left_speed,
            'wheel_2': right_speed,
            'wheel_3': left_speed,
            'wheel_4': right_speed
        }
        return speeds

    def get_weapon_speed(self):
        # Convert pulse width to speed (0 to 100)
        weapon_speed = self._map_pulse_to_speed(self.pulse_widths['weapon'], center=1500, deadzone=50)
        weapon_speed = max(min(weapon_speed, 100), 0)
        return weapon_speed

    def _map_pulse_to_speed(self, pulse_width, center=1500, deadzone=50):
        # Map pulse width (1000-2000 us) to speed (-100 to 100)
        if abs(pulse_width - center) < deadzone:
            return 0
        elif pulse_width > center:
            return ((pulse_width - center - deadzone) / (500 - deadzone)) * 100
        else:
            return ((pulse_width - center + deadzone) / (500 - deadzone)) * 100

    def cleanup(self):
        self.pi.stop()
