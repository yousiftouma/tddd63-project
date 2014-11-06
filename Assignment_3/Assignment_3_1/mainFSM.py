# Import the FSM functions
from fsm.functions import (createState, createFSM, addTransition,
    addStates, setInitialState, readWM, writeWM, setPrintTransition)	

# Import primitive robot behaviors
from api.pubapi import (sit, stand, rest, say, shutdown,
    startWalking, turnHead, setCamera, resetSubFSM,
    say, setLED, setWalkVelocity, stopWalking)

# Import FSM
from lookBallFSM import (lookBallFSM, shakeHeadState, shakeHeadState2, setTopCameraState, 
                         setBottomCameraState, setTopCameraState2, lookAtBallState, 
                         rotateState, bottomLedState, topLedState, topLedState2, 
                         stopWalkState)
                         


from kickBallFSM import (kickBallFSM, rotateLeftState, rotateRightState,
                           walkToBallState, watchBallState, stopWalkingState,
                           stopWalkingState2, setBottomCamState, setBottomLedState)

# Import functions we've written
from functions import (detectTouch, seeBall, noSeeBall)

# Create states

waitSittingState = createState("waitSittingState", lambda : None)
sitState = createState("sitState", sit)
restState = createState("restState", rest)
standState = createState("standState", stand)
shutdownState = createState("shutdownState",
				lambda : shutdown("Final state reached"))
stopWalkState = createState("stopWalkState", stopWalking)
stopWalkState2 = createState("stopWalkState2", stopWalking)
resetKickBallState = createState("resetKickBallState", lambda : resetSubFSM(kickBallFSM))
resetLookBallState = createState("resetLookBallState", lambda : resetSubFSM(lookBallFSM))

# The main FSM

# Transitions for the mainFSM

addTransition(waitSittingState, detectTouch, standState)
addTransition(standState, lambda wm: True, lookBallFSM)
#addTransition(lookBallFSM, seeBall, resetFollowBallState)
#addTransition(resetKickBallState, lambda wm: True, kickBallFSM)
addTransition(lookBallFSM, seeBall, kickBallFSM)
addTransition(kickBallFSM, noSeeBall, resetKickBallState)

addTransition(resetKickBallState, lambda wm: True, stopWalkState)
#addTransition(resetLookBallState, lambda wm: True, lookBallFSM)
addTransition(stopWalkState, lambda wm: True, lookBallFSM)

addTransition(kickBallFSM, detectTouch, stopWalkState2)
addTransition(lookBallFSM, detectTouch, stopWalkState2)

addTransition(stopWalkState2, lambda wm: True, sitState)
addTransition(sitState, lambda wm: True, restState)
addTransition(restState, lambda wm: True, shutdownState)

mainFSM = createFSM("mainFSM")
addStates(mainFSM, waitSittingState, standState, sitState,
          restState, shutdownState, lookBallFSM, kickBallFSM,
          stopWalkState, stopWalkState2, resetLookBallState, resetKickBallState)
          
setInitialState(mainFSM, waitSittingState)

# Prints all the completed transitions

setPrintTransition(mainFSM, True)
