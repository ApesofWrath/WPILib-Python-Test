import wpimath.units as units
import wpimath.kinematics as kinematics
import navx, wpilib

class SwerveDrive():
	def __init__(self): # Constructor, zeros the gyro for swervedrive
		self.navX = navx.AHRS(wpilib.SerialPort.Port)
		self.navX.ZeroYaw()
		
		'''
		#TODO: Possibly define the variables below in __init__() instead of dedicating a whole method for it
		self.xSpeed = xSpeed, # meters per second
		self.ySpeed = ySpeed, # meters per second
		self.zRot = zRot, # radians per second
		self.relative = relative # boolean per second
		'''
	
	def resetGyro(self): # Resets the gyro when function run
		self.navX.ZeroYaw()

	def setSpeed(self, speed): # origionally slowDown (.25) and normalSpeed (1)
		SLOWCONST = speed # TODO: punt this baby (to the high-level component)

	def swerveDrive(self, # Sets Desired States of the swerve modules for swervedrive
		xSpeed, # meters per second
		ySpeed, # meters per second
		zRot, # radians per second
		relative, # boolean per second

		# Set the constants as arguments so we can have all constants stored in robot.py
		MOTOR_DRIVE_FRONT_LEFT_ID,
		MOTOR_TURN_FRONT_LEFT_ID,
		ENCODER_TURN_FRONT_LEFT_ID,
		OFFSETS_FRONT_LEFT,
		MOTOR_DRIVE_FRONT_RIGHT_ID,
		MOTOR_TURN_FRONT_RIGHT_ID,
		ENCODER_TURN_FRONT_RIGHT_ID,
		OFFSETS_FRONT_RIGHT,
		MOTOR_DRIVE_REAR_LEFT_ID,
		MOTOR_TURN_REAR_LEFT_ID,
		ENCODER_TURN_REAR_LEFT_ID,
		OFFSETS_REAR_LEFT,
		MOTOR_DRIVE_REAR_RIGHT_ID,
		MOTOR_TURN_REAR_RIGHT_ID,
		ENCODER_TURN_REAR_RIGHT_ID,
		OFFSETS_REAR_RIGHT,

		# Do the same for calculation arguments
		CALCULTIONS_MODULE_MAX_SPEED
	):
		# Get a ChassisSpeeds object representing the speeds in the robot’s frame of reference, 
		# from ether relative or absoloute speeds
		drivetrainSpeed = kinematics.ChassisSpeeds(xSpeed, ySpeed, zRot) if not relative else kinematics.fromFieldRelativeSpeeds(xSpeed, ySpeed, zRot)

		# Get the desired swerve module states (desaturated) from the drivetrainSpeed and swerve modules' max speed 
		# (converting from feet/sec to meters/sec)
		moduleStates = kinematics.SwerveDrive4Kinematics.desaturateWheelSpeeds(kinematics.SwerveDrive4Kinematics.toSwerveModuleStates(drivetrainSpeed), units.feetToMeters(CALCULTIONS_MODULE_MAX_SPEED)) 

		wpilib

		# TODO: Find out wtf 'swervemodule is' (Probably the 'SwerveModule" class in swervemodule.py)
		swerveModules = [swervemodule(MOTOR_DRIVE_FRONT_LEFT_ID, 
								MOTOR_TURN_FRONT_LEFT_ID, 
								ENCODER_TURN_FRONT_LEFT_ID, 
								OFFSETS_FRONT_LEFT), 

				   swervemodule(MOTOR_DRIVE_FRONT_RIGHT_ID, 
					MOTOR_TURN_FRONT_RIGHT_ID, 
					ENCODER_TURN_FRONT_RIGHT_ID, 
					OFFSETS_FRONT_RIGHT), 

				   swervemodule(MOTOR_DRIVE_REAR_LEFT_ID, 
					MOTOR_TURN_REAR_LEFT_ID, 
					ENCODER_TURN_REAR_LEFT_ID, 
					OFFSETS_REAR_LEFT), 

				   swervemodule(MOTOR_DRIVE_REAR_RIGHT_ID,
					MOTOR_TURN_REAR_RIGHT_ID,
					ENCODER_TURN_REAR_RIGHT_ID, 
					OFFSETS_REAR_RIGHT)]
		# TODO: proper implamentation depends on using magicRobot. 
		# if i see this placeholder in prod someone will be killed
		# Standin' on bidness! >:[]
		
		for i in range(3):
			# For every swerve module, apply the proper state (i lined it up right i prommy)
			swerveModules[i].SetDesiredState(moduleStates[i])
		# TODO: smartDashboard or perhaps an alternative