# Controlls the swerve module
# Stuck? https://github.com/robotpy/examples/blob/main/SwerveBot/drivetrain.py
# TODO: Import libraries (dont ask which ones nobody knows)
import wpimath

class SwerveModule:
    def __init__(self, driveMotorChannel, turnMotorChannel, driveEncoderChannel, turnEncoderChannel, location) -> None:
        self.driveMotorChannel = driveMotorChannel
        self.turnMotorChannel = turnMotorChannel
        self.driveEncoderChannel = driveEncoderChannel
        self.turnEncoderChannel = turnEncoderChannel
        self.location = wpimath.geometry.Translation2d(location[0], location[1])