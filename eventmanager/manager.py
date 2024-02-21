# Manages events in different stages of the robot
import json, subprocess, time

# Load constants from the json file
with open('constants.json') as jsonf:
    constants = json.load(jsonf)

class Event:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.availableMacros = []  # Specify which macros you want available

class Manager:
    def __init__(self):
        # Create a dictionary to store events with event names as keys
        self.events = {name: Event(name, value) for name, value in constants['EVENTS'].items()}

    def toggle(self, eventName):
        # Toggles an event while deactivating the rest
        for event in self.events.values():
            event.value = (event.name == eventName)

    def addMacrosToEvent(self, eventName, macroNames=[]):
        event = next((event for event in self.events.values() if event.name == eventName), None)
        event.availableMacros = macroNames

    def getEvent(self, eventName):
        # Get the event object by name from the dictionary
        return self.events.get(eventName, None)