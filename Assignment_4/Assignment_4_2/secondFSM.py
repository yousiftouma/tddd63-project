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
                        

# Import functions we've written
from functions import (detectTouch, seeBall, noSeeBall, closeToFeet, seeGoal, oneKick,
                       waitForSit, waitForStand, waitForKick)

# Create states

waitSittingState = createState("waitSittingState", lambda: None)
sitState = createState("sitState", sit)
restState = createState("restState", rest)
standState = createState("standState", stand)
shutdownState = createState("shutdownState",
				lambda: shutdown("Final state reached"))
stopWalkState = createState("stopWalkState", stopWalking)
stopWalkState2 = createState("stopWalkState2", stopWalking)
stopWalkState3 = createState("stopWalkState3", stopWalking)
stopWalkState4 = createState("stopWalkState4", stopWalking)
resetKickBallState = createState("resetKickBallState", lambda: resetSubFSM(kickBallFSM))
resetLookBallState = createState("resetLookBallState", lambda: resetSubFSM(lookBallFSM))
resetgoToBallState = createState("resetgoToBallState", lambda: resetSubFSM(goToBallFSM))
resetFindGoalState = createState("resetFindGoalState", lambda: resetSubFSM(findGoalFSM))
setBottomCameraState = createState("setBottomCameraState", lambda: setCamera("bottom"))
bottomLedState = createState("bottomLedState", lambda: setLED("eyes", 1, 0, 0)) # Red
lookDownState = createState("lookDownState", lambda: turnHead(0,0.3149))

# The main FSM

# Transitions for the mainFSM

addTransition(waitSittingState, waitForStand, standState)
addTransition(standState, lambda wm: True, lookBallFSM)
addTransition(lookBallFSM, seeBall, resetgoToBallState)
addTransition(resetgoToBallState, lambda wm: True, goToBallFSM)
addTransition(goToBallFSM, noSeeBall, resetgoToBallState)
addTransition(goToBallFSM, closeToFeet, stopWalkState3)
addTransition(stopWalkState3, waitForKick, lookDownState)

addTransition(lookDownState, seeBall, kickBallFSM)
addTransition(lookDownState, noSeeBall, stopWalkState)

addTransition(kickBallFSM, oneKick, stopWalkState4)
addTransition(stopWalkState4, waitForSit, sitState)

addTransition(goToBallFSM, detectTouch, stopWalkState2)
addTransition(lookBallFSM, detectTouch, stopWalkState2)
addTransition(kickBallFSM, detectTouch, stopWalkState2)

addTransition(stopWalkState2, lambda wm: True, sitState)
addTransition(sitState, lambda wm: True, restState)
addTransition(restState, lambda wm: True, shutdownState)


secondFSM = createFSM("secondFSM")
addStates(secondFSM, waitSittingState, standState, sitState, goToBallFSM,
          restState, shutdownState, lookBallFSM, kickBallFSM, resetgoToBallState,
          stopWalkState, stopWalkState2, stopWalkState3, stopWalkState4,
          resetKickBallState, resetLookBallState, setBottomCameraState, bottomLedState,
          lookDownState, resetFindGoalState)
          
setInitialState(secondFSM, waitSittingState)

# Prints all the completed transitions

setPrintTransition(secondFSM, True)
