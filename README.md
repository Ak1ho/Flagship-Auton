Flagship Auton

This repository contains the source code for an autonomous robotics system built on a horizontal spinner weapon platform with two wheels per side. The system uses a camera module to detect opponents and autonomously navigate toward them. There is also support for remote (manual) control as an override.

Modules

- main.py  
  Entry point that ties together the camera module, robot detection, and motor control. It includes a main loop that processes camera frames and decides movement commands.

- camera_module.py  
  Contains the `CameraModule` class that wraps OpenCV’s video capture functionality.

- robot_detection.py  
  Contains the `RobotDetector` class which processes video frames (using basic color segmentation as an example) to locate opponents.

- motor_control.py  
  Contains the `MotorController` class to control wheel movements (forward, backward, turn, stop). Modify the hardware control code as needed.

- remote_control.py  
  Contains the `RemoteControl` class for manual control override. This may use keyboard input or another interface.

- test_camera.py  
  A test script to verify that the camera module and detection overlay are working as expected.

Usage

1. Install dependencies:
   pip3 install opencv-python
