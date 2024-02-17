# Controlls the swerve module
# Stuck? https://github.com/robotpy/examples/blob/main/SwerveBot/swervemodule.py
         #https://robotpy.readthedocs.io/projects/wpimath/en/latest/wpimath.geometry/Translation2d.html
import extras.debugmsgs
from extras.debugmsgs import *

import wpimath.kinematics
import wpimath.geometry
import wpimath.controller
import wpimath.trajectory
import wpimath.units

import rev, phoenix6

class SwerveModule:
    def __init__(self, driveMotorChannel, turnMotorChannel, turnEncoderChannel, location):

        # Location represents the distance (TODO: Find what unit of measurement for distance)
        # From the middle of the robot to any of the swerve modules
        self.location = wpimath.geometry.Translation2d(location[0], location[1])

        # Set up the turn (absolute) encoder
        try:
            self.absoluteEncoder = phoenix6.hardware.CANcoder(turnEncoderChannel) #TODO: Find what 'CANBus' is
            #time.sleep(5) # Give some time for phoenix6 to initialize
        except Exception as e:
            errorMsg('Could not initialize absolute encoder:',e,__file__)

        # Set up the drive motor (motor that moves the robot in a direction)
        # and the turn motor (motor that turns the drive motor to change the direction of the robot)
        try:
            self.motorDrive = rev.CANSparkMax(driveMotorChannel, rev.CANSparkMax.MotorType.kBrushless)
            self.motorTurn = rev.CANSparkMax(turnMotorChannel, rev.CANSparkMax.MotorType.kBrushless)
        except Exception as e:
            errorMsg('Could not initialize motors [rev.CANSparkMax]:',e,__file__)

        # Resets the swerve module motors and encoders to factory settings
        try:
            self.motorDrive.restoreFactoryDefaults(True)
            self.motorTurn.restoreFactoryDefaults(True)

            # Invert the motors
            self.motorDrive.setInverted(True)
            self.motorTurn.setInverted(True)

            # Sets the idle mode of the swerve module motors to brake (Motors brake when not doing anything)
            self.motorDrive.setIdleMode(rev.CANSparkMax.IdleMode.kBrake)
            self.motorTurn.setIdleMode(rev.CANSparkMax.IdleMode.kBrake)

            # Sets current limits for the swerve module motors
            self.motorDrive.setSmartCurrentLimit(80)
            self.motorTurn.setSmartCurrentLimit(20)
        except Exception as e:
            errorMsg('Could not configure motors:',e,__file__)

        # Set up relative encoders
        try:
            self.encoderDriveRelative = self.motorDrive.getEncoder(
                    rev.SparkRelativeEncoder.Type.kHallSensor, 42
            )
            
            self.encoderTurnRelative = self.motorTurn.getEncoder(
                    rev.SparkRelativeEncoder.Type.kHallSensor, 42
            )

        except Exception as e:
            errorMsg('Could not initialize relative encoders:',e,__file__)
            
        # Configure relative encoders (Velocity values for the external turn encoder and the built in drive encoder)
        try:
            self.encoderDriveRelative.setPositionConversionFactor(0.0508 * 2.0 * 3.141592653589 * ((14.0 / 50.0) * (25.0 / 19.0) * (15.0 / 45.0)))
            self.encoderDriveRelative.setVelocityConversionFactor(0.0508 * (2.0 * 3.141592653589 * ((14.0 / 50.0) * (25.0 / 19.0) * (15.0 / 45.0))) / 60.0)

            self.encoderTurnRelative.setPositionConversionFactor(2.0 * 3.141592653589 * ((14.0 / 50.0) * (10.0 / 60.0)))
            self.encoderTurnRelative.setVelocityConversionFactor((2.0 * 3.141592653589 * ((14.0 / 50.0) * (10.0 / 60.0))) / 60.0)
        except Exception as e:
            errorMsg('Could not configure relative encoders:',e)

        # Set up PID constrollers
        try:
            self.controllerDrive = self.motorDrive.getPIDController()
            self.controllerTurn = self.motorTurn.getPIDController()
        except Exception as e:
            errorMsg('Could not obtain PID controllers:',e,__file__)

        # Sets the feedback device of the drive motor to the built in motor encoder 
        # and the feedback device of the turn motor to the external encoder
        try:
            self.controllerDrive.setFeedbackDevice(self.encoderDriveRelative)
            self.controllerTurn.setFeedbackDevice(self.encoderTurnRelative)

            # Configure PID for the controllers
            self.controllerDrive.setP(0.01)
            self.controllerDrive.setI(0)
            self.controllerDrive.setD(0)
            self.controllerDrive.setFF(1.0/73.0)
            self.controllerDrive.setOutputRange(-1.0, 1.0)

            self.controllerTurn.setP(0.015)
            self.controllerTurn.setI(0)
            self.controllerTurn.setD(0.001)
            self.controllerTurn.setFF(0)
            self.controllerTurn.setOutputRange(-1.0, 1.0)
        except Exception as e:
            errorMsg('Could not configure PID controllers:',e,__file__)

        # TODO: Ask if I need to add code HERE that sets the starting positions of all parts of the swervemodule

    def getPosition(self):
        try:
            return wpimath.kinematics.SwerveModulePosition(
                wpimath.units.meters(self.encoderDriveRelative.getPosition()), 

                wpimath.geometry.Rotation2d(
                    wpimath.angleModulus(self.absoluteEncoder.get_absolute_position().value_as_double * 360.0)
                    )
                )
        except Exception as e:
            errorMsg('Could not get position:',e,__file__)
    
    def getState(self):
        try:
            # Returns the speed (meters/second) from the drive encoder and the rotation from the turn encoder
            return wpimath.kinematics.SwerveModuleState(
                wpimath.units.meters_per_second(self.encoderDriveRelative.getVelocity()), # Speed of the drive motor

                wpimath.geometry.Rotation2d(
                    wpimath.angleModulus(self.absoluteEncoder.get_absolute_position().value_as_double * 360.0) # Angle of rotation
                )
            )
        except Exception as e:
            errorMsg('Could not get state:',e,__file__)
    
    def setDesiredState(self, desiredState):
        # Sets desired state (speed & angle) of the swervemodule
        try:
            encoderRotation = wpimath.geometry.Rotation2d(
                wpimath.units.degrees(
                    float(self.absoluteEncoder.get_absolute_position().value_as_double) * 360.0)
                )
        except Exception as e:
            errorMsg('Could not get encoder rotation:',e,__file__)

        # Get the currect state of the swervemodule
        try:
            state = wpimath.kinematics.SwerveModuleState.optimize(
                desiredState, encoderRotation
            )
        except Exception as e:
            errorMsg('Could not get state:',e,__file__)

        state.speed *= ((state.angle - encoderRotation).cos()) # IDK check robotpy examples in swervedrive
        targetAngle = state.angle.degrees() # Target angle of the swervemodule

        # Get the target motor speed
        try:
            targetMotorSpeed = wpimath.units.radians_per_second(
                state.speed * wpimath.units.radians(2*3.14159) #TODO: Ask if I should use 'radians' or 'radiansToDegrees'
            )
        except Exception as e:
            errorMsg('Could not get target motor speed:',e,__file__)

        try:
            self.controllerDrive.setReference(targetMotorSpeed, rev.CANSparkMax.ControlType.kVelocity)
        except Exception as e:
            errorMsg('Could not set reference to drive controller:',e,__file__)
        
        try:
            self.encoderTurnRelative.setPosition(self.absoluteEncoder.get_absolute_position().value_as_double * 360.0)
        except Exception as e:
            errorMsg('Could not set position to relative turn encoder:',e,__file__)

        try:
            self.controllerTurn.setReference(float(targetAngle), rev.CANSparkMax.ControlType.kPosition)
        except Exception as e:
            errorMsg('Could not set reference to turn controller:',e,__file__)