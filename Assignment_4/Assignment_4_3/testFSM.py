# Import the FSM functions
from fsm.functions import (
	createState , createFSM ,
	addTransition , addStates ,
	setInitialState, readWM, setPrintTransition )	

# Import primitive robot behaviors
from api.pubapi import (sit, stand, rest, say, shutdown, communicate, stopWalking,
                        resetSubFSM, setCamera, setLED)

# Import functions we've written
from functions import (detectTouch, touchDelay, waitForSit, seeBall, noSeeBall, closeToFeet,
                       seeNao, oneKick, cameraDelay)

waitSittingState = createState("waitSittingState", lambda : None)
standState = createState("standState", stand)
sitState = createState("sitState", sit)
restState = createState("restState", rest)
shutdownState = createState("shutdownState",
				lambda : shutdown("Final state reached"))

addTransition(waitSittingState , detectTouch, standState)
addTransition(standState, seeNao, sitState)
addTransition(standState, touchDelay, sitState)
addTransition(sitState, lambda wm: True, restState)
addTransition(restState, lambda wm: True, shutdownState)

testFSM = createFSM("testFSM")
addStates(testFSM, standState, sitState, restState, shutdownState, waitSittingState)

setInitialState(testFSM, waitSittingState)

setPrintTransition(testFSM, True)
