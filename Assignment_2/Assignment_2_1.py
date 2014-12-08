from math import pi

# Import the FSM functions
from fsm.functions import (
	createState, createFSM,
	addTransition, addStates,
	setInitialState, readWM, writeWM, setPrintTransition)	

# Import primitive robot behaviors
from api.pubapi import (sit, stand, rest, say, shutdown,
    startWalking, stopWalking, setWalkVelocity)

# Define the functions for world model

def detectTouch(wm):
    return readWM(wm, "tactile", "middle")

# Adjusts the walking time of the robot

def entryTime(wm):
    return readWM(wm, "time", "entry")

def currentTime(wm):
    return readWM(wm, "time", "current")

def walkTime(wm):
    if currentTime(wm) - entryTime(wm) >= 13:
        return True
    else:
        return False

def rotateTime(wm):
    if currentTime(wm) - entryTime(wm) >= 5:
        return True
    else:
        return False

def uTurnTime(wm):
    if currentTime(wm) - entryTime(wm) >= 17:
        return True
    else:
        return False
   

## CREATE STATES ##

sitState = createState("sitState", sit)
standState = createState("standState", stand)
restState = createState("restState", rest)
walkState = createState("walkState", startWalking)
stopWalkState = createState("stopWalkState", stopWalking)
stopWalk2State = createState("stopWalk2State", stopWalking)
rotateState = createState("rotateState", lambda: setWalkVelocity(0, 0, 0.5))
uTurnState = createState("uTurnState", lambda: setWalkVelocity(1, 0, 0.2))
shutdownState = createState("shutdownState",
				lambda: shutdown("Final state reached"))


# Create states for talking

sayLetsWalkState = createState("sayLetsWalkState", lambda: say("Hej Yousif!"))
sayRotateState = createState("sayRotateState", lambda: say("spinn!"))
sayUTurnState = createState("sayUTurnState", lambda: say("u turn!"))
sayGoodbyeState = createState("sayGoodbyeState", lambda: say("Goodbye World!"))

 
# Create states for waiting for touch

waitSittingState = createState("waitSittingState", lambda: None)
waitStandingState = createState("waitStandingState", lambda: None)

# Create states for function calls


# Add transitions according to the state diagram
addTransition(waitSittingState, detectTouch, standState)
addTransition(standState, lambda wm: True, sayLetsWalkState)
addTransition(sayLetsWalkState, lambda wm: True, walkState)
addTransition(walkState, walkTime, stopWalkState)
addTransition(stopWalkState, lambda wm: True, rotateState)
addTransition(rotateState, rotateTime, uTurnState)
addTransition(uTurnState, uTurnTime, stopWalk2State)
addTransition(stopWalk2State, lambda wm: True, sitState)
addTransition(sitState, lambda wm: True, restState)
addTransition(restState, lambda wm: True, shutdownState)

# Create the FSM and add the states created above
myFSM = createFSM("fsm")
addStates(myFSM, waitSittingState, waitStandingState,  standState, 
          sayLetsWalkState, sayGoodbyeState, sitState, restState,
          shutdownState, walkState, stopWalkState, rotateState, 
          uTurnState, sayRotateState, sayUTurnState, 
          stopWalk2State)
 
setPrintTransition(myFSM, True)

# Set the initial state to waitSittingState
setInitialState(myFSM, waitSittingState)


