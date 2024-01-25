from modules.debugmsgs import debugMsg, successMsg, errorMsg # Colorfull messages that we can use
import yaml # Reads from '.yaml' files

# Import custom modules
try:
    from components.swervemodule import SwerveModule
    # Print debug message that all "swervemodule" modules were imported successfully
    successMsg('components.swervemodule: import SwerveModule')
except Exception as e: 
    # If imports fail, print an error message
    errorMsg('Cound not import components.swervemodule: SwerveModule:', e)

try:
    from components.drivetrain import SwerveDrive
    # Print debug message that all "drivetrain" modules were imported successfully
    successMsg('components.drivetrain: import SwerveDrive')
except Exception as e:
    # If imports fail, print an error message
    errorMsg('Cound not import components.drivetrain: SwerveDrive:', e)


# Import robot modules
try:
    import wpilib
    import wpilib.drive
    import wpimath
    import rev
    import magicbot
    import wpilib

    # Print debug message that all robot modules were imported successfully
    successMsg('Robot modules imported')

except Exception as e: 
    # If imports fail, print an error message
    errorMsg('Cound not import robot modules:', e)

# Get the data we need from the 'constants.yaml'
with open('constants.yaml', "r") as f:
    constants = yaml.safe_load(f)

# Set the values from 'constants.yaml' as global variables so they can be declared in python
globals().update(constants)
debugMsg(f'Hostname: {Hostname}')


# Create the robot class
class Robot(magicbot.MagicRobot):

    def createObjects(self):
        
        pass

    def teleopInit(self):
        '''Called when teleop starts; optional'''

    def teleopPeriodic(self):
        '''Called on each iteration of the control loop'''

if __name__ == '__main__':
    wpilib.run(Robot)
