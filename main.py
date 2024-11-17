import cv2
import time
from motor_control import MotorControl
from robot_detection import RobotDetector
from remote_control import RemoteControl
import RPi.GPIO as GPIO

def main():
    GPIO.setmode(GPIO.BCM)
    MODE_PIN = 24  # GPIO pin connected to the mode switch
    GPIO.setup(MODE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Initialize modules
    motor_control = MotorControl()
    robot_detector = RobotDetector()
    remote_control = RemoteControl()

    # Open camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera not accessible")
        return

    try:
        while True:
            # Check mode switch
            if GPIO.input(MODE_PIN) == GPIO.LOW:
                mode = 'manual'
            else:
                mode = 'autonomous'

            if mode == 'autonomous':
                # Autonomous mode
                ret, frame = cap.read()
                if not ret:
                    print("Failed to read frame from camera")
                    break

                # Detect robot in the frame
                detected, direction = robot_detector.detect_robot(frame)

                if detected:
                    print("Detected!")
                    motor_control.move_towards(direction)
                    motor_control.activate_weapon(speed=100)
                else:
                    print("Searching")
                    motor_control.search_pattern()
                time.sleep(0.1)
            else:
                # Manual mode
                remote_control.update_controls()
                motor_speeds = remote_control.get_motor_speeds()
                weapon_speed = remote_control.get_weapon_speed()
                motor_control.set_wheel_speeds(motor_speeds)
                motor_control.set_weapon_speed(weapon_speed)
                time.sleep(0.05)

    except KeyboardInterrupt:
        print("Program interrupted by user")

    finally:
        cap.release()
        cv2.destroyAllWindows()
        motor_control.cleanup()
        GPIO.cleanup()
        remote_control.cleanup()

if __name__ == "__main__":
    main()
