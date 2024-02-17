# Stuck? https://github.com/robotpy/examples/blob/main/SwerveBot/drivetrain.py
import wpimath.units
import wpimath.kinematics

import navx

from extras.debugmsgs import *

from .swervemodule import SwerveModule

# Load constants from the json file
import json
with open('constants.json') as jsonf:
	constants = json.load(jsonf)
	jsonf.close()

class Drivetrain():
	def __init__(self):
		# Setup the gyro
		try:
			self.navx = navx.AHRS.create_spi()
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

		# Zero the NavX gyro
		try:
			self.navx.zeroYaw()
			successMsg('NavX calibrated')
		except Exception as e:
			errorMsg('Issue calibrating NavX:',e,__file__)

	def updateOdometry(self):
		# Updates the field relative position of the robot
		self.odometry.update(
            self.navx.getRotation2d(),
            (
                self.swerveFrontLeft.getPosition(),
                self.swerveFrontRight.getPosition(),
                self.swerveBackLeft.getPosition(),
                self.swerveBackRight.getPosition(),
            ),
        )

	# Drives the robot based on the imput from the xbox controller
	def drive(self, xSpeed, ySpeed, rot, fieldRelative, periodSeconds):
		swerveModuleStates = self.kinematics.toSwerveModuleStates(
            wpimath.kinematics.ChassisSpeeds.discretize(
                (
                    wpimath.kinematics.ChassisSpeeds.fromFieldRelativeSpeeds(
                        xSpeed, ySpeed, rot, self.navx.getRotation2d()
                    )
                    if fieldRelative
                    else wpimath.kinematics.ChassisSpeeds(xSpeed, ySpeed, rot)
                ),
                periodSeconds,
            )
        )
		wpimath.kinematics.SwerveDrive4Kinematics.desaturateWheelSpeeds(
            swerveModuleStates, constants['CALCULATIONS']['MODULE_MAX_SPEED']
        )
		self.swerveFrontLeft.setDesiredState(swerveModuleStates[0])
		self.swerveFrontRight.setDesiredState(swerveModuleStates[1])
		self.swerveBackLeft.setDesiredState(swerveModuleStates[2])
		self.swerveBackRight.setDesiredState(swerveModuleStates[3])