import wpilib
import wpilib.drive
import wpimath
import rev
import magicbot

import magicbot
import wpilib
from components.swervemodule import SwerveModule

class Robot(magicbot.MagicRobot):

    def createObjects(self):
        
        pass

    def teleopInit(self):
        '''Called when teleop starts; optional'''

    def teleopPeriodic(self):
        '''Called on each iteration of the control loop'''

if __name__ == '__main__':
    wpilib.run(Robot)
