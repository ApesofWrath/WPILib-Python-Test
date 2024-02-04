# Controlls the swerve module
# Stuck? https://github.com/robotpy/examples/blob/main/SwerveBot/swervemodule.py
         #https://robotpy.readthedocs.io/projects/wpimath/en/latest/wpimath.geometry/Translation2d.html

import math
import wpilib, rev, phoenix6
import wpimath.kinematics
import wpimath.geometry
import wpimath.controller
import wpimath.trajectory
import wpimath.units

class SwerveModule:
    def __init__(self, driveMotorChannel, turnMotorChannel, turnEncoderChannel, location):
        self.driveMotorChannel = driveMotorChannel
        self.turnMotorChannel = turnMotorChannel
        self.turnEncoderChannel = turnEncoderChannel

        # Location represents the distance (TODO: Find what unit of measurement for distance)
        # From the middle of the robot to any of the swerve modules
        self.location = wpimath.geometry.Translation2d(location[0], location[1])

        # Set up the turn (absolute) encoder 
        self.absoluteEncoder = phoenix6.hardware.CANcoder(turnEncoderChannel) #TODO: Find what 'CANBus' is

        # Set up the drive motor (motor that moves the robot in a direction)
        # and the turn motor (motor that turns the drive motor to change the direction of the robot)
        self.motorDrive = rev.CANSparkMax(driveMotorChannel, rev.CANSparkMax.MotorType.kBrushless)
        self.motorTurn = rev.CANSparkMax(turnMotorChannel, rev.CANSparkMax.MotorType.kBrushless)

        # Resets the swerve module motors and encoders to factory settings
        self.motorDrive.restoreFactoryDefaults(True)
        self.motorTurn.restoreFactoryDefaults(True)

        # Invert the motors
        self.motorDrive.setInverted(True)
        self.motorTurn.setInverted(True)

        # Sets the idle mode of the swerve module motors to brake (Motors brake when not doing anything)
        self.motorDrive.setIdleMode(rev.CANSparkMax.IdleMode.kBrake)
        self.motorTurn.setIdleMode(rev.CANSparkMax.IdleMode.kBrake)

        # Sets current limits for the swerve module motors
        self.motorDrive.SetSmartCurrentLimit(80.0)
        self.motorTurn.SetSmartCurrentLimit(20.0)

        # Set up relative encoders
        self.encoderDriveRelative = rev.SparkRelativeEncoder(
            self.motorDrive.GetEncoder(rev.SparkRelativeEncoder.Type.kHallSensor, 42))
            # 42 = refresh rate of 'kHallSensor'
        
        self.encoderTurnRelative = rev.SparkRelativeEncoder(
            self.motorTurn.GetEncoder(rev.SparkRelativeEncoder.Type.kHallSensor, 42))
        
        # Configure relative encoders (Velocity values for the external turn encoder and the built in drive encoder)
        self.encoderDriveRelative.setPositionConversionFactor(0.0508 * 2.0 * 3.141592653589 * ((14.0 / 50.0) * (25.0 / 19.0) * (15.0 / 45.0)))
        self.encoderDriveRelative.setVelocityConversionFactor(0.0508 * (2.0 * 3.141592653589 * ((14.0 / 50.0) * (25.0 / 19.0) * (15.0 / 45.0))) / 60.0)

        self.encoderTurnRelative.SetPositionConversionFactor(2.0 * 3.141592653589 * ((14.0 / 50.0) * (10.0 / 60.0)));
        self.encoderTurnRelative.SetVelocityConversionFactor((2.0 * 3.141592653589 * ((14.0 / 50.0) * (10.0 / 60.0))) / 60.0);


        # Set up PID constrollers
        self.controllerDrive = rev.SparkPIDController(self.driveMotor.getPIDController())
        self.controllerTurn = rev.SparkPIDController(self.motorTurn.getPIDController())

        # Sets the feedback device of the drive motor to the built in motor encoder 
        # sand the feedback device of the turn motor to the external encoder
        self.controllerDrive.setFeedbackDevice(self.encoderDriveRelative)
        self.controllerTurn.setFeedbackDevice(self.encoderTurnRelative)

        # Configure PID for the controllers
        self.controllerDrive.setP(0.01)
        self.controllerDrive.setI(0)
        self.controllerDrive.setD(0)
        self.controllerDrive.SetFF(1.0/73.0)
        self.controllerDrive.SetOutputRange(-1.0, 1.0)

        self.controllerTurn.setP(0.015)
        self.controllerTurn.setI(0)
        self.controllerTurn.setD(0.001)
        self.controllerTurn.setFF(0)
        self.controllerTurn.setOutputRange(-1.0, 1.9)

    def getPosition(self):
        # Returns the location from the drive controller and the rotation from the turn encoder
        return (
            (wpimath.units.meters(self.encoderDriveRelative.getPosition())),
            (wpimath.geometry.Rotation2d(
                wpimath.angleModulus(
                    wpimath.units.degrees(float(self.encoderTurnRelative.getPosition())  *360.0)
                        )
                    )
                )
            )
    
    def getState(self):
        # Returns the speed (meters/second) from the drive encoder and the rotation from the turn encoder
        return (
            (wpimath.units.meters_per_second(self.encoderDriveRelative.getVelocity())),
            (wpimath.geometry.Rotation2d(
                wpimath.angleModulus(wpimath.units.degrees(
                    float(self.encoderTurnRelative.getPosition() * 360.0)
                        )
                    )
                )
            )
        )