# Controlls the swerve module
# Stuck? https://github.com/robotpy/examples/blob/main/SwerveBot/swervemodule.py
         #https://robotpy.readthedocs.io/projects/wpimath/en/latest/wpimath.geometry/Translation2d.html

import math
import wpilib, rev, phoenix6
import wpimath.kinematics
import wpimath.geometry
import wpimath.controller
import wpimath.trajectory

class SwerveModule:
    def __init__(self, driveMotorChannel, turnMotorChannel, turnEncoderChannel, location):
        self.driveMotorChannel = driveMotorChannel
        self.turnMotorChannel = turnMotorChannel
        self.turnEncoderChannel = turnEncoderChannel

        # Location represents the distance (TODO: Find what unit of measurement for distance)
        # From the middle of the robot to any of the swerve modules
        # Check the links above more more explanation...
        self.location = wpimath.geometry.Translation2d(location[0], location[1])

        # Set up the turn encoder 
        self.absoluteEncoder = phoenix6.hardware.CANcoder(turnEncoderChannel)

        # Set up the drive motor (motor that moves the robot in a direction)
        # and the turn motor (motor that turns the drive motor to change the direction of the robot)
        self.driveMotor = rev.CANSparkMax(driveMotorChannel)
        self.turnMotor = rev.CANSparkMax(turnMotorChannel)

        # Set up relative encoders
        self.encoderDriveRelative = rev.SparkRelativeEncoder(
            self.driveMotor.GetEncoder(rev.SparkRelativeEncoder.Type.kHallSensor, 42))
            # 42 = refresh rate of 'kHallSensor'
        
        self.encoderTurnRelative = rev.SparkRelativeEncoder(
            self.turnMotor.GetEncoder(rev.SparkRelativeEncoder.Type.kHallSensor, 42))
        
        # Configure relative encoders
        self.encoderDriveRelative.setPositionConversionFactor(0.0508 * 2.0 * 3.141592653589 * ((14.0 / 50.0) * (25.0 / 19.0) * (15.0 / 45.0)))
        self.encoderDriveRelative.setVelocityConversionFactor(0.0508 * (2.0 * 3.141592653589 * ((14.0 / 50.0) * (25.0 / 19.0) * (15.0 / 45.0))) / 60.0)


    def getPosition(self) -> wpimath.kinematics.SwerveModulePosition:
        #Returns the current position of the module.
        return wpimath.kinematics.SwerveModulePosition(
            self.encoderDriveRelative.getPosition(),
            wpimath.geometry.Rotation2d(self.encoderTurnRelative.get()),
        )