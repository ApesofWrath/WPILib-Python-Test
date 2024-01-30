# Colors yay
import platform
import colorama

# Get OS name
osName = platform.system()

# Functions for different output messages (they are colorfull so they are easy to spot)
def debugMsg(message):
    if 'windows' in osName.lower():
        print('DEBUG: ' + str(message))
    else:
        print(colorama.Style.BRIGHT + colorama.Fore.CYAN + ('DEBUG: ' + str(message)) + colorama.Fore.WHITE + colorama.Style.NORMAL)

def successMsg(message):
    if 'windows' in osName.lower():
        print('SUCCESS: ' + str(message))
    else:
        print(colorama.Style.BRIGHT + colorama.Fore.GREEN + ('SUCCESS: ' + str(message)) + colorama.Fore.WHITE + colorama.Style.NORMAL)

def errorMsg(message, error):
    if 'windows' in osName.lower():
        print('ERROR: ' + str(message) + '\n\n\t> ' + str(error))
    else:
        print(colorama.Style.BRIGHT + colorama.Fore.RED + ('ERROR: ' + str(message) + '\n\n\t> ' + str(error)) + colorama.Fore.WHITE + colorama.Style.NORMAL)