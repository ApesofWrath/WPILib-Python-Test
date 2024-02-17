# Streamlines implementation of periphierals like xbox controllers, keybaords
import wpilib
import wpimath
import wpimath.filter

from queue import Queue
import threading

from extras.debugmsgs import *

import numpy as np

# Load constants from the json file
import json
with open('constants.json') as jsonf:
	constants = json.load(jsonf)
	jsonf.close()

class XboxController():
    def __init__(self, globals):
        self.globals = globals # Import a specific globals namespace to call functions from annother python script

        self.controller = wpilib.XboxController(constants['CONTROLLER_CONSTANTS']['CONTROLLER_MAIN_ID'])
        # Slew rate limiters to make joystick inputs more gentle; 1/3 sec from 0 to 1.
        self.xSpeedLimiter = wpimath.filter.SlewRateLimiter(constants['CONTROLLER_CONSTANTS']['CONTROLLER_RATE_LIMIT'])
        self.ySpeedLimiter = wpimath.filter.SlewRateLimiter(constants['CONTROLLER_CONSTANTS']['CONTROLLER_RATE_LIMIT'])
        self.rotLimiter = wpimath.filter.SlewRateLimiter(constants['CONTROLLER_CONSTANTS']['CONTROLLER_RATE_LIMIT'])

        # Booleans that indicate if a button is pressed, then released
        self.buttonA = self.controller.getAButtonReleased()
        self.buttonB = self.controller.getBButtonReleased()
        self.buttonX = self.controller.getXButtonReleased()
        self.buttonY = self.controller.getYButtonReleased()
        self.bumperLeft = self.controller.getLeftBumperReleased()
        self.bumperRight = self.controller.getRightBumperReleased()
        self.triggerLeftValue = self.controller.getLeftTriggerAxis()
        self.triggerRightValue = self.controller.getRightTriggerAxis()

        # Values of the left and right stick
        self.stickLeftClicked = self.controller.getLeftStickButtonReleased() # This actually registers true when released

        self.stickRightClicked = self.controller.getRightStickButtonReleased() # This actually registers true when released

        # An array of all of the boolean values that we can bind a macro too
        self.values = np.array([
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
        self.valuesFucntions = [constants['CONTROLLER_CONSTANTS']['MACROS'][key] for key in ['A', 'B', 'X', 'Y', 'L_BUMPER', 'R_BUMPER', 'L_STICK', 'R_STICK']]

    def callFunctionByName(self, name):
        # Using globals() to access functions defined in the global scope
        func = self.globals.get(name)
        
        if func is not None and callable(func):
            func()
        else:
            debugMsg(f"Function '{name}' not found.")

    def executeMacros(self):
        # Use boolean indexing to execute functions for pressed buttons
        trueValues = np.where(self.values == False)[0]

        # Run indexed values through a list comprehension to execute macros
        [self.callFunctionByName(self.valuesFucntions[index]) for index in trueValues]

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