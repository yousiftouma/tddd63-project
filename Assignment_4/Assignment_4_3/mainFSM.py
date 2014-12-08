# Import the FSM functions
from fsm.functions import (
	createState, createFSM,
	addTransition, addStates,
	setInitialState, readWM, setPrintTransition)	

# Import primitive robot behaviors
from api.pubapi import (sit, stand, rest, say, shutdown, communicate, stopWalking,
                        resetSubFSM, setCamera, setLED, turnHead)

# Import functions we've written
from functions import (detectTouch, touchDelay, waitForSit, seeBall, noSeeBall, closeToFeet,
                       seeNao, oneKick, cameraDelay)

# Import FSM

from lookBallFSM import (lookBallFSM)
from goToBallFSM import (goToBallFSM)
from findNaoFSM import (findNaoFSM)
from kickBallFSM import (kickBallFSM)

## CREATE STATES ##


standState = createState("standState", stand)
sitState = createState("sitState", sit)
restState = createState("restState", rest)
shutdownState = createState("shutdownState",
				lambda : shutdown("Final state reached"))
stopWalkingState = createState("stopWalkingState", stopWalking)
stopWalkingState2 = createState("stopWalkingState2", stopWalking)
stopWalkingState3 = createState("stopWalkingState3", stopWalking)
stopWalkingState4 = createState("stopWalkingState4", stopWalking)
waitSittingState = createState("waitSittingState", lambda: None)
resetLookBallState = createState("resetLookBallState", lambda: resetSubFSM(lookBallFSM))
resetgoToBallState = createState("resetgoToBallState", lambda: resetSubFSM(goToBallFSM))
resetFindNaoState = createState("resetFindNaoState", lambda: resetSubFSM(findNaoFSM))
setBottomCamState = createState("setBottomCamState", lambda: setCamera("bottom"))
setBottomLedState = createState("setBottomLedState", lambda: setLED("eyes", 1.0, 0.0, 0.0)) # Red
setTopCamState = createState("setTopCamState", lambda: setCamera("top"))
setTopLedState = createState("setTopLedState", lambda: setLED("eyes", 0.0, 1.0, 0.0)) # Green
lookDownState = createState("lookDownState", lambda: turnHead(0,0.3149))

# Create communcationsstates

robot = "piff"

sendStandStatus = createState("sendStandStatus" , 
                               lambda: communicate(robot, "Stand"))

sendFindBallStatus = createState("sendFindBallStatus", 
                            lambda: communicate(robot, "Find ball"))

# Add transitions

addTransition(waitSittingState , detectTouch, sendStandStatus)

addTransition(sendStandStatus , lambda wm: True, standState)
addTransition(standState, lambda wm: True, lookBallFSM)

addTransition(lookBallFSM, seeBall, resetgoToBallState)
addTransition(resetgoToBallState, lambda wm: True, goToBallFSM)

addTransition(goToBallFSM, noSeeBall, resetLookBallState) 
addTransition(goToBallFSM, closeToFeet, stopWalkingState)

addTransition(stopWalkingState, lambda wm: True, resetFindNaoState)
addTransition(resetFindNaoState, lambda wm: True, findNaoFSM)
addTransition(findNaoFSM, seeNao, stopWalkingState2)

addTransition(stopWalkingState2, lambda wm: True, setBottomCamState)
addTransition(setBottomCamState, lambda wm: True, setBottomLedState)
addTransition(setBottomLedState, lambda wm: True, lookDownState)

addTransition(lookDownState, seeBall, kickBallFSM)
addTransition(lookDownState, noSeeBall, stopWalkingState3)

addTransition(stopWalkingState3, lambda wm: True, resetLookBallState)
addTransition(resetLookBallState, lambda wm: True, lookBallFSM)

addTransition(kickBallFSM, oneKick, sendFindBallStatus)

addTransition(sendFindBallStatus, lambda wm: True, stopWalkingState4)
addTransition(stopWalkingState4, waitForSit, sitState)

addTransition(sitState, lambda wm: True, restState)
addTransition(restState, lambda wm: True, shutdownState)

# Create the FSM and add the states created above
mainFSM = createFSM("mainFSM")
addStates(mainFSM, waitSittingState, setBottomCamState, setBottomLedState,
          sendStandStatus, sendFindBallStatus, resetLookBallState, resetgoToBallState, resetFindNaoState,
          sitState, standState, lookBallFSM, goToBallFSM, findNaoFSM, kickBallFSM,
          restState, shutdownState, stopWalkingState, stopWalkingState2, stopWalkingState3, 
          stopWalkingState4, setTopCamState, setTopLedState, lookDownState)

# Set the initial state to waitSittingState
setInitialState(mainFSM, waitSittingState)

setPrintTransition(mainFSM, True)
