from os import environ
import logging
import pint
ureg = pint.UnitRegistry()
from math import pi

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Get the name of the robot (may be moved to main.py)
robot_name = environ.get("Robot")
logger.info("Current Robot %s", robot_name)

class ControllerConstants:
    ControllerMainID = 0
    ControllerAuxID = 1
    
class DrivetrainConstants:
    kMotorDriveFrontRightID = 26
    kMotorDriveRearRightID = 1
    kMotorDriveFrontLeftID = 2
    kMotorDriveRearLeftID = 3

    kMotorTurnFrontRightID = 4
    kMotorTurnRearRightID = 5
    kMotorTurnFrontLeftID = 6
    kMotorTurnRearLeftID = 7

    kEncoderTurnFrontRightID = 8
    kEncoderTurnRearRightID = 9
    kEncoderTurnFrontLeftID = 10
    kEncoderTurnRearLeftID = 11

    class Offsets:
        print(environ.get("Robot"))
            
        # Set the offsets depending on the robot name 
        # Maybe add default Case
        if robot_name is None:
            raise Exception("Robot Name Not Set!")
        if robot_name == "Kava":
            kFrontRight = [-40.429]
            kRearRight = [66.181]
            kFrontLeft = [-94.921]
            kRearLeft = [-1.142]

        elif robot_name == "T-Shirt Shooter":
            kFrontRight = [145.107] 
            kRearRight = [60.732]
            kFrontLeft = [39.023]
            kRearLeft = [2.285]
        else:
            raise Exception("Robot Name Invalid!")

    class Calculations:
        kFinalDriveRatio= 6.75 * 360 #degrees
        kFinalTurnRatio = (14.0 / 50.0) * (10.0 / 60.0)
        kWheelCircumference = pi * 3.8 #inches

        kModuleMaxSpeed = 16.3 #Feet Per Second
        kChassisMaxSpeed = 16.3

        kModuleMaxAngularVelocity= pi * 4  #radians per second
        kModuleMaxAngularAcceleration= pi * 8/1  #radians per second^2

        kMotorMaxOutput = 0.5
        kMotorDeadband = 0.1