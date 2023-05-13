import ctre.sensors
import rev
from constants import DrivetrainConstants
import wpimath.kinematics
class SwerveModule:
    def __init__(self, drive_motor_id, turn_motor_id, encoder_id, offset):
        
        # Set attributes
        self.target_angle = 0

        # Initialize Motor and Encoder Objects (Note: turn_encoder is the absolute encoder located on the top of the swerve drive, the other encoders are for the motors themselves)
        self.drive_motor = rev.CANSparkMax(drive_motor_id, rev.CANSparkMax.MotorType.kBrushless)
        self.turn_motor = rev.CANSparkMax(turn_motor_id, rev.CANSparkMax.MotorType.kBrushless)
        self.turn_encoder = ctre.sensors.WPI_CANCoder(encoder_id, )
        self.drive_motor_encoder = self.drive_motor.getEncoder(rev.SparkMaxRelativeEncoder.Type.kHallSensor)
        self.turn_motor_encoder = self.turn_motor.getEncoder(rev.SparkMaxRelativeEncoder.Type.kHallSensor)

        # Initialize the PID Controllers
        self.drive_motor_pid_controller = self.drive_motor.getPIDController()
        self.turn_motor_pid_controller = self.turn_motor.getPIDController()
        # Resets the swerve module motors and encoders to factory settings
        self.drive_motor.restoreFactoryDefaults()
        self.turn_motor.restoreFactoryDefaults()
        self.turn_encoder.configFactoryDefault()

        # Sets both the drive motor and the turn motor to be inverted
        self.drive_motor.setInverted(True)
        self.turn_motor.setInverted(True)

        # Sets the idle mode of the swerve module motors to brake (Motors brake when not doing anything)
        self.drive_motor.setIdleMode(rev.CANSparkMax.IdleMode.kBrake)
        self.turn_motor.setIdleMode(rev.CANSparkMax.IdleMode.kBrake)

        # Sets current limits for the swerve module motors
        self.drive_motor.setSmartCurrentLimit(80.0)
        self.turn_motor.setSmartCurrentLimit(20.0)

        # Adds and sets the encoder offset to each swerve module encoder
        self.turn_encoder.configMagnetOffset(offset)

        # Configurations and settings for the encoders
        self.turn_encoder.configVelocityMeasurementPeriod(ctre.sensors.SensorVelocityMeasPeriod.Period_100Ms)
        self.turn_encoder.configAbsoluteSensorRange(ctre.sensors.AbsoluteSensorRange.Signed_PlusMinus180)
        self.turn_encoder.configSensorDirection(False)
        self.turn_encoder.configSensorInitializationStrategy(ctre.sensors.SensorInitializationStrategy.BootToAbsolutePosition)
        self.turn_encoder.configFeedbackCoefficient(360.0 / 4096.0, "deg", ctre.sensors.SensorTimeBase.PerSecond)

        # Sets the feedback device of the drive motor to the built in motor encoder and the feedback device of the turn motor to the external encoder
        self.drive_motor_pid_controller.setFeedbackDevice(m_encoderDrive)
        self.turn_motor_pid_controller.setFeedbackDevice(self.turn_motor_encoder)

        self.drive_motor_pid_controller.setP(0.001)
        self.drive_motor_pid_controller.setI(0)
        self.drive_motor_pid_controller.setD(0)
        #self.drive_motor_pid_controller.SetFF(1/107.9101*2) #(0.5*1023.0)/(22100.0*0.5)
        self.drive_motor_pid_controller.setFF(1/73.0)
        self.drive_motor_pid_controller.setOutputRange(-1.0, 1.0)

        self.turn_motor_pid_controller.setP(0.015) #0.55
        self.turn_motor_pid_controller.setI(0.0)
        self.turn_motor_pid_controller.setD(0.001) #0.3
        self.turn_motor_pid_controller.setFF(0.0)
        self.turn_motor_pid_controller.setOutputRange(-1.0, 1.0)

        # Velocity values for the external turn encoder and the built in drive encoder
        self.turn_motor_encoder.setPositionConversionFactor(2.0 * 3.141592653589 * ((14.0 / 50.0) * (10.0 / 60.0)))
        self.turn_motor_encoder.setVelocityConversionFactor((2.0 * 3.141592653589 * ((14.0 / 50.0) * (10.0 / 60.0))) / 60.0)

        self.drive_motor_encoder.setPositionConversionFactor(0.0508 * 2.0 * 3.141592653589 * ((14.0 / 50.0) * (25.0 / 19.0) * (15.0 / 45.0)))
        self.drive_motor_encoder.setVelocityConversionFactor(0.0508 * (2.0 * 3.141592653589 * ((14.0 / 50.0) * (25.0 / 19.0) * (15.0 / 45.0))) / 60.0)
        self.drive_motor_encoder.getP
def GetPosition(self):
    return wpimath.kinematics.SwerveModulePosition(self.drive_motor_encoder.getPosition(), self.turn_encoder.getAbsolutePosition())  
def SetDesiredState(self, refenceState):
    referenceState = referenceState.optimize
    targetWheelSpeed = state.speed
    m_targetAngle = state.angle.Degrees().value()
    turnOutput = m_targetAngle
    targetMotorSpeed = [(targetWheelSpeed *2*3.14159) / DrivetrainConstants.Calculations.kWheelCircumference]