import serial
import time
import struct

class IBUSReceiver:
    """
    A more realistic FlySky iBus decoder for a UART on the Raspberry Pi.
    This example:
      - Opens /dev/ttyAMA0 at 115200 baud.
      - Continuously reads data and parses iBus frames (32 bytes).
      - Decodes up to 14 channels, though we only store e.g. 6 or more if needed.
    NOTE:
      1) You must enable the Pi’s hardware UART (disable serial console, enable serial port).
      2) Connect the FlySky iBus signal line to the Pi's Rx pin (e.g. GPIO14 on older models).
         On the Pi 5, confirm which pins map to /dev/ttyAMA0 or /dev/ttyAMA2, etc.
      3) This is a minimal example. Adjust or expand for reliability (e.g. ring buffer approach).
    """

    IBUS_FRAME_SIZE = 32  # Each iBus frame is 32 bytes total
    IBUS_HEADER = b'\x20\x40'  # Typical iBus packet header

    def __init__(self, uart_port='/dev/ttyAMA0', baud=115200, num_channels=6):
        self.num_channels = num_channels
        # Store channel values in microseconds 1000..2000
        self.channels = [1500]*num_channels

        # Open the serial port
        self.ser = serial.Serial(
            port=uart_port,
            baudrate=baud,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_1,
            bytesize=serial.EIGHTBITS,
            timeout=0.02
        )
        if not self.ser.is_open:
            raise IOError(f"Failed to open serial port {uart_port}")

        # A small buffer to accumulate data read
        self.buffer = bytearray()

    def update(self):
        """
        Poll serial for new data, parse any complete iBus frames.
        Store the last valid frame's channel values in self.channels.
        Call this frequently from your main loop (e.g. ~50+ times per second).
        """
        # Read whatever is available
        data_in = self.ser.read(self.ser.in_waiting or 1)
        if data_in:
            self.buffer.extend(data_in)

        # Try to find and parse complete 32-byte frames in the buffer
        while len(self.buffer) >= self.IBUS_FRAME_SIZE:
            # Look for the iBus header at the start
            if self.buffer[0:2] == self.IBUS_HEADER:
                # If we have at least 32 bytes, attempt to parse one frame
                frame = self.buffer[:self.IBUS_FRAME_SIZE]
                if self._check_checksum(frame):
                    self._decode_frame(frame)
                # Remove the first 32 bytes (parsed frame) from buffer
                del self.buffer[:self.IBUS_FRAME_SIZE]
            else:
                # If no header, pop one byte and keep searching
                self.buffer.pop(0)

    def _check_checksum(self, frame):
        """
        iBus frames end with a 2-byte checksum = sum(all prior bytes) & 0xFFFF.
        This function verifies that.
        """
        # sum of the first 30 bytes
        chksum = sum(frame[0:30]) & 0xFFFF
        # low byte, high byte
        frame_sum = frame[30] | (frame[31] << 8)
        return (chksum == frame_sum)

    def _decode_frame(self, frame):
        """
        Parse the channel data (14 channels x 2 bytes each = 28 bytes) from positions 2..29,
        but we only store up to self.num_channels.
        """
        # The first 2 bytes are header (0x20 0x40), next 28 bytes are channel data, last 2 are checksum
        # Channels are little-endian 16-bit. Each channel is 2 bytes.
        # Example: channel 0 is frame[2..4], channel 1 is frame[4..6], etc.
        for ch_index in range(min(self.num_channels, 14)):
            # Each channel: 2 bytes, little-endian
            low = frame[2 + ch_index*2]
            high = frame[3 + ch_index*2]
            value = (high << 8) | low
            # Typically iBus channel value is ~1000..2000
            self.channels[ch_index] = value

    def get_channel(self, ch_index):
        """
        Return the channel value in the range [1000..2000], or a default 1500 if out of range.
        """
        if 0 <= ch_index < self.num_channels:
            return self.channels[ch_index]
        return 1500

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
