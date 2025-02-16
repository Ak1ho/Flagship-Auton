"""
main.py
Entry point for the autonomous robot behavior.
Sets up camera, detection, motor control, and remote override logic.
Implements a basic state machine for robot behavior.
"""

import time
import cv2
from motor_control import MotorController
from robot_detection import OpponentDetector
from remote_control import RemoteControl

def main():
    # Initialize hardware modules
    # Example pin definitions (adjust as per your hardware)
    left_motor_pins = (17, 18)    # Example GPIO pins
    right_motor_pins = (27, 22)
    spinner_motor_pin = 23

    motor_controller = MotorController(
        left_motor_pins, right_motor_pins, spinner_motor_pin
    )

    # Initialize detection
    detector = OpponentDetector(
        color_lower=(0, 120, 70),   # Example HSV range for red-ish color
        color_upper=(10, 255, 255)
    )

    # Initialize remote control
    remote = RemoteControl()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open camera.")
        return

    # Basic robot states
    state = "IDLE"
    motor_controller.spin_weapon(on=False)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Camera read error. Stopping.")
                break

            # Update remote control commands
            remote.update_command()
            if remote.is_override_active():
                # If manual override, just read commands and pass to motors
                cmd = remote.get_command()
                if cmd:
                    # e.g. interpret cmd like ('FORWARD', 0.8)
                    pass
                else:
                    motor_controller.stop()
                continue

            # AUTONOMOUS BEHAVIOR
            # 1. Detect opponent
            center = detector.detect_opponent(frame)

            if center:
                # Robot logic if opponent is seen
                (cx, cy) = center
                frame_center_x = frame.shape[1] // 2
                # Simple strategy: if center is left of mid, turn left; if right, turn right; if center, go forward
                # Fine-tune turning threshold as needed.
                if abs(cx - frame_center_x) < 50:
                    # Opponent roughly in front
                    motor_controller.set_speed(0.5, 0.5)  # Move forward
                    motor_controller.spin_weapon(on=True)
                else:
                    # Turn towards the opponent
                    if cx < frame_center_x:
                        motor_controller.set_speed(-0.3, 0.3)  # Turn left
                    else:
                        motor_controller.set_speed(0.3, -0.3)  # Turn right
                    motor_controller.spin_weapon(on=True)
            else:
                # Opponent not found - spin in place looking for target
                motor_controller.set_speed(0.3, -0.3)
                motor_controller.spin_weapon(on=False)

            # Visual feedback (optional)
            cv2.imshow('Robot Camera', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                # Quit if 'q' is pressed on the keyboard
                break

            time.sleep(0.02)  # small delay for loop

    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        motor_controller.cleanup()

if __name__ == "__main__":
    main()
