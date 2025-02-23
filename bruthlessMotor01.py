import RPi.GPIO as GPIO
import time

PIN = 15  # GPIO pin connected to the motor
PWM_FREQ = 50

# Setup GPIO mode and PWM pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT)

# Create PWM instance with frequency 50 Hz
pwm = GPIO.PWM(PIN, 50)
pwm.start(0)  # Start PWM with 0% duty cycle (off)
time.sleep(2)

time.sleep(2)

def set_motor_speed(duty_cycle):
    pwm.ChangeDutyCycle(duty_cycle)
    print(f"Motor speed set to {duty_cycle}%")

try:
    print("Starting ESC calibration...")
    
    # 1) Full throttle (~10% duty cycle for 2 ms pulse in a 20 ms period)
    #    This signals 'max throttle' to the ESC
    pwm.ChangeDutyCycle(10)  
    print("Full throttle signal sent. Waiting 2 seconds...")
    time.sleep(2)
    
    # 2) Zero throttle (~5% duty cycle for 1 ms pulse in a 20 ms period)
    #    This signals 'min throttle' to the ESC
    pwm.ChangeDutyCycle(5)
    print("Zero throttle signal sent. Waiting 2 seconds...")
    time.sleep(2)

    print("ESC should now be calibrated.")
    
    # Set throttle to zero (or off) just to be safe
    pwm.ChangeDutyCycle(0)
    print("Throttle set to 0%. Waiting a moment...")
    time.sleep(2)
    
    # Decrease speed from 100% to 50% with steps of 10%
    for i in range(100, 50, -10):
        set_motor_speed(i)
        time.sleep(1)

    # Increase speed from 50% to 100% with steps of 10%
    for i in range(50, 100, 10):
        set_motor_speed(i)
        time.sleep(1)

    time.sleep(5)  # Keep the motor running for a while at full speed

except KeyboardInterrupt:
    pass
finally:
    pwm.stop()  # Stop the PWM signal
    GPIO.cleanup()  # Clean up GPIO settings
    print("GPIO cleaned up.")
