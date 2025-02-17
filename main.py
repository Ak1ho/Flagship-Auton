import cv2
import time

from camera_module import CameraModule
from robot_detection import RobotDetector
from motor_control import MotorController
from remote_control import RemoteControl

def main():
    camera = CameraModule(camera_index=0, width=640, height=480)
    detector = RobotDetector()
    motors = MotorController()
    remote = RemoteControl()

    camera.start()
    remote.start()

    autonomous_mode = True

    print("Starting main loop. Press 'r' to toggle remote override, 'k' for kill switch, or 'q' to quit.")
    try:
        while True:
            # Check if kill switch has been pressed
            if remote.kill_switch:
                print("Kill switch activated. Stopping all motors.")
                motors.stop_all()
                break

            if remote.remote_override:

                autonomous_mode = False
                command = remote.last_command
                if command == 'w':
                    motors.drive_forward(speed=0.5)
                elif command == 's':
                    motors.drive_backward(speed=0.5)
                elif command == 'a':
                    motors.turn_left(speed=0.5)
                elif command == 'd':
                    motors.turn_right(speed=0.5)
                else:
                    motors.stop_drivetrain()

            else:
                autonomous_mode = True
                frame = camera.get_frame()
                if frame is None:
                    continue
                opponent_center = detector.detect_opponent(frame)
                height, width, _ = frame.shape

                if opponent_center:
                    cx, cy = opponent_center
                    center_x = width // 2
                    diff_x = cx - center_x

                    motors.spin_up(speed=1.0)

                    if abs(diff_x) < 40:
                        motors.drive_forward(speed=0.5)
                    elif diff_x < 0:
                        motors.turn_left(speed=0.4)
                    else:
                        motors.turn_right(speed=0.4)
                else:
                    motors.spin_up(speed=0.8)
                    motors.turn_left(speed=0.3)

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Keyboard interrupt received. Exiting...")

    finally:
        motors.stop_all()
        camera.release()
        remote.stop()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
