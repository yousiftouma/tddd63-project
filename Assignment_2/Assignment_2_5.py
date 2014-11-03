# Import the FSM functions
from fsm.functions import (createState, createFSM, addTransition,
    addStates, setInitialState, readWM, writeWM, setPrintTransition)	

# Import primitive robot behaviors
from api.pubapi import (sit, stand, rest, say, shutdown,
    startWalking, turnHead, setCamera,
    say, setLED, setWalkVelocity, stopWalking)

#import FSM
from lookBallFSM import *
from followBallFSM import *

# Functions to use world model

def detectTouch(wm):
    return readWM(wm, "tactile", "middle")

def seeBall(wm):
    camera_data_balls = readWM(wm, "balls")
    if largestBall(wm) == None:
        return False
    elif largestBall(wm)["pa"] >= 200:
        print(largestBall(wm)['camera'] , "SeeBall")
        return True
    else:
        return False

# Create states

waitSittingState = createState("waitSittingState", lambda : None)
sitState = createState("sitState", sit)
restState = createState("restState", rest)
standState = createState("standState", stand)
shutdownState = createState("shutdownState",
				lambda : shutdown("Final state reached"))

# The main FSM

# Transitions for the mainFSM

addTransition(waitSittingState, detectTouch, standState)
addTransition(standState, lambda wm: True, lookBallFSM)
addTransition(lookBallFSM, seeBall, followBallFSM)
addTransition(followBallFSM, noSeeBall, lookBallFSM)
addTransition(followBallFSM, detectTouch, sitState)
addTransition(lookBallFSM, detectTouch, sitState)
addTransition(sitState, lambda wm: True, restState)
addTransition(restState, lambda wm: True, shutdownState)

mainFSM = createFSM("mainFSM")
addStates(mainFSM, waitSittingState, standState, sitState,
          restState, shutdownState, lookBallFSM, followBallFSM)
          
setInitialState(mainFSM, waitSittingState)

# Prints all the completed transitions

setPrintTransition(mainFSM, True)
