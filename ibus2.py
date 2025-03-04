import serial
import time

# --- 1. Serial Port Setup ---
# Use the UART TX pin on the Pi to send data.
SERIAL_PORT = '/dev/serial0'  # Update as needed for your Pi
BAUD_RATE = 115200            # Choose a baud rate that FS-IA6B expects

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
except Exception as e:
    print(f"Error opening serial port: {e}")
    exit(1)

# --- 2. Mapping Function ---
def map_duty_to_value(duty, in_min=5, in_max=10, out_min=0, out_max=255):
    """
    Maps a duty cycle (in %) to a value between out_min and out_max.
    For example, duty=5 (zero throttle) -> 0, duty=10 (full throttle) -> 255.
    """
    return int((duty - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# --- 3. Packet Builder and Sender ---
def send_esc_packet(ch1, ch2, ch3, ch4):
    """
    Constructs a packet with:
      [Start Byte, ch1, ch2, ch3, ch4, Checksum]
    and sends it over the serial port.
    """
    packet = bytearray()
    packet.append(0xAA)        # Start byte
    packet.append(ch1)
    packet.append(ch2)
    packet.append(ch3)
    packet.append(ch4)
    # Checksum: simple sum modulo 256 of the previous bytes
    checksum = (0xAA + ch1 + ch2 + ch3 + ch4) & 0xFF
    packet.append(checksum)
    ser.write(packet)
    print(f"Sent packet: {[hex(b) for b in packet]}")

# --- 4. Main Control Routine (Calibration & Testing) ---
try:
    print("Starting ESC calibration via FS‑IA6B receiver...")

    # Define duty cycle values (in percent) corresponding to throttle positions.
    full_duty = 10.0      # Full throttle (approx. 10% duty cycle)
    zero_duty = 5.0       # Zero throttle (approx. 5% duty cycle)
    half_duty = 7.5       # Half throttle (approx. 7.5% duty cycle)

    # Map these duty cycles to a 0–255 range.
    full_val = map_duty_to_value(full_duty)
    zero_val = map_duty_to_value(zero_duty)
    half_val = map_duty_to_value(half_duty)

    # --- Calibration Sequence ---
    # 1) Full throttle on all ESCs
    send_esc_packet(full_val, full_val, full_val, full_val)
    print("Full throttle signal sent. Waiting 4 seconds...")
    time.sleep(4)

    # 2) Zero throttle on all ESCs
    send_esc_packet(zero_val, zero_val, zero_val, zero_val)
    print("Zero throttle signal sent. Waiting 3 seconds...")
    time.sleep(3)

    # 3) Half throttle on all ESCs
    send_esc_packet(half_val, half_val, half_val, half_val)
    print("Half throttle signal sent. Waiting 4 seconds...")
    time.sleep(4)

    # --- Demonstrate Independent Control ---
    # For example, send different throttle values to each ESC:
    send_esc_packet(half_val, full_val, zero_val, half_val)
    print("Individual channel test 1 sent. Waiting 3 seconds...")
    time.sleep(3)

    send_esc_packet(half_val, half_val, full_val, zero_val)
    print("Individual channel test 2 sent. Waiting 3 seconds...")
    time.sleep(3)

    send_esc_packet(full_val, half_val, half_val, half_val)
    print("Individual channel test 3 sent. Waiting 3 seconds...")
    time.sleep(3)

    # --- Ramp Testing ---
    print("Testing motor control: ramping up...")
    for duty in range(5, 11):  # from 5% to 10%
        val = map_duty_to_value(float(duty))
        send_esc_packet(val, val, val, val)
        time.sleep(0.5)

    print("Testing motor control: ramping down...")
    for duty in range(10, 4, -1):  # from 10% down to 5%
        val = map_duty_to_value(float(duty))
        send_esc_packet(val, val, val, val)
        time.sleep(0.5)

    print("Motor control test complete. Holding zero throttle.")
    send_esc_packet(zero_val, zero_val, zero_val, zero_val)
    time.sleep(2)

except KeyboardInterrupt:
    print("Operation interrupted by user.")
finally:
    ser.close()
    print("Serial port closed.")
