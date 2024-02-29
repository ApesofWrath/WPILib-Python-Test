from extras.debugmsgs import * # Formatted messages used for debugging

# Different components (components interact with hardware)
from components.drivetrain import Drivetrain
from hardware.periphierals import XboxController

# Custom event manager class (for controller macros)
from eventmanager.manager import Manager

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
        self.drivetrain = Drivetrain()
        successMsg('Drivetrain initialized')

        try:
            self.controller = XboxController(self) # Link the xbox controller to the terrance class
            successMsg('Xbox controller initialized')
        except Exception as e:
            errorMsg('Issue in initializing xbox controller:', e, __file__)

        # Create an event manager and link macros to their specific events
        # IMPORTANT: Make sure specific macros do not execute in specific robot stages
        self.eventManager = Manager()

        self.eventManager.addMacrosToEvent('PERIODIC', 
                                           ['zeroGyro', 
                                            'slowDownSwerve',
                                            'resetSwerveSpeed'])
    
    # Add proccesses that should always be running at all times here
    def robotPeriodic(self):
        # Execute macros based on controller state
        self.controller.executeMacrosInEvent('PERIODIC')
    
    def disabledPeriodic(self):
        # TODO: Add functionality
        pass

    def autonomousInit(self): 
        # Called only at the beginning of autonomous mode.
        debugMsg('Entering autonomous mode')

        # Vibrate xbox controller to let driver know they are in auton mode
        self.controller.rumble(0.5)

    def autonomousPeriodic(self): 
        # Called every 20ms in autonomous mode.

        self.driveWithJoystick(False) # Disable joystick controll in autonomous mode
        self.drivetrain.updateOdometry()

    def teleopInit(self): 
        # Called only at the begining of teleop mode
        debugMsg('Entering tele-operated mode')

        # Stop vibrating xbox controller to let driver know they are in teleop mode
        self.controller.rumble(0.0)
    def teleopPeriodic(self):
        # Enable drive mode with joystick
        self.controller.getSwerveValues()
        self.driveWithJoystick(True)

    def autonomousExit(self):
        # Called when exiting autonomous mode
        debugMsg('Exiting autonomous mode')

    def teleopExit(self):
        # Called when exiting teleop mode
        debugMsg('Exiting tele-operated mode')

    # Custom methos to drive with joystick
    def driveWithJoystick(self, state):
        self.controller.getSwerveValues()
        self.drivetrain.drive(self.controller.xSpeed, 
                              self.controller.ySpeed, 
                              self.controller.rot, state, 
                              self.getPeriod())

    '''
    
    MACROS:
        Below, add functions that can be linked to specific buttons 
        on a compatible peripherial device
    
    '''
    def zeroGyro(self):
        self.drivetrain.navx.zeroYaw()

    def slowDownSwerve(self):
        pass

    def resetSwerveSpeed(self):
        pass