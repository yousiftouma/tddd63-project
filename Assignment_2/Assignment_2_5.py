# Import the FSM functions
from fsm.functions import (createState, createFSM, addTransition,
    addStates, setInitialState, readWM, writeWM, setPrintTransition)	

# Import primitive robot behaviors
from api.pubapi import (sit, stand, rest, say, shutdown,
    startWalking, turnHead, setCamera, resetSubFSM,
    say, setLED, setWalkVelocity, stopWalking)

# Import FSM
from lookBallFSM import *
from followBallFSM import *

# Import functions we've written
from functions import (detectTouch, seeBall)

# Create states

waitSittingState = createState("waitSittingState", lambda : None)
sitState = createState("sitState", sit)
restState = createState("restState", rest)
standState = createState("standState", stand)
shutdownState = createState("shutdownState",
				lambda : shutdown("Final state reached"))
stopWalkState = createState("stopWalkState", stopWalking)
resetFollowBallState = createState("resetFollowBallState", lambda : resetSubFSM(followBallFSM))
resetLookBallState = createState("resetLookBallState", lambda : resetSubFSM(lookBallFSM))

# The main FSM

# Transitions for the mainFSM

addTransition(waitSittingState, detectTouch, standState)
addTransition(standState, lambda wm: True, lookBallFSM)
#addTransition(lookBallFSM, seeBall, resetFollowBallState)
#addTransition(resetFollowBallState, lambda wm: True, followBallFSM)
addTransition(lookBallFSM, seeBall, followBallFSM)
addTransition(followBallFSM, noSeeBall, resetFollowBallState)

addTransition(resetFollowBallState, lambda wm: True, stopWalkState)
#addTransition(resetLookBallState, lambda wm: True, lookBallFSM)
addTransition(stopWalkState, lambda wm: True, lookBallFSM)

addTransition(followBallFSM, detectTouch, sitState)
addTransition(lookBallFSM, detectTouch, sitState)

addTransition(sitState, lambda wm: True, restState)
addTransition(restState, lambda wm: True, shutdownState)

mainFSM = createFSM("mainFSM")
addStates(mainFSM, waitSittingState, standState, sitState,
          restState, shutdownState, lookBallFSM, followBallFSM,
          stopWalkState, resetLookBallState, resetFollowBallState)
          
setInitialState(mainFSM, waitSittingState)

# Prints all the completed transitions

setPrintTransition(mainFSM, True)
