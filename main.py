import time
import cv2
from camera_module import CameraModule
from robot_detection import RobotDetector
from motor_control import MotorController
from remote_control import RemoteControl

def main():
    left_pins=(17,18)
    right_pins=(27,22)
    weapon_pin=23
    motor=MotorController(left_pins,right_pins,weapon_pin)
    detector=RobotDetector()
    remote=RemoteControl()
    cam=CameraModule(0)
    state="IDLE"
    motor.spin_weapon(False)
    while True:
        frame=cam.read_frame()
        if frame is None:break
        remote.update_command()
        if remote.is_override_active():
            c=remote.get_command()
            if c:pass
            else:motor.stop()
            continue
        ctr=detector.detect(frame)
        if ctr:
            cx,cy=ctr
            mid=frame.shape[1]//2
            if abs(cx-mid)<50:
                motor.set_speed(0.5,0.5)
                motor.spin_weapon(True)
            else:
                if cx<mid:motor.set_speed(-0.3,0.3)
                else:motor.set_speed(0.3,-0.3)
                motor.spin_weapon(True)
        else:
            motor.set_speed(0.3,-0.3)
            motor.spin_weapon(False)
        cv2.imshow("Robot",frame)
        if cv2.waitKey(1)&0xFF==ord('q'):break
        time.sleep(0.02)
    cam.release()
    cv2.destroyAllWindows()
    motor.cleanup()

if __name__=="__main__":
    main()
