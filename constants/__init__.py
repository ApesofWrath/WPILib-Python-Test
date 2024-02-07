# Robot constants
# TODO: Re-calculate/change values of constants to match new robot

HOSTNAME = 668 # Same number as in '.deploy_cfg'

# ControllerConstants
CONTROLLER_MAIN_ID = 0
CONTROLLER_AUX_ID = 1
CONTROLLER_RATE_LIMIT = 3 # Sorta like sensitivity

# DrivetrainConstants
MOTOR_DRIVE_FRONT_LEFT_ID = 2
MOTOR_TURN_FRONT_LEFT_ID = 6
ENCODER_TURN_FRONT_LEFT_ID = 8

MOTOR_DRIVE_FRONT_RIGHT_ID = 26
MOTOR_TURN_FRONT_RIGHT_ID = 4
ENCODER_TURN_FRONT_RIGHT_ID = 10 # (Old name: ENCODER_TURN_FRONT_LEFT_ID: 10)

MOTOR_DRIVE_REAR_LEFT_ID = 3
MOTOR_TURN_REAR_LEFT_ID = 7
ENCODER_TURN_REAR_LEFT_ID = 9

MOTOR_DRIVE_REAR_RIGHT_ID = 1
MOTOR_TURN_REAR_RIGHT_ID = 5
ENCODER_TURN_REAR_RIGHT_ID = 11

# Offsets
FRONT_RIGHT = -40.429
REAR_RIGHT = 66.181
FRONT_LEFT = -94.921
REAR_LEFT = -1.142

# Calculations
FINAL_DRIVE_RATIO = 2430 # 6.75 * 360 (degrees)
FINAL_TURN_RATIO = 0.0466666667 #(14.0 / 50.0) * (10.0 / 60.0)
WHEEL_CIRCUMFERENCE = 11.9380521 # pi * 3.8 (inches)

MODULE_MAX_SPEED = 16.3 # Feet Per Second
CHASSIS_MAX_SPEED = 16.3 # Why is this one even here (MODULE_MAX_SPEED = CHASSIS_MAX_SPEED ???)

MODULE_MAX_ANGULAR_VELOCITY = 12.5663706 # pi * 4 (radians per second)
MODULE_MAX_ANGULAR_ACCELERATION = 25.1327412 # pi * 8 (radians per second^2)

MOTOR_MAX_OUTPUT = 0.5
MOTOR_DEADBAND = 0.1