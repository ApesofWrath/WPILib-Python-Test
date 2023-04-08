import wpilib
import wpilib.drive
import wpimath
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
        self.swerveLocations = {
            "frontright":wpimath.geometry.Translation2d(0.3556, -0.3556),
            "rearright":wpimath.geometry.Translation2d(0.3556, -0.3556),
            "frontleft":wpimath.geometry.Translation2d(0.3556, -0.3556),
            "rearleft":wpimath.geometry.Translation2d(0.3556, -0.3556),
        }
        self.robotCenter = wpimath.geometry.Translation2d(0.0, 0.0)
        self.kinematics = wpimath.kinematics.SwerveDrive4Kinematics(self.swerveLocations["frontright"], 
                                                                    self.swerveLocations["rearright"], 
                                                                    self.swerveLocations["frontleft"], 
                                                                    self.swerveLocations["rearleft"])
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
        chassisSpeeds = wpimath.kinematics.ChassisSpeeds(self.stick.getX(), self.stick.getY(), 0)
        fl, fr, bl, br = self.kinematics.toSwerveModuleStates(chassisSpeeds)

if __name__ == "__main__":
    wpilib.run(MyRobot)
