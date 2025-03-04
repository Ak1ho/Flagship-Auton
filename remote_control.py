# remote_control.py
from ibus import IBUSReceiver

class RemoteControl:
    """
    Reads from iBus (via a real UART).
    Provides a method to get mode, get movement, and get killswitch states.
    """
    def __init__(self,
                 uart_port='/dev/ttyAMA0',
                 baud=115200,
                 num_channels=6,
                 mode_channel=4,
                 x_channel=0,
                 y_channel=1,
                 rotate_channel=3,
                 killswitch_channel=5):
        self.ibus = IBUSReceiver(uart_port=uart_port, baud=baud, num_channels=num_channels)
        self.mode_channel = mode_channel
        self.x_channel = x_channel
        self.y_channel = y_channel
        self.rotate_channel = rotate_channel
        self.killswitch_channel = killswitch_channel

    def update(self):
        # Now we read from the serial buffer and parse iBus frames
        self.ibus.update()

    def get_mode(self):
        """
        For example, channel 4 above 1500 => auton
        """
        val = self.ibus.get_channel(self.mode_channel)
        return 1 if val > 1500 else 0

    def get_movement(self):
        x_val = self.ibus.get_channel(self.x_channel)
        y_val = self.ibus.get_channel(self.y_channel)
        r_val = self.ibus.get_channel(self.rotate_channel)

        def norm(v):
            return (v - 1500) / 500.0  # 1000..2000 -> -1..+1

        return norm(x_val), norm(y_val), norm(r_val)

    def get_killswitch(self):
        val = self.ibus.get_channel(self.killswitch_channel)
        return (val > 1500)

    def close(self):
        self.ibus.close()
