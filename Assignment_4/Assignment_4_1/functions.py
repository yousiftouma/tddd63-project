# Import the FSM functions
from fsm.functions import (readWM)

# Import primitive robot behaviors
from api.pubapi import sit, stand, rest, say, shutdown, communicate

def detectTouch(wm):
    return readWM(wm, "tactile", "middle")

def waitForStand(wm):
    print(readWM(wm, "comms"))
    messages = readWM(wm, "comms")
    for key in  messages:
        if messages[key]["msg"] == "Stand":
            return True
    return False

def waitForSit(wm):
    print(readWM(wm, "comms"))
    messages = readWM(wm, "comms")
    for key in messages:
        if  messages[key]["msg"] == "Sit":
            return True
    return False

def entryTime(wm):
    return readWM(wm, "time", "entry")

def currentTime(wm):
    return readWM(wm, "time", "current")

def touchDelay(wm):
    return ((currentTime(wm) - entryTime(wm)) > 3) and readWM(wm, "tactile", "middle")
