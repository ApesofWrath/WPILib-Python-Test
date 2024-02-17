from extras.debugmsgs import * # Formatted messages used for debugging

from components.drivetrain import Drivetrain
from components.periphierals import XboxController

# Import robot modules
import wpilib

import wpimath
import wpimath.filter

# Load constants from the json file
import json
with open('constants.json') as jsonf:
	constants = json.load(jsonf)
	jsonf.close()

# Create the robot class (his name is terrance)
class terrance(wpilib.TimedRobot):
    def robotInit(self):
        # Robot initialization
        debugMsg('Terance')
        self.drivetrain = Drivetrain()

        try:
            self.controller = XboxController(globals())
            successMsg('Xbox controller initialized')
        except Exception as e:
            errorMsg('Issue in initializing xbox controller:', e, __file__)
            pass

        self.controller.executeMacros()
        return super().robotInit()
    
    def robotPeriodic(self):
        # TODO: Add functionality
        return super().robotPeriodic()
    
    def disabledPeriodic(self):
        # TODO: Add functionality
        return super().disabledPeriodic()

    def autonomousInit(self): 
        # Called only at the beginning of autonomous mode.
        debugMsg('Entering autonomous mode')
        return super().autonomousInit()

    def autonomousPeriodic(self): 
        # Called every 20ms in autonomous mode.
        self.driveWithJoystick(False) # Disable joystick controll in autonomous mode
        self.drivetrain.updateOdometry()
        return super().autonomousPeriodic()

    def teleopInit(self): 
        # Called only at the begining of teleop mode
        debugMsg('Entering tele-operated mode')
        return super().teleopInit()

    def teleopPeriodic(self):
        self.driveWithJoystick(True)
        return super().teleopPeriodic

    def autonomousExit(self):
        # Called when exiting autonomous mode
        debugMsg('Exiting autonomous mode')
        return super().autonomousExit()

    def teleopExit(self):
        # Called when exiting teleop mode
        debugMsg('Exiting tele-operated mode')
        return super().teleopExit()

    def driveWithJoystick(self, state):
        xSpeed, ySpeed, rot = self.controller.getSwerveValues()
        self.drivetrain.drive(xSpeed, ySpeed, rot, state, self.getPeriod())