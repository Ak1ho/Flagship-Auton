### main.py

import cv2
import threading
import time
import logging

from camera_module import CameraModule
from robot_detection import RobotDetector
from motor_control import MotorController
from remote_control import RemoteControl

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Global flag to allow switching between autonomous and remote modes
AUTONOMOUS_MODE = True

def autonomous_loop(camera, detector, motor):
    """Main loop for autonomous operation."""
    logging.info("Starting autonomous mode.")
    while True:
        frame = camera.get_frame()
        if frame is None:
            logging.error("No frame captured from camera.")
            continue

        # Detect opponent (returns center position if detected, else None)
        target = detector.detect_opponent(frame)

        if target:
            logging.info(f"Target detected at {target}.")
            # Simple decision-making: if target is left/right of center, adjust wheel speeds accordingly
            frame_center = frame.shape[1] // 2
            if target[0] < frame_center - 20:
                logging.info("Turning left.")
                motor.turn_left()
            elif target[0] > frame_center + 20:
                logging.info("Turning right.")
                motor.turn_right()
            else:
                logging.info("Moving forward.")
                motor.move_forward()
        else:
            logging.info("No target detected, stopping.")
            motor.stop()

        # Display frame with detection overlay (for debugging; remove in final autonomous deployment)
        cv2.imshow("Autonomous View", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.1)  # adjust loop speed as needed

    camera.release()
    cv2.destroyAllWindows()

def remote_control_loop(remote, motor):
    """Loop for remote control operation."""
    logging.info("Starting remote control mode.")
    while True:
        cmd = remote.get_command()
        if cmd == 'forward':
            motor.move_forward()
        elif cmd == 'backward':
            motor.move_backward()
        elif cmd == 'left':
            motor.turn_left()
        elif cmd == 'right':
            motor.turn_right()
        elif cmd == 'stop':
            motor.stop()
        elif cmd == 'exit':
            break
        else:
            logging.warning("Unknown command received.")
        time.sleep(0.1)

if __name__ == "__main__":
    try:
        # Initialize modules
        camera = CameraModule(0)  # 0 for default camera
        detector = RobotDetector()
        motor = MotorController()
        remote = RemoteControl()

        # Start the appropriate control loop (could also run both in separate threads with a mode switch)
        if AUTONOMOUS_MODE:
            autonomous_loop(camera, detector, motor)
        else:
            remote_control_loop(remote, motor)

    except KeyboardInterrupt:
        logging.info("Shutting down system.")
    except Exception as e:
        logging.exception("An error occurred in the main loop: %s", e)
