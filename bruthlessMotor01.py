
import RPi.GPIO as GPIO
import time

PIN = 15         # BCM GPIO pin connected to the ESC signal line
PWM_FREQ = 50    # 50 Hz (typical for servo/ESC signals)

# Setup GPIO mode and PWM pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT)

# Create PWM instance on PIN with the desired frequency
pwm = GPIO.PWM(PIN, PWM_FREQ)
pwm.start(0)  # Start with 0% duty cycle
time.sleep(3)  # Allow some time for setup

def set_esc_signal(duty_cycle):
    """
    Set the PWM duty cycle for the ESC.
    Valid range for most ESCs: 5% (zero throttle) to 10% (full throttle)
    """
    pwm.ChangeDutyCycle(duty_cycle)
    print(f"ESC signal set to {duty_cycle}% duty cycle")

try:
    print("Starting ESC calibration...")
    
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
    print("Zero throttle signal sent. Waiting 4 seconds...")
    time.sleep(4)
    
    set_esc_signal(7.5)
    time.sleep(3)
    
    set_esc_signal(8)
    time.sleep(3)
    
    set_esc_signal(8.5)
    time.sleep(3)
    """
    set_esc_signal(9)
    time.sleep(1)
    
    set_esc_signal(9.5)
    time.sleep(1)
    
    set_esc_signal(10)
    time.sleep(1)
    
    set_esc_signal(10.5)
    time.sleep(1)
    
    set_esc_signal(11)
    time.sleep(1)
    
    
    set_esc_signal(7.5)
    time.sleep(3)
    
    set_esc_signal(8)
    time.sleep(1)
    
    set_esc_signal(8.5)
    time.sleep(1)
    
    set_esc_signal(9)
    time.sleep(1)
    
    
    for duty in range(3, 6, 1):  # 10% down to 5%
        set_esc_signal(duty)
        time.sleep(1)
        
    
    print("ESC calibration complete.")
    
    # Now, test motor control by ramping between 5% and 10%
    print("Testing motor control: ramping up...")
    for duty in range(5, 11):  # 5% to 10%
        set_esc_signal(duty)
        time.sleep(.1)
    
    print("Testing motor control: ramping down...")
    for duty in range(10, 4, -1):  # 10% down to 5%
        set_esc_signal(duty)
        time.sleep(.1)
    
    print("Motor control test complete. Holding zero throttle.")
    set_esc_signal(5)  # Hold at zero throttle
    time.sleep(2)
    
"""
except KeyboardInterrupt:
    print("Operation interrupted by user.")

finally:
    pwm.stop()         # Stop the PWM signal
    GPIO.cleanup()     # Clean up GPIO settings
    print("GPIO cleaned up.")
