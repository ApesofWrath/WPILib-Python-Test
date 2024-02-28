# Module for controlling different motors
from extras.debugmsgs import *

import rev

class CANSparkMax:
    def __init__(self, channel,
                smartCurrentLimit,
                brushless = True,
                restoreFactoryDefaults=True, 
                setInverted=True, 
                idleMode=rev.CANSparkMax.IdleMode.kBrake):
        
        self.motor = rev.CANSparkMax(channel,
            rev.CANSparkMax.MotorType.kBrushless if brushless else rev.CANSparkMax.MotorType.kBrushed
        )

        # Configure motor
        self.motor.restoreFactoryDefaults(restoreFactoryDefaults) # Resets the motor to factory settings
        self.motor.setInverted(setInverted) # Invert the motor
        self.motor.setIdleMode(idleMode) # Sets the idle mode of the motor to brake (Motor brakes when not doing anything)
        self.motor.setSmartCurrentLimit(smartCurrentLimit) # Sets current limit for the motor

        # Encoder(s) which can be set to CANSparkMax
        self.relativeEncoder = None

        # Controller(s) which can be set to CANSparkMax
        self.PIDController = None

    def setRelativeEncoder(self, positionConversionFactor, velocityConversionFactor):
        self.relativeEncoder = self.motor.getEncoder(
                    rev.SparkRelativeEncoder.Type.kHallSensor, 42
        )

        # Configure relative encoder conversion factor (Velocity values for the external turn encoder and the built in drive encoder)
        self.relativeEncoder.setPositionConversionFactor(positionConversionFactor)
        self.relativeEncoder.setVelocityConversionFactor(velocityConversionFactor)

    def setPIDController(self, P, I, D, FF, outputRange):
        if self.relativeEncoder == None:
            errorMsg('Cannot create PID controller without a relative encoder being set',None)

        # Sets the feedback device of the drive motor to the built in motor encoder 
        # and the feedback device of the turn motor to the external encoder
        self.PIDController = self.motor.getPIDController()
        self.PIDController.setFeedbackDevice(self.relativeEncoder)

        self.PIDController.setP(P)
        self.PIDController.setI(I)
        self.PIDController.setD(D)
        self.PIDController.setFF(FF)
        self.PIDController.setOutputRange(outputRange[0], outputRange[1])