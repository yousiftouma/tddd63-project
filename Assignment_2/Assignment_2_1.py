from math import pi

# Import the FSM functions
from fsm.functions import (
	createState , createFSM ,
	addTransition , addStates ,
	setInitialState, readWM, writeWM, setPrintTransition )		# setMainFSM should be there

# Import primitive robot behaviors
from api.pubapi import sit, stand , rest, say , shutdown ,\
    startWalking , stopWalking , setWalkVelocity

# Define the functions for world model

def detectTouch(wm):
    return readWM(wm, "tactile", "middle")

# Adjusts the walking time of the robot

def entryTime(wm):
    return readWM(wm, "time", "entry")

def currentTime(wm):
    return readWM(wm, "time", "current")

def walkTime(wm):
    if currentTime(wm) - entryTime(wm) >= 10:
        return True
    else:
        return False

def start_position(wm):
    writeWM(wm, current_position(wm), "start_angle") 

def current_position(wm):
    return readWM(wm, "odometry", "wz")

def rotate(wm):
    start_position(wm)
   # print(readWM(wm, "start_angle"))
    if readWM(wm, "start_angle") + current_position(wm) >=readWM(wm, "start_angle") + 0.25:
        return True
    else:
        return False

def uTurn(wm):
    start_position(wm)
    if start_angle + current_position(wm) >= start_angle + 0.5:
        return True
    else:
        return False

## CREATE STATES ##

sitState = createState("sitState", sit)
standState = createState("standState", stand)
restState = createState("restState", rest)
walkState = createState("walkState", startWalking)
stopWalkState = createState("stopWalkState", stopWalking)
rotate90State = createState("rotate90State", lambda : setWalkVelocity(0, 0, 1))
uTurnState = createState("uTurnState", lambda : setWalkVelocity(1, 0, 1))
shutdownState = createState("shutdownState",
				lambda : shutdown("Final state reached"))

# Create states for talking

sayLetsWalkState = createState("sayLetsWalkState", lambda : say("Let us waaalk!"))
sayRotateState = createState("sayRotateState", lambda : say("Let us spinn!"))
sayUTurnState = createState("sayUTurnState", lambda : say("Let us walk in an arch!"))
sayGoodbyeState = createState("sayGoodbyeState", lambda : say("Goodbye World!"))

 
# Create states for waiting for touch

waitSittingState = createState("waitSittingState", lambda : None)
waitStandingState = createState("waitStandingState", lambda : None)

# Add transitions according to the state diagram
#addTransition(waitSittingState , detectTouch , standState)
addTransition(standState , lambda wm: True , sayLetsWalkState)
addTransition(sayLetsWalkState, lambda wm: True , walkState)
addTransition(walkState , walkTime , stopWalkState)
addTransition(stopWalkState, lambda wm: True , sayRotateState)
addTransition(sayRotateState, lambda wm: True , rotate90State)
addTransition(rotate90State, rotate , sayUTurnState)
addTransition(sayUTurnState, lambda wm: True , uTurnState)
addTransition(uTurnState, uTurn , stopWalkState)
addTransition(stopWalkState, lambda wm: True , sayGoodbyeState)
addTransition(sayGoodbyeState , lambda wm: True , sitState)
addTransition(sitState , lambda wm: True , restState)
addTransition(restState , lambda wm: True , shutdownState)

# Create the FSM and add the states created above
myFSM = createFSM("fsm")
addStates(myFSM , waitSittingState , waitStandingState ,  standState , 
          sayLetsWalkState , sayGoodbyeState , sitState , restState ,
          shutdownState , walkState , stopWalkState, rotate90State , 
          uTurnState , sayRotateState, sayUTurnState)
 
setPrintTransition(myFSM, True)

# Set the initial state to waitSittingState
setInitialState(myFSM , standState)


