# Colors yay
import colorama

# Functions for different output messages (they are colorfull so they are easy to spot)
def debugMsg(message):
    print(colorama.Style.BRIGHT + colorama.Fore.CYAN + ('DEBUG: ' + str(message)) + colorama.Fore.WHITE + colorama.Style.NORMAL)

def successMsg(message):
    print(colorama.Style.BRIGHT + colorama.Fore.GREEN + ('SUCCESS: ' + str(message)) + colorama.Fore.WHITE + colorama.Style.NORMAL)

def errorMsg(message):
    print(colorama.Style.BRIGHT + colorama.Fore.RED + ('ERROR: ' + str(message)) + colorama.Fore.WHITE + colorama.Style.NORMAL)