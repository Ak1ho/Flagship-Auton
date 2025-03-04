import RPi.GPIO as GPIO
import time

# --- 1. GPIO Pin Assignments ---
ESC_PINS = [15, 27, 24, 9]  # GPIO pins connected to the ESC signal lines
PWM_FREQ = 50               # 50 Hz (typical for servo/ESC signals)

# --- 2. Setup GPIO and PWM for all ESCs ---
GPIO.setmode(GPIO.BCM)
pwm_objects = []

for pin in ESC_PINS:
    GPIO.setup(pin, GPIO.OUT)
    pwm = GPIO.PWM(pin, PWM_FREQ)
    pwm.start(0)  # Start with 0% duty cycle
    pwm_objects.append(pwm)

time.sleep(3)  # Allow some time for setup

# --- 3. Function to set ESC signal ---
def set_esc_signal(duty_cycle, esc_index=None):
    if esc_index is None:
        # Update all ESCs
        for i, pwm in enumerate(pwm_objects):
            pwm.ChangeDutyCycle(duty_cycle)
            print(f"ESC {i+1} signal set to {duty_cycle}% duty cycle")
    else:
        # Update specific ESC
        pwm_objects[esc_index].ChangeDutyCycle(duty_cycle)
        print(f"ESC {esc_index+1} signal set to {duty_cycle}% duty cycle")

# --- 4. Main Control Loop ---
try:
    print("Starting ESC calibration...")

    # --- Calibration Sequence ---
    # 1) Full throttle signal (approx. 10% duty cycle)
    set_esc_signal(10)
    print("Full throttle signal sent. Waiting 4 seconds...")
    time.sleep(4)

    # 2) Zero throttle signal (approx. 5% duty cycle)
    set_esc_signal(5)
    print("Zero throttle signal sent. Waiting 3 seconds...")
    time.sleep(3)

    # 3) Half throttle signal (approx. 7.5% duty cycle)
    set_esc_signal(7.5)
    print("Half throttle signal sent. Waiting 4 seconds...")
    time.sleep(4)

    set_esc_signal(7.5)
    time.sleep(3)

    set_esc_signal(8)
    time.sleep(3)

    set_esc_signal(8.5)
    time.sleep(3)

    # --- Ramp Testing ---
    print("Testing motor control: ramping up...")
    for duty in range(5, 11):  # 5% to 10%
        set_esc_signal(duty)
        time.sleep(0.5)

    print("Testing motor control: ramping down...")
    for duty in range(10, 4, -1):  # 10% down to 5%
        set_esc_signal(duty)
        time.sleep(0.5)

    print("Motor control test complete. Holding zero throttle.")
    set_esc_signal(5)  # Hold at zero throttle
    time.sleep(2)

except KeyboardInterrupt:
    print("Operation interrupted by user.")

finally:
    # Stop all PWM signals and clean up GPIO
    for pwm in pwm_objects:
        pwm.stop()
    GPIO.cleanup()
    print("GPIO cleaned up.")
