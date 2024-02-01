from modules.debugmsgs import debugMsg, successMsg, errorMsg # Colorfull messages that we can use
import constants # 'constants/__init__.py'

try:
    from components.drivetrain import Drivetrain
    # Print debug message that all "drivetrain" modules were imported successfully
    successMsg('components.drivetrain: import SwerveDrive')
except Exception as e:
    # If imports fail, print an error message
    errorMsg('Cound not import components.drivetrain: SwerveDrive:', e)


# Import robot modules
try:
    import wpilib
    import wpilib.drive

    import wpimath
    import wpimath.filter
    import wpimath.controller
    # Print debug message that all robot modules were imported successfully
    successMsg('Robot modules imported')

except Exception as e: 
    # If imports fail, print an error message
    errorMsg('Cound not import robot modules:', e)

# Create the robot class (his name is terrance)
class terrance(wpilib.TimedRobot):
    def robotInit(self) -> None:
        self.drivetrain = Drivetrain()

        self.controller = wpilib.XboxController(constants.CONTROLLER_MAIN_ID) # Member variable of our Xbox controller

        # Slew rate limiters to make joystick inputs more gentle; 1/3 sec from 0 to 1.
        self.xSpeedLimiter = wpimath.filter.SlewRateLimiter(3)
        self.ySpeedLimiter = wpimath.filter.SlewRateLimiter(3)
        self.rotLimiter = wpimath.filter.SlewRateLimiter(3)

    def autonomousPeriodic(self) -> None:
        self.driveWithJoystick(False) # Disable joystick controll in autonomous mode
        self.drivetrain.updateOdometry() # TODO: Add this method to 'components/drivetrain.py'

    def teleopPeriodic(self) -> None:
        self.driveWithJoystick(True)

    def driveWithJoystick(self, state) -> None:
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

        self.drivetrain.drive(xSpeed, ySpeed, rot, state, self.getPeriod()) # TODO: Add this method to 
                                                                            # 'components/drivetrain.py'