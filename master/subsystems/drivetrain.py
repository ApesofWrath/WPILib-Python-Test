import wpimath.units as units
import wpimath.kinematics as kinematics
import navx, wpilib
import subsystems.swervemodule as swervemodule # TODO: magicRobot pls 🥺
import constants

class drivetrain():
	def __init__(self): # Constructor, zeros the gyro for swervedrive
		self.navX = navx.AHRS(wpilib.SerialPort.Port)
		self.navX.ZeroYaw()
	
	def resetGyro(self): # Resets the gyro when function run
		self.navX.ZeroYaw()

	def setSpeed(speed): # origionally slowDown (.25) and normalSpeed (1)
		SLOWCONST = speed # TODO: punt this baby (to the high-level component)

	def swerveDrive(self, # Sets Desired States of the swerve modules for swervedrive
		xSpeed, # meters per second
		ySpeed, # meters per second
		zRot, # radians per second
		relative # boolean per second
	):
		drivetrainSpeed = kinematics.ChassisSpeeds(xSpeed, ySpeed, zRot) if not relative else kinematics.fromFieldRelativeSpeeds(xSpeed, ySpeed, zRot) # get a ChassisSpeeds object representing the speeds in the robot’s frame of reference, from ether relative or absoloute speeds
		moduleStates = kinematics.SwerveDrive4Kinematics.desaturateWheelSpeeds(kinematics.SwerveDrive4Kinematics.toSwerveModuleStates(drivetrainSpeed), units.feetToMeters(constants.DrivetrainConstants.Calculations.MODULE_MAX_SPEED)) # get the desired swerve module states (desaturated) from the drivetrainSpeed and swerve modules' max speed (converting from feet/sec to meters/sec)

		swerveModules = [swervemodule(constants.MOTOR_DRIVE_FRONT_LEFT_ID, constants.MOTOR_TURN_FRONT_LEFT_ID, constants.ENCODER_TURN_FRONT_LEFT_ID, constants.Offsets.FRONT_LEFT), swervemodule(constants.MOTOR_DRIVE_FRONT_RIGHT_ID, constants.MOTOR_TURN_FRONT_RIGHT_ID, constants.ENCODER_TURN_FRONT_RIGHT_ID, constants.Offsets.FRONT_RIGHT), swervemodule(constants.MOTOR_DRIVE_REAR_LEFT_ID, constants.MOTOR_TURN_REAR_LEFT_ID, constants.ENCODER_TURN_REAR_LEFT_ID, constants.Offsets.REAR_LEFT), swervemodule(constants.MOTOR_DRIVE_REAR_RIGHT_ID, constants.MOTOR_TURN_REAR_RIGHT_ID, constants.ENCODER_TURN_REAR_RIGHT_ID, constants.Offsets.REAR_RIGHT) ] # TODO: proper implamentation depends on using magicRobot. if i see this placeholder in prod someone will be killed
		
		for i in range(3): swerveModules[i].SetDesiredState(moduleStates[i]) # for every swerve module, apply the proper state (i lined it up right i prommy)

		# TODO: smartDashboard or perhaps an alternative