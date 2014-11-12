# Import the FSM functions
from fsm.functions import (createState, createFSM, addTransition,
    addStates, setInitialState, readWM, writeWM, setPrintTransition)	

# Import primitive robot behaviors
from api.pubapi import (sit, stand, rest, say, shutdown,
    startWalking, turnHead, setCamera, resetSubFSM,
    say, setLED, setWalkVelocity, stopWalking)

# Import FSM
from lookBallFSM import (lookBallFSM)
from kickBallFSM import (kickBallFSM) 
from goToBallFSM import (goToBallFSM)
from findGoalFSM import (findGoalFSM)                        

# Import functions we've written
from functions import (detectTouch, seeBall, noSeeBall, closeToFeet, seeGoal)

# Create states

waitSittingState = createState("waitSittingState", lambda : None)
sitState = createState("sitState", sit)
restState = createState("restState", rest)
standState = createState("standState", stand)
shutdownState = createState("shutdownState",
				lambda : shutdown("Final state reached"))
stopWalkState = createState("stopWalkState", stopWalking)
stopWalkState2 = createState("stopWalkState2", stopWalking)
stopWalkState3 = createState("stopWalkState3", stopWalking)
stopWalkState4 = createState("stopWalkState4", stopWalking)
resetKickBallState = createState("resetKickBallState", lambda : resetSubFSM(kickBallFSM))
resetLookBallState = createState("resetLookBallState", lambda : resetSubFSM(lookBallFSM))
resetgoToBallState = createState("resetgoToBallState", lambda : resetSubFSM(goToBallFSM))
setBottomCameraState = createState("setBottomCameraState", lambda : setCamera("bottom"))
bottomLedState = createState("bottomLedState", lambda : setLED("eyes", 1, 0, 0)) # Red

# The main FSM

# Transitions for the mainFSM

addTransition(waitSittingState, detectTouch, standState)
addTransition(standState, lambda wm: True, lookBallFSM)
addTransition(lookBallFSM, seeBall, goToBallFSM)
addTransition(goToBallFSM, noSeeBall, resetgoToBallState)
addTransition(goToBallFSM, closeToFeet, stopWalkState3)
addTransition(stopWalkState3, lambda wm: True, findGoalFSM)
addTransition(findGoalFSM, seeGoal, stopWalkState4)
addTransition(stopWalkState4, lambda wm: True, setBottomCameraState)
addTransition(setBottomCameraState, lambda wm: True, bottomLedState)
addTransition(bottomLedState, seeBall, kickBallFSM)
addTransition(bottomLedState, noSeeBall, stopWalkState)

addTransition(resetgoToBallState, lambda wm: True, stopWalkState)
addTransition(stopWalkState, lambda wm: True, resetLookBallState)
addTransition(resetLookBallState, lambda wm: True, lookBallFSM)

addTransition(goToBallFSM, detectTouch, stopWalkState2)
addTransition(lookBallFSM, detectTouch, stopWalkState2)

addTransition(stopWalkState2, lambda wm: True, sitState)
addTransition(sitState, lambda wm: True, restState)
addTransition(restState, lambda wm: True, shutdownState)


mainFSM = createFSM("mainFSM")
addStates(mainFSM, waitSittingState, standState, sitState, goToBallFSM, findGoalFSM,
          restState, shutdownState, lookBallFSM, kickBallFSM, resetgoToBallState,
          stopWalkState, stopWalkState2, stopWalkState3, stopWalkState4,
          resetKickBallState, resetLookBallState, setBottomCameraState, bottomLedState)
          
setInitialState(mainFSM, waitSittingState)

# Prints all the completed transitions

setPrintTransition(mainFSM, True)

