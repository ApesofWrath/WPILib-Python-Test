# Controlls the swerve module
# Stuck? https://github.com/robotpy/examples/blob/main/SwerveBot/swervemodule.py
         #https://robotpy.readthedocs.io/projects/wpimath/en/latest/wpimath.geometry/Translation2d.html
# TODO: Import libraries (dont ask which ones nobody knows)
import wpimath

class SwerveModule:
    def __init__(self, driveMotorChannel, turnMotorChannel, driveEncoderChannel, turnEncoderChannel, location) -> None:
        self.driveMotorChannel = driveMotorChannel
        self.turnMotorChannel = turnMotorChannel
        self.driveEncoderChannel = driveEncoderChannel
        self.turnEncoderChannel = turnEncoderChannel

        # Location represents the distance (TODO: Find what unit of measurement for distance)
        # From the middle of the robot to any of the swerve modules
        # Check the links above more more explanation...
        self.location = wpimath.geometry.Translation2d(location[0], location[1])