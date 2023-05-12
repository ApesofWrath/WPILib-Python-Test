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
        self.drive_motor.RestoreFactoryDefaults()
        self.turn_motor.RestoreFactoryDefaults()
        self.turn_encoder.ConfigFactoryDefault()


        # Sets both the drive motor and the turn motor to be inverted
        self.drive_motor.SetInverted(True)
        self.turn_motor.SetInverted(True)

        # Sets the idle mode of the swerve module motors to brake (Motors brake when not doing anything)
        self.drive_motor.SetIdleMode(rev.CANSparkMax.IdleMode.kBrake)
        self.turn_motor.SetIdleMode(rev.CANSparkMax.IdleMode.kBrake)

        # Sets current limits for the swerve module motors
        self.drive_motor.SetSmartCurrentLimit(80.0)
        self.turn_motor.SetSmartCurrentLimit(20.0)

        # Adds and sets the encoder offset to each swerve module encoder
        self.turn_encoder.ConfigMagnetOffset(offset)

        # Configurations and settings for the encoders
        self.turn_encoder.ConfigVelocityMeasurementPeriod(ctre.sensors.SensorVelocityMeasPeriod.Period_100Ms)
        self.turn_encoder.ConfigAbsoluteSensorRange(ctre.sensors.AbsoluteSensorRange.Signed_PlusMinus180)
        self.turn_encoder.ConfigSensorDirection(False)
        self.turn_encoder.ConfigSensorInitializationStrategy(ctre.sensors.SensorInitializationStrategy.BootToAbsolutePosition)
        self.turn_encoder.ConfigFeedbackCoefficient(360.0 / 4096.0, "deg", ctre.sensors.SensorTimeBase.PerSecond)

        # Sets the feedback device of the drive motor to the built in motor encoder and the feedback device of the turn motor to the external encoder
        self.drive_motor_pid_controller.SetFeedbackDevice(m_encoderDrive)
        self.turn_motor_pid_controller.SetFeedbackDevice(self.turn_motor_encoder)

        self.drive_motor_pid_controller.SetP(0.001)
        self.drive_motor_pid_controller.SetI(0)
        self.drive_motor_pid_controller.SetD(0)
        #self.drive_motor_pid_controller.SetFF(1/107.9101*2) #(0.5*1023.0)/(22100.0*0.5)
        self.drive_motor_pid_controller.SetFF(1/73.0)
        self.drive_motor_pid_controller.SetOutputRange(-1.0, 1.0)

        self.turn_motor_pid_controller.SetP(0.015) #0.55
        self.turn_motor_pid_controller.SetI(0.0)
        self.turn_motor_pid_controller.SetD(0.001) #0.3
        self.turn_motor_pid_controller.SetFF(0.0)
        self.turn_motor_pid_controller.SetOutputRange(-1.0, 1.0)

        # Velocity values for the external turn encoder and the built in drive encoder
        self.turn_motor_encoder.SetPositionConversionFactor(2.0 * 3.141592653589 * ((14.0 / 50.0) * (10.0 / 60.0)))
        self.turn_motor_encoder.SetVelocityConversionFactor((2.0 * 3.141592653589 * ((14.0 / 50.0) * (10.0 / 60.0))) / 60.0)

        self.drive_motor_encoder.SetPositionConversionFactor(0.0508 * 2.0 * 3.141592653589 * ((14.0 / 50.0) * (25.0 / 19.0) * (15.0 / 45.0)))
        self.drive_motor_encoder.SetVelocityConversionFactor(0.0508 * (2.0 * 3.141592653589 * ((14.0 / 50.0) * (25.0 / 19.0) * (15.0 / 45.0))) / 60.0)

def GetPosition(self):
    return wpimath.kinematics.SwerveModulePosition(self.drive_motor_encoder.GetPosition(), self.turn_encoder.GetAbsolutePosition())  

def SetDesiredState(self, refenceState):
    referenceState = referenceState.optimize
    targetWheelSpeed = state.speed
    m_targetAngle = state.angle.Degrees().value()
    turnOutput = m_targetAngle
    targetMotorSpeed = [(targetWheelSpeed *2*3.14159) / DrivetrainConstants.Calculations.kWheelCircumference]