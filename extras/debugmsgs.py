# Colors yay
import os, sys, platform, traceback

scriptFile = None
def init(file):
    global scriptFile
    scriptFile = file

# Functions for different output messages (they are colorfull so they are easy to spot)
def debugMsg(message):
    # Print message with different formatting based on operating system
    print('DEBUG: ' + str(message))

def successMsg(message):
    # Print message with different formatting based on operating system
    print('SUCCESS: ' + str(message))

def errorMsg(message, error, optionalScriptFile=None):
    # Print message with different formatting based on operating system
    if optionalScriptFile != None:
        try:
            raise Exception('ERROR: ' 
                + str(message) + '\n\n\t' 
                + f'{optionalScriptFile}' + '\n\t> '+ 
                str(error) + f' -> [Line: {error.__traceback__.tb_lineno}]')
        except:
            raise Exception('ERROR: ' 
                + str(message)
            ) # Print bare minimum error
    else:
        try:
            raise Exception('ERROR: ' 
                + str(message) + '\n\n\t' 
                + f'{scriptFile}' + '\n\t> '+ 
                str(error) + f' -> [Line: {error.__traceback__.tb_lineno}]')
        except:
            raise Exception('ERROR: ' 
                + str(message)
            ) # Print bare minimum error