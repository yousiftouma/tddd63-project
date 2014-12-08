# Import the FSM functions
from fsm.functions import (createState, createFSM, addTransition,
    addStates, setInitialState, readWM, writeWM, setPrintTransition)	

# Import primitive robot behaviors
from api.pubapi import (sit, stand, rest, say, shutdown,
    startWalking, turnHead, setCamera, resetSubFSM,
    say, setLED, setWalkVelocity, stopWalking, communicate)

# Import FSM
from lookBallFSM import (lookBallFSM)
from goToBallFSM import (goToBallFSM)
                        

# Import functions we've written
from functions import (detectTouch, seeBall, noSeeBall, closeToFeet, seeGoal, oneKick,
                       waitForSit, waitForStand, waitForKick, waitForFindBall)

# Create states

waitSittingState = createState("waitSittingState", lambda : None)
sitState = createState("sitState", sit)
restState = createState("restState", rest)
standState = createState("standState", stand)
shutdownState = createState("shutdownState",
				lambda : shutdown("Final state reached"))
stopWalkState = createState("stopWalkState", stopWalking)
stopWalkState2 = createState("stopWalkState", stopWalking)
resetLookBallState = createState("resetLookBallState", lambda: resetSubFSM(lookBallFSM))
resetgoToBallState = createState("resetgoToBallState", lambda: resetSubFSM(goToBallFSM))

# States for communication

robot = "david"

sendSitStatus = createState("sendSitStatus" , 
                               lambda: communicate(robot, "Sit"))



# The main FSM

# Transitions for the mainFSM

addTransition(waitSittingState, waitForStand, standState)
addTransition(standState, waitForFindBall, lookBallFSM)
addTransition(lookBallFSM, seeBall, resetLookBallState)
addTransition(resetLookBallState, lambda wm: True, goToBallFSM)
addTransition(goToBallFSM, noSeeBall, resetgoToBallState)
addTransition(resetgoToBallState, lambda wm: True, lookBallFSM)
addTransition(goToBallFSM, closeToFeet, stopWalkState)
addTransition(stopWalkState, lambda wm: True, sendSitStatus)

addTransition(goToBallFSM, detectTouch, stopWalkState2)
addTransition(lookBallFSM, detectTouch, stopWalkState2)
addTransition(stopWalkState2, lambda wm: True, sendSitStatus)

addTransition(sendSitStatus, lambda wm: True, sitState)
addTransition(sitState, lambda wm: True, restState)
addTransition(restState, lambda wm: True, shutdownState)


secondFSM = createFSM("secondFSM")
addStates(secondFSM, waitSittingState, standState, sitState, goToBallFSM,
          restState, shutdownState, lookBallFSM,
          stopWalkState, stopWalkState2, sendSitStatus,
          resetLookBallState, resetgoToBallState)
          
setInitialState(secondFSM, waitSittingState)

# Prints all the completed transitions

setPrintTransition(secondFSM, True)
