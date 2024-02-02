# Colors yay
import platform
import colorama
from . import logger

# Variables
osName = platform.system()

# Change the path to our log file based on OS
if 'windows' in osName.lower():
    logger = logger.Logger('.\\logs\\output.log')
else:
    logger = logger.Logger('./logs/output.log')

# Functions for different output messages (they are colorfull so they are easy to spot)
def debugMsg(message):
    # Log message to file
    logger.write('DEBUG: ' + str(message))

    # Print message with different formatting based on operating system
    if 'windows' in osName.lower():
        print('DEBUG: ' + str(message))
    else:
        print(colorama.Style.BRIGHT + colorama.Fore.CYAN + ('DEBUG: ' + str(message)) + colorama.Fore.WHITE + colorama.Style.NORMAL)

def successMsg(message):
    # Log message to file
    logger.write('SUCCESS: ' + str(message))

    # Print message with different formatting based on operating system
    if 'windows' in osName.lower():
        print('SUCCESS: ' + str(message))
    else:
        print(colorama.Style.BRIGHT + colorama.Fore.GREEN + ('SUCCESS: ' + str(message)) + colorama.Fore.WHITE + colorama.Style.NORMAL)

def errorMsg(message, error):
    # Log message to file
    logger.write('ERROR: ' + str(message) + '\n\n\t> ' + str(error))

    # Print message with different formatting based on operating system
    if 'windows' in osName.lower():
        print('ERROR: ' + str(message) + '\n\n\t> ' + str(error))
    else:
        print(colorama.Style.BRIGHT + colorama.Fore.RED + ('ERROR: ' + str(message) + '\n\n\t> ' + str(error)) + colorama.Fore.WHITE + colorama.Style.NORMAL)