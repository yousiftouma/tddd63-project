# Import the FSM functions
from fsm.functions import (
	createState , createFSM ,
	addTransition , addStates ,
	setInitialState, readWM, setPrintTransition )	

# Import primitive robot behaviors
from api.pubapi import sit, stand, rest, say, shutdown, communicate, stopWalking

# Import functions we've written
from functions import (detectTouch, touchDelay, waitForSit, seeBall, noSeeBall, closeToFeet,
                       seeNao, oneKick)

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
 
# Create other states

stopWalkingState = createState("stopWalkingState", stopWalking)
stopWalkingState2 = createState("stopWalkingState2", stopWalking)
stopWalkingState3 = createState("stopWalkingState3", stopWalking)

waitSittingState = createState("waitSittingState", lambda : None)

resetLookBallState = createState("resetLookBallState", lambda : resetSubFSM(lookBallFSM))
resetgoToBallState = createState("resetgoToBallState", lambda : resetSubFSM(goToBallFSM))



# Create communcationsstates

robot = "goliath"

sendStandStatus = createState("sendStandStatus" , 
                               lambda: communicate(robot, "Stand"))

sendFindBallStatus = createState("sendFindBallStatus", 
                            lambda: communicate(robot, "Find ball"))



# States for talking



# Add transitions
addTransition(waitSittingState , detectTouch, sendStandStatus)

addTransition(sendStandStatus , lambda wm: True, standState)
addTransition(standState, lambda wm: True, lookBallFSM)

addTransition(lookBallFSM, seeBall, resetgoToBallState)
addTransition(resetgoToBallState, lambda wm: True, goToBallFSM)

addTransition(goToBallFSM, closeToFeet, stopWalkingState)
addTransition(goToBallFSM, noSeeBall, resetLookBallState)
addTransition(resetLookBallState, lambda wm: True, lookBallFSM)

addTransition(stopWalkingState, lambda wm: True, findNaoFSM)
addTransition(findNaoFSM, seeNao, stopWalkingState2)
addTransition(stopWalkingState2, lambda wm: True, kickBallFSM)
addTransition(kickBallFSM, oneKick, sendFindBallStatus)

addTransition(sendFindBallStatus, lambda wm: True, stopWalkingState3)
addTransition(stopWalkingState, waitForSit, sitState)

addTransition(sitState, lambda wm: True, restState)
addTransition(restState, lambda wm: True, shutdownState)


# Create the FSM and add the states created above
mainFSM = createFSM("mainFSM")
addStates(mainFSM , waitSittingState,
          sendStandStatus, sendFindBallStatus, resetLookBallState, resetgoToBallState,
          sitState, standState, lookBallFSM, goToBallFSM, findNaoFSM, kickBallFSM,
          restState, shutdownState, stopWalkingState, stopWalkingState2, stopWalkingState3)

# Set the initial state to waitSittingState
setInitialState(mainFSM , waitSittingState)

setPrintTransition(mainFSM, True)
