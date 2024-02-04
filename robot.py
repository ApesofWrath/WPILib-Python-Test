from modules.debugmsgs import * # Colorfull messages that we can use
import constants # 'constants/__init__.py'

# Import drivetrain and check for errors in initialization
from components.drivetrain import Drivetrain

# Import robot modules
import wpilib
import wpilib.drive

import wpimath
import wpimath.filter
import wpimath.controller

# Create the robot class (his name is terrance)
class terrance(wpilib.TimedRobot):
    def robotInit(self):
        # Robot initialization
        self.drivetrain = Drivetrain()

        try:
            self.controller = wpilib.XboxController(constants.CONTROLLER_MAIN_ID) # Member variable of our Xbox controller
            successMsg('Xbox controller initialized')
        except Exception as e:
            #errorMsg('Issue in initializing xbox controller:', e)
            pass

        # Slew rate limiters to make joystick inputs more gentle; 1/3 sec from 0 to 1.
        self.xSpeedLimiter = wpimath.filter.SlewRateLimiter(3)
        self.ySpeedLimiter = wpimath.filter.SlewRateLimiter(3)
        self.rotLimiter = wpimath.filter.SlewRateLimiter(3)

    def autonomousInit(self): 
        # Called only at the beginning of autonomous mode.
        debugMsg('Entering autonomous mode')
        return super().autonomousInit()

    def autonomousPeriodic(self): 
        # Called every 20ms in autonomous mode.
        self.driveWithJoystick(False) # Disable joystick controll in autonomous mode
        self.drivetrain.updateOdometry()

    def teleopInit(self): 
        # Called only at the begining of teleop mode
        debugMsg('Entering tele-operated mode')
        return super().teleopInit()

    def teleopPeriodic(self):
        self.driveWithJoystick(True)

    def autonomousExit(self) -> None:
        # Called when exiting autonomous mode
        debugMsg('Exiting autonomous mode')
        return super().autonomousExit()

    def teleopExit(self) -> None:
        # Called when exiting teleop mode
        debugMsg('Exiting tele-operated mode')
        return super().teleopExit()

    def driveWithJoystick(self, state):
        # Get the x speed. We are inverting this because Xbox controllers return
        # negative values when we push forward.
        xSpeed = (
            -self.xSpeedLimiter.calculate(
                wpimath.applyDeadband(self.controller.getLeftY(), 0.02)) * constants.CHASSIS_MAX_SPEED
        )

        # Get the y speed or sideways/strafe speed. We are inverting this because
        # we want a positive value when we pull to the left. Xbox controllers
        # return positive values when you pull to the right by default.
        ySpeed = (
            -self.ySpeedLimiter.calculate(
                wpimath.applyDeadband(self.controller.getLeftX(), 0.02)) * constants.CHASSIS_MAX_SPEED
        )

        # Get the rate of angular rotation. We are inverting this because we want a
        # positive value when we pull to the left (remember, CCW is positive in
        # mathematics). Xbox controllers return positive values when you pull to
        # the right by default.
        rot = (
            -self.rotLimiter.calculate(
                wpimath.applyDeadband(self.controller.getRightX(), 0.02)) * constants.CHASSIS_MAX_SPEED
        )

        self.drivetrain.drive(xSpeed, ySpeed, rot, state, self.getPeriod())