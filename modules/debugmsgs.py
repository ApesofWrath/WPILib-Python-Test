# Colors yay
import os, sys, platform

# Variables
osName = platform.system()

# Functions for different output messages (they are colorfull so they are easy to spot)
def debugMsg(message):
    # Print message with different formatting based on operating system
    print('DEBUG: ' + str(message))

def successMsg(message):
    # Print message with different formatting based on operating system
    print('SUCCESS: ' + str(message))

def errorMsg(message, error):
    # Print message with different formatting based on operating system
    print('ERROR: ' + str(message) + '\n\n\t> ' + str(error))
    sys.exit(1)