import wpilib
import wpilib.drive
import rev


class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        self.test_motor = rev.CANSparkMax(5, rev._rev.CANSparkMaxLowLevel.MotorType.kBrushless)
        self.stick = wpilib.Joystick(1)
        self.timer = wpilib.Timer()

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.timer.reset()
        self.timer.start()
        

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""

        # Drive for two seconds
        if self.timer.get() < 2.0:
            self.test_motor.set(0.1)  # Drive forwards at half speed
        else:
            self.test_motor.set(0.0)  # Stop robot

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        self.test_motor.set(self.stick.getY())


if __name__ == "__main__":
    wpilib.run(MyRobot)
