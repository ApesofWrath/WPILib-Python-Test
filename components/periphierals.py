# Streamlines implementation of periphierals like xbox controllers, keybaords, button stations, etc.
import wpilib
import wpimath
import wpimath.filter

from extras.debugmsgs import *

import numpy as np

# Load constants from the json file
import json
with open('constants.json') as jsonf:
	constants = json.load(jsonf)
	jsonf.close()

class XboxController():
    def __init__(self, instance):
        self.instance = instance # The instance should be the name of the class of your robot

        # Define our controller
        self.controller = wpilib.XboxController(constants['CONTROLLER_CONSTANTS']['CONTROLLER_MAIN_ID'])

        # Slew rate limiters to make joystick inputs more gentle; 1/3 sec from 0 to 1.
        self.xSpeedLimiter = wpimath.filter.SlewRateLimiter(constants['CONTROLLER_CONSTANTS']['CONTROLLER_RATE_LIMIT'])
        self.ySpeedLimiter = wpimath.filter.SlewRateLimiter(constants['CONTROLLER_CONSTANTS']['CONTROLLER_RATE_LIMIT'])
        self.rotLimiter = wpimath.filter.SlewRateLimiter(constants['CONTROLLER_CONSTANTS']['CONTROLLER_RATE_LIMIT'])

        # An array of all of the boolean values that we can bind a macro too
        self.values = np.array([
            self.controller.getStartButtonReleased(),
            self.controller.getAButtonReleased(),
            self.controller.getBButtonReleased(),
            self.controller.getXButtonReleased(),
            self.controller.getYButtonReleased(),
            self.controller.getLeftBumperReleased(),
            self.controller.getRightBumperReleased(),
            self.controller.getLeftStickButtonReleased(),
            self.controller.getRightStickButtonReleased()
        ])

        # Eack key can be set in 'constants.json' to carry out a function in annother python script
        self.valuesFucntions = [constants['CONTROLLER_CONSTANTS']['MACROS'][key] for key in ['START', 'A', 'B', 'X', 'Y', 'L_BUMPER', 'R_BUMPER', 'L_STICK', 'R_STICK']]

    def callFunctionByName(self, macroName):
        # Use 'getattr()' to dynamically call the macro (method) by name
        macroToCall = getattr(self.instance, macroName, None)

        if macroToCall and callable(macroToCall):
            macroToCall()
        else:
            errorMsg(f"Method '{macroName}' not found or not callable.", None)

    def executeMacros(self):
        # Use boolean indexing to execute functions for pressed buttons
        trueValues = np.where(self.values == True)[0]

        # Run indexed values through a list comprehension to execute macros
        for index in trueValues:
            self.callFunctionByName(self.valuesFucntions[index])
            
    # Returns calculated values from xbox controller input to appropriate swervedrive values
    def getSwerveValues(self):
        # Get the x speed. We are inverting this because Xbox controllers return
        # negative values when we push forward.
        xSpeed = (
            -self.xSpeedLimiter.calculate(
                wpimath.applyDeadband(self.controller.getLeftX(), 0.02)) * constants['CALCULATIONS']['CHASSIS_MAX_SPEED']
        )

        # Get the y speed or sideways/strafe speed. We are inverting this because
        # we want a positive value when we pull to the left. Xbox controllers
        # return positive values when you pull to the right by default.
        ySpeed = (
            -self.ySpeedLimiter.calculate(
                wpimath.applyDeadband(self.controller.getLeftY(), 0.02)) * constants['CALCULATIONS']['CHASSIS_MAX_SPEED']
        )

        # Get the rate of angular rotation. We are inverting this because we want a
        # positive value when we pull to the left (remember, CCW is positive in
        # mathematics). Xbox controllers return positive values when you pull to
        # the right by default.
        rot = (
            -self.rotLimiter.calculate(
                wpimath.applyDeadband(self.controller.getRightX(), 0.02)) * constants['CALCULATIONS']['CHASSIS_MAX_SPEED']
        )

        return xSpeed, ySpeed, rot