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
    if current_position(wm) < 0:
        current_angle = current_position(wm) + 2*pi
    else:
        current_angle = current_position(wm)
    if readWM(wm, "start_angle") < 0:
        angle = readWM(wm, "start_angle") + 2 * pi
    else:
        angle = readWM(wm, "start_angle")
    if abs(angle - current_angle) >=  pi/2 - 0.1:
        return True
    else:
        return False

def uTurn(wm):
    if current_position(wm) < 0:
        current_angle = current_position(wm) + 2*pi
    else:
        current_angle = current_position(wm)
    if readWM(wm, "start_angle") < 0:
        angle = readWM(wm, "start_angle") + 2 * pi
    else:
        angle = readWM(wm, "start_angle")
    print(readWM(wm,"start_angle"), current_position(wm), abs(angle - current_angle), pi)
    if abs(angle - current_angle) >=  pi :
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
stopWalk3State = createState("stopWalk3State", stopWalking)
rotate90State = createState("rotate90State", lambda : setWalkVelocity(0, 0, 0.2))
uTurnState = createState("uTurnState", lambda : setWalkVelocity(1, 0, 0.3))
shutdownState = createState("shutdownState",
				lambda : shutdown("Final state reached"))
#stopRotateState = createState

# Create states for talking

sayLetsWalkState = createState("sayLetsWalkState", lambda : say("go!"))
sayRotateState = createState("sayRotateState", lambda : say("spinn!"))
sayUTurnState = createState("sayUTurnState", lambda : say("u turn!"))
sayGoodbyeState = createState("sayGoodbyeState", lambda : say("Goodbye World!"))

 
# Create states for waiting for touch

waitSittingState = createState("waitSittingState", lambda : None)
waitStandingState = createState("waitStandingState", lambda : None)

# Create states for function calls

startAngleState = createState("startAngleState", lambda wm : start_position(wm))
startAngle2State = createState("startAngle2State", lambda wm : start_position(wm))


# Add transitions according to the state diagram
addTransition(waitSittingState , detectTouch , standState)
addTransition(standState , lambda wm: True , sayLetsWalkState)
addTransition(sayLetsWalkState, lambda wm: True , walkState)
addTransition(walkState , walkTime , stopWalkState)
addTransition(stopWalkState, lambda wm: True , sayRotateState)
addTransition(sayRotateState, lambda wm: True , startAngleState)
addTransition(startAngleState, lambda wm: True , rotate90State)
addTransition(rotate90State, rotate , stopWalk2State)
addTransition(stopWalk2State, lambda wm: True , startAngle2State)
addTransition(startAngle2State, lambda wm: True , uTurnState)
addTransition(uTurnState, uTurn , stopWalk3State)
addTransition(stopWalk3State, lambda wm: True, sitState)
addTransition(sitState , lambda wm: True , restState)
addTransition(restState , lambda wm: True , shutdownState)

# Create the FSM and add the states created above
myFSM = createFSM("fsm")
addStates(myFSM , waitSittingState , waitStandingState ,  standState , 
          sayLetsWalkState , sayGoodbyeState , sitState , restState ,
          shutdownState , walkState , stopWalkState, rotate90State , 
          uTurnState , sayRotateState, sayUTurnState, startAngleState,
          startAngle2State, stopWalk2State, stopWalk3State)
 
setPrintTransition(myFSM, True)

# Set the initial state to waitSittingState
setInitialState(myFSM , waitSittingState)


