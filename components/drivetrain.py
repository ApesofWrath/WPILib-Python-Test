# Stuck? https://github.com/robotpy/examples/blob/main/SwerveBot/drivetrain.py
import wpimath.units
import wpimath.kinematics
from wpilib import TimedRobot

import navx

from .swervemodule import SwerveModule

from extras.debugmsgs import *

class seconds:
	'''
	# Does nothing, used for doumentation formatting
	'''

# Load constants from the json file
import json
with open('constants.json') as jsonf:
	constants = json.load(jsonf)
	jsonf.close()

class Drivetrain():
	'''
	# Drivetrain

	Class that controlls components of the drivetrain (anything that moves the robot forwards, backwards, and sideways)
	'''
	def __init__(self):
		# Setup the gyro
		try:
			self.navx = navx.AHRS.create_spi()
			self.zeroGyro()
		except Exception as e:
			errorMsg('Issue initializing NavX:',e,__file__) # We have to declare file since the global file 
														    # in drivetrain.py is overiding the global file in swervemodule.oy
			pass
		
		# Each member variable represents a 'swervemodule.SwerveModule()' object
		self.swerveFrontLeft = SwerveModule(
			constants['MOTOR_CONSTANTS']['MOTOR_DRIVE_FRONT_LEFT_ID'],
			constants['MOTOR_CONSTANTS']['MOTOR_TURN_FRONT_LEFT_ID'],
			constants['MOTOR_CONSTANTS']['ENCODER_TURN_FRONT_LEFT_ID'],
			(constants['OFFSETS']['FRONT_LEFT'], constants['OFFSETS']['FRONT_LEFT'])
		)
		
		self.swerveFrontRight = SwerveModule(
			constants['MOTOR_CONSTANTS']['MOTOR_DRIVE_FRONT_RIGHT_ID'],
			constants['MOTOR_CONSTANTS']['MOTOR_TURN_FRONT_RIGHT_ID'],
			constants['MOTOR_CONSTANTS']['ENCODER_TURN_FRONT_RIGHT_ID'],
			(constants['OFFSETS']['FRONT_RIGHT'], -constants['OFFSETS']['FRONT_RIGHT'])
		)

		self.swerveBackLeft = SwerveModule(
			constants['MOTOR_CONSTANTS']['MOTOR_DRIVE_REAR_LEFT_ID'],
			constants['MOTOR_CONSTANTS']['MOTOR_TURN_REAR_LEFT_ID'],
			constants['MOTOR_CONSTANTS']['ENCODER_TURN_REAR_LEFT_ID'],
			(constants['OFFSETS']['REAR_LEFT'], -constants['OFFSETS']['REAR_LEFT'])
		)
		
		self.swerveBackRight = SwerveModule(
			constants['MOTOR_CONSTANTS']['MOTOR_DRIVE_REAR_RIGHT_ID'],
			constants['MOTOR_CONSTANTS']['MOTOR_TURN_REAR_RIGHT_ID'],
			constants['MOTOR_CONSTANTS']['ENCODER_TURN_REAR_RIGHT_ID'],
			(constants['OFFSETS']['REAR_RIGHT'], -constants['OFFSETS']['REAR_RIGHT'])
		)
		
		self.kinematics = wpimath.kinematics.SwerveDrive4Kinematics(
            self.swerveFrontLeft.location,
            self.swerveFrontRight.location,
            self.swerveBackLeft.location,
            self.swerveBackRight.location,
        )

		self.odometry = wpimath.kinematics.SwerveDrive4Odometry(
            self.kinematics,
            self.navx.getRotation2d(),
            (
                self.swerveFrontLeft.getPosition(),
                self.swerveFrontRight.getPosition(),
                self.swerveBackLeft.getPosition(),
                self.swerveBackRight.getPosition(),
            ),
        )

	def zeroGyro(self):
		'''
		Re-calibrates the NavX gyroscope
		'''
		# Zero the NavX gyro
		try:
			self.navx.zeroYaw()
		except Exception as e:
			errorMsg('Issue calibrating NavX:',e,__file__)

	def updateOdometry(self):
		'''
		Updates the field relative position of the robot
		'''
		
		self.odometry.update(
            self.navx.getRotation2d(),
            (
                self.swerveFrontLeft.getPosition(),
                self.swerveFrontRight.getPosition(),
                self.swerveBackLeft.getPosition(),
                self.swerveBackRight.getPosition(),
            )
        )

	def drive(self, xSpeed: float, ySpeed: float, rotation: float, fieldRelative: bool, periodSeconds: seconds):
		'''
		Drives the robot based on the imput from the xbox controller
		'''
		swerveModuleStates = self.kinematics.toSwerveModuleStates(
            wpimath.kinematics.ChassisSpeeds.discretize(
                (
                    wpimath.kinematics.ChassisSpeeds.fromFieldRelativeSpeeds(
                        xSpeed, ySpeed, rotation, self.navx.getRotation2d()
                    )
					
                    if fieldRelative
                    else wpimath.kinematics.ChassisSpeeds(xSpeed, ySpeed, rotation)
                ),
                periodSeconds
            )
        )
		wpimath.kinematics.SwerveDrive4Kinematics.desaturateWheelSpeeds(
            swerveModuleStates, constants['CALCULATIONS']['MODULE_MAX_SPEED']
        )

		# Set the desired states to each swerve motor
		self.swerveFrontLeft.setDesiredState(swerveModuleStates[0])
		self.swerveFrontRight.setDesiredState(swerveModuleStates[1])
		self.swerveBackLeft.setDesiredState(swerveModuleStates[2])
		self.swerveBackRight.setDesiredState(swerveModuleStates[3])