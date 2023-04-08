class swerveModule:
    __init__(self, m_motorDrive, m_motorTurn, m_encoderTurn, m_encoderOffset):
        # Resets the swerve module motors and encoders to factory settings
        m_motorDrive.RestoreFactoryDefaults()
        m_motorTurn.RestoreFactoryDefaults()
        m_encoderTurn.ConfigFactoryDefault()


        # Sets both the drive motor and the turn motor to be inverted
        m_motorDrive.SetInverted(True)
        m_motorTurn.SetInverted(True)

        # Sets the idle mode of the swerve module motors to brake (Motors brake when not doing anything)
        m_motorDrive.SetIdleMode(rev.CANSparkMax.IdleMode.kBrake)
        m_motorTurn.SetIdleMode(rev.CANSparkMax.IdleMode.kBrake)

        # Sets current limits for the swerve module motors
        m_motorDrive.SetSmartCurrentLimit(80.0)
        m_motorTurn.SetSmartCurrentLimit(20.0)

        # Adds and sets the encoder offset to each swerve module encoder
        m_encoderTurn.ConfigMagnetOffset(m_encoderOffset)

        # Configurations and settings for the encoders
        m_encoderTurn.ConfigVelocityMeasurementPeriod(ctre.sensors.SensorVelocityMeasPeriod.Period_100Ms)
        m_encoderTurn.ConfigAbsoluteSensorRange(ctre.sensors.AbsoluteSensorRange.Signed_PlusMinus180)
        m_encoderTurn.ConfigSensorDirection(false)
        m_encoderTurn.ConfigSensorInitializationStrategy(ctre.sensors.SensorInitializationStrategy.BootToAbsolutePosition)
        m_encoderTurn.ConfigFeedbackCoefficient(360.0 / 4096.0, "deg", ctre.sensors.SensorTimeBase.PerSecond)

        # Sets the feedback device of the drive motor to the built in motor encoder and the feedback device of the turn motor to the external encoder
        m_driveController.SetFeedbackDevice(m_encoderDrive)
        m_turnController.SetFeedbackDevice(m_encoderTurnIntegrated)

        m_driveController.SetP(0.001)
        m_driveController.SetI(0)
        m_driveController.SetD(0)
        #m_driveController.SetFF(1/107.9101*2) #(0.5*1023.0)/(22100.0*0.5)
        m_driveController.SetFF(1/73.0)
        m_driveController.SetOutputRange(-1.0, 1.0)

        m_turnController.SetP(0.015) #0.55
        m_turnController.SetI(0.0)
        m_turnController.SetD(0.001) #0.3
        m_turnController.SetFF(0.0)
        m_turnController.SetOutputRange(-1.0, 1.0)

        # Velocity values for the external turn encoder and the built in drive encoder
        m_encoderTurnIntegrated.SetPositionConversionFactor(2.0 * 3.141592653589 * ((14.0 / 50.0) * (10.0 / 60.0)))
        m_encoderTurnIntegrated.SetVelocityConversionFactor((2.0 * 3.141592653589 * ((14.0 / 50.0) * (10.0 / 60.0))) / 60.0)

        m_encoderDrive.SetPositionConversionFactor(0.0508 * 2.0 * 3.141592653589 * ((14.0 / 50.0) * (25.0 / 19.0) * (15.0 / 45.0)))
        m_encoderDrive.SetVelocityConversionFactor(0.0508 * (2.0 * 3.141592653589 * ((14.0 / 50.0) * (25.0 / 19.0) * (15.0 / 45.0))) / 60.0)

def GetPosition():
    return [m_encoderDrive.GetPosition(), ((m_encoderTurn.GetAbsolutePosition()))]  