from os import environ
import logging
from math import pi
logger = logging.getLogger(__name__)

# Get the name of the robot (may be moved to main.py)
ROBOT_NAME = environ.get("Robot")
logger.info("Current Robot %s", ROBOT_NAME)

class ControllerConstants:
    CONTROLLER_MAIN_ID = 0
    CONTROLLER_AUX_ID = 1
    
class DrivetrainConstants:
    MOTOR_DRIVE_FRONT_RIGHT = 26
    MOTOR_DRIVE_REAR_RIGHT_ID = 1
    MOTOR_DRIVE_FRONT_LEFT_ID = 2
    MOTOR_DRIVE_REAR_LEFT_ID = 3

    MOTOR_TURN_FRONT_RIGHT_ID = 4
    MOTOR_TURN_REAR_RIGHT_ID = 5
    MOTOR_TURN_FRONT_LEFT_ID = 6
    MOTOR_TURN_REAR_LEFT_ID = 7

    ENCODER_TURN_FRONT_LEFT_ID = 8
    ENCODER_TURN_REAR_LEFT_ID = 9
    ENCODER_TURN_FRONT_LEFT_ID = 10
    ENCODER_TURN_REAR_LEFT_ID = 11

    class Offsets:
        print(environ.get("Robot"))
            
        # Set the offsets depending on the robot name 
        # Maybe add default Case
        if ROBOT_NAME is None:
            raise Exception("Robot Name Not Set!")
        if ROBOT_NAME == "Kava":
            FRONT_RIGHT = [-40.429]
            REAR_RIGHT = [66.181]
            FRONT_LEFT = [-94.921]
            REAR_LEFT = [-1.142]

        elif ROBOT_NAME == "T-Shirt Shooter":
            FRONT_RIGHT = [145.107] 
            REAR_RIGHT = [60.732]
            FRONT_LEFT = [39.023]
            REAR_LEFT = [2.285]
        else:
            raise Exception("Robot Name Invalid!")
        
    class Calculations:
        kFinalDriveRatio = 6.75 * 360;
        kFinalTurnRatio = (14.0 / 50.0) * (10.0 / 60.0)
        kWheelCircumference = 2 * pi * 3.8 / 2;

    class Calculations:
        FINAL_DRIVE_RATIO = 6.75 * 360 #degrees
        FINAL_TURN_RATIO = (14.0 / 50.0) * (10.0 / 60.0)
        WHEEL_CIRCUMFERENCE = pi * 3.8 #inches

        MODULE_MAX_SPEED = 16.3 #Feet Per Second
        CHASSIS_MAX_SPEED = 16.3

        MODULE_MAX_ANGULAR_VELOCITY = pi * 4  #radians per second
        MODULE_MAX_ANGULAR_ACCELERATION = pi * 8/1  #radians per second^2

        MOTOR_MAX_OUTPUT = 0.5
        MOTOR_DEADBAND = 0.1
