import time
import cv2
from camera_module import CameraModule
from robot_detection import RobotDetector  # <-- Make sure this is the advanced version
from motor_control import MotorController
from remote_control import RemoteControl

def main():
    # -----------------------------
    # 1) Initialize Hardware
    # -----------------------------
    # Example BCM pins for the 4 drive motors
    motor_pins = [17, 27, 22, 23]
    # BCM pin for the spinner weapon
    spinner_pin = 24

    # Create MotorController (RPi.GPIO PWM)
    motor_controller = MotorController(motor_pins, spinner_pin, pwm_freq=1000)

    # Create CameraModule (OpenCV capture)
    camera = CameraModule(camera_index=0, width=640, height=480)

    # Create our advanced classical RobotDetector
    # Adjust parameters as needed (e.g., color filtering, thresholds)
    detector = RobotDetector(
        min_area=500,
        use_color_filter=False,
        # If you want to enable color filtering for a particular color, set:
        # use_color_filter=True,
        # lower_color=(0, 100, 100),
        # upper_color=(10, 255, 255),
        history=500,
        var_threshold=16
    )

    # Single-pin FlySky iBus (Placeholder or real UART approach in ibus.py)
    # Also includes a kill switch channel
    remote_control = RemoteControl(
        ibus_gpio_pin=21,   # or /dev/ttyAMA0 if using a real UART approach
        mode_channel=4,     # channel for manual/auton toggle
        x_channel=0,
        y_channel=1,
        rotate_channel=3,
        killswitch_channel=5
    )

    # Start spinner at full throttle (100% duty)
    motor_controller.start_spinner()

    try:
        while True:
            # -----------------------------
            # 2) Read RC input
            # -----------------------------
            remote_control.update()

            # -----------------------------
            # 3) Check Kill Switch
            # -----------------------------
            if remote_control.get_killswitch():
                # Immediately stop all motors and spinner
                motor_controller.stop_all()
                motor_controller.stop_spinner()
                # Wait a bit and continue checking in next loop iteration
                time.sleep(0.1)
                continue

            # -----------------------------
            # 4) Manual vs. Autonomous
            # -----------------------------
            mode = remote_control.get_mode()

            if mode == 0:
                # ---- MANUAL MODE ----
                x_cmd, y_cmd, r_cmd = remote_control.get_movement()
                motor_controller.xdrive_move(x_cmd, y_cmd, r_cmd)

            else:
                # ---- AUTONOMOUS MODE ----
                frame = camera.get_frame()
                detection = detector.detect_robot(frame)

                if detection is None:
                    # No robot detected => spin in place searching
                    motor_controller.search_spin()
                else:
                    # Move towards the detected robot
                    cx, cy = detection
                    height, width, _ = frame.shape
                    center_x = width // 2
                    center_y = height // 2

                    # Error signals: how far from center
                    error_x = (cx - center_x) / float(center_x)  # range ~ -1..+1
                    error_y = (center_y - cy) / float(center_y)  # range ~ -1..+1

                    # Simple proportional gain
                    kP = 0.4
                    move_x = kP * error_x
                    move_y = kP * error_y
                    rotate = 0.0  # no rotation in this example

                    # Clamp speeds
                    def clamp(val, low=-1.0, high=1.0):
                        return max(low, min(high, val))
                    move_x = clamp(move_x)
                    move_y = clamp(move_y)

                    motor_controller.xdrive_move(move_x, move_y, rotate)

            # Sleep briefly to avoid 100% CPU usage
            time.sleep(0.02)

    except KeyboardInterrupt:
        print("Shutting down...")

    finally:
        # Cleanup on exit
        remote_control.close()
        camera.release()
        motor_controller.shutdown()

if __name__ == "__main__":
    main()
