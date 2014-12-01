# Import the FSM functions
from fsm.functions import (
	createState, createFSM,
	addTransition, addStates,
	setInitialState, readWM, setPrintTransition)	

# Import primitive robot behaviors
from api.pubapi import (sit, stand, rest, say, shutdown, communicate, stopWalking,
                        resetSubFSM, setCamera, setLED, turnHead, setWalkVelocity)

# Import functions we've written
from functions import (closeToObstacle, closeToFeet, rotateTime, walkDelay,
                       obstacleToLeft, obstacleToRight, headDelay)
                       
# Import FSM
# Currently none

# Create state

#resetLookBallState = createState("resetLookBallState", lambda : resetSubFSM(lookBallFSM))

setBottomCamState = createState("setBottomCamState", lambda : setCamera("bottom"))
setBottomLedState = createState("setBottomLedState", lambda : setLED("eyes", 1.0, 0.0, 0.0)) # Red
setTopCamState = createState("setTopCamState", lambda : setCamera("top"))
setTopLedState = createState("setTopLedState", lambda : setLED("eyes", 0.0, 0.0, 1.0)) # Red
walkState = createState("walkState", lambda : setWalkVelocity(0.6, 0, 0))
walkState2 = createState("walkState2", lambda : setWalkVelocity(0.6, 0, 0))
rotateState = createState("rotateState", lambda : setWalkVelocity(0, 0, -0.4))
rotateState2 = createState("rotateState2", lambda : setWalkVelocity(0, 0, -0.4))
stopWalkState = createState("stopWalkState", stopWalking)
stopWalkState2 = createState("stopWalkState2", stopWalking)
leftHeadState = createState("leftHeadState", lambda: turnHead(0.5, 0.0549))
rightHeadState = createState("rightHeadState", lambda: turnHead(-0.5, 0.0549))
lookDownState = createState("lookDownState", lambda : turnHead(0, 0.0549)) #0.1149 ok
lookDownState2 = createState("lookDownState2", lambda : turnHead(0, 0.0549))
lookDownMoreState = createState("lookDownMoreState", lambda : turnHead(0, 0.2549))

# Add transitions

addTransition(setBottomCamState, lambda wm: True, setBottomLedState)
addTransition(setBottomLedState, lambda wm: True, lookDownState2)

addTransition(lookDownState2, lambda wm: True, walkState)

addTransition(walkState, closeToObstacle, rotateState)
addTransition(walkState, headDelay, rightHeadState)

addTransition(rightHeadState, closeToObstacle, rotateState)
addTransition(rightHeadState, headDelay, lookDownState)

addTransition(lookDownState, closeToObstacle, rotateState)
addTransition(lookDownState, headDelay, leftHeadState)

addTransition(leftHeadState, closeToObstacle, rotateState)
addTransition(leftHeadState, headDelay, lookDownState2)

addTransition(rotateState, rotateTime, stopWalkState)

addTransition(stopWalkState, closeToObstacle, rotateState)
addTransition(stopWalkState, lambda wm: True, lookDownMoreState) 
addTransition(lookDownMoreState, closeToObstacle, rotateState)
addTransition(lookDownMoreState, headDelay, lookDownState2)


#addTransition(lookDownState, closeToObstacle, rotateState)

#addTransition(walkState, obstacleToLeft, rotateState)
#addTransition(walkState, obstacleToRight, rotateState2)

#addTransition(rotateState2, rotateTime, stopWalkState2)

#addTransition(stopWalkState2, closeToObstacle, rotateState2)
#addTransition(stopWalkState2, lambda wm: True, walkState2)
#addTransition(walkState2, walkDelay, walkState)


# Create the FSM and add the states created above
walkObstacleFSM = createFSM("walkObstacleFSM")
addStates(walkObstacleFSM, setBottomCamState, setBottomLedState, setTopCamState, setTopLedState,
          walkState, walkState2, rotateState, rotateState2, lookDownState, lookDownState2, 
          stopWalkState, stopWalkState2, leftHeadState, rightHeadState, lookDownMoreState)

# Set the initial state to waitSittingState
setInitialState(walkObstacleFSM , setBottomCamState)

setPrintTransition(walkObstacleFSM, True)
