# Import the FSM functions
from fsm.functions import (
	createState, createFSM,
	addTransition, addStates,
	setInitialState, readWM, setPrintTransition)	

# Import primitive robot behaviors
from api.pubapi import (sit, stand, rest, say, shutdown, communicate, stopWalking,
                        resetSubFSM, setCamera, setLED, turnHead, setWalkVelocity)

# Import functions we've written
from functions import (closeToObstacle, closeToFeet, rotateTime, rotateTime2)
                       
# Import FSM
# Currently none

# Create state

#resetLookBallState = createState("resetLookBallState", lambda : resetSubFSM(lookBallFSM))

setBottomCamState = createState("setBottomCamState", lambda : setCamera("bottom"))
setBottomLedState = createState("setBottomLedState", lambda : setLED("eyes", 1.0, 0.0, 0.0)) # Red
walkState = createState("walkState", lambda : setWalkVelocity(0.6, 0, 0))
lookUpState = createState("lookDownState", lambda : turnHead(0,0.2149))#-0.3149)) 
rotateState = createState("rotateState", lambda : setWalkVelocity(0, 0, -0.4))
stopWalkState = createState("stopWalkState", stopWalking)

# Add transitions

addTransition(setBottomCamState, lambda wm: True, setBottomLedState)
addTransition(setBottomLedState, lambda wm: True, lookUpState)

addTransition(lookUpState, closeToObstacle, rotateState)
addTransition(lookUpState, lambda wm: True, walkState)

addTransition(walkState, closeToObstacle, rotateState)
addTransition(rotateState, rotateTime, stopWalkState)

addTransition(stopWalkState, closeToObstacle, rotateState)
addTransition(stopWalkState, lambda wm: True, walkState) 


# Create the FSM and add the states created above
walkObstacleFSM = createFSM("walkObstacleFSM")
addStates(walkObstacleFSM, setBottomCamState, setBottomLedState, walkState,
          rotateState, lookUpState, stopWalkState)

# Set the initial state to waitSittingState
setInitialState(walkObstacleFSM , setBottomCamState)

setPrintTransition(walkObstacleFSM, True)
