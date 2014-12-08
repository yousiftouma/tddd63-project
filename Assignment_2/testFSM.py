# Import the FSM functions
from fsm.functions import (createState, createFSM, addTransition,
    addStates, setInitialState, readWM, writeWM, setPrintTransition)

# Import primitive robot behaviors

from api.pubapi import (sit, stand, rest, say, shutdown,
    startWalking, turnHead, setCamera,
    say, setLED, setWalkVelocity, stopWalking)

from followBallFSM import (followBallFSM, rotateLeftState, 
    rotateRightState, walkToBallState, watchBallState, 
    stopWalkingState, stopWalkingState2, followBallFSM)

def detectTouch(wm):
    return readWM(wm, "tactile", "middle")

waitSittingState = createState("waitSittingState", lambda: None)
sitState = createState("sitState", sit)
restState = createState("restState", rest)
standState = createState("standState", stand)
shutdownState = createState("shutdownState",
				lambda: shutdown("Final state reached"))

mainFSM = createFSM("mainFSM")
addStates(mainFSM, waitSittingState, sitState, restState, standState,
          shutdownState, followBallFSM)

setInitialState(mainFSM, waitSittingState)

addTransition(waitSittingState, detectTouch, standState)
addTransition(standState, lambda wm: True, followBallFSM)
addTransition(followBallFSM, detectTouch, sitState)
addTransition(sitState, lambda wm: True, restState)
addTransition(restState, lambda wm: True, shutdownState)

setPrintTransition(mainFSM, True)
