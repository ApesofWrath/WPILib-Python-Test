# Terminal gui for configuring robot
# NOTE: Do not run on roboRio, for python configuration only
import json, subprocess, platform, os

# Load path to
if 'windows' in platform.platform():
    data_file = os.getcwd()+'\\constants'
else:
    data_file = os.getcwd()+'/constants'