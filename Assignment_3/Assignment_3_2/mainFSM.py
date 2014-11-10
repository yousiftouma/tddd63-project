# Import the FSM functions
from fsm.functions import (createState, createFSM, addTransition,
    addStates, setInitialState, readWM, writeWM, setPrintTransition)	

# Import primitive robot behaviors
from api.pubapi import (sit, stand, rest, say, shutdown,
    startWalking, turnHead, setCamera, resetSubFSM,
    say, setLED, setWalkVelocity, stopWalking)

# Import FSM
from findGoalFSM import (findGoalFSM)
                         

# Import functions we've written
from functions import (detectTouch, seeGoal)

# Create states

waitSittingState = createState("waitSittingState", lambda : None)
sitState = createState("sitState", sit)
restState = createState("restState", rest)
standState = createState("standState", stand)
shutdownState = createState("shutdownState",
				lambda : shutdown("Final state reached"))
stopWalkState = createState("stopWalkState", stopWalking)
lookAtGoalState = createState("lookAtGoalState", stopWalking)

# The main FSM

# Transitions for the mainFSM

addTransition(waitSittingState, detectTouch, standState)
addTransition(standState, lambda wm: True, findGoalFSM)
addTransition(findGoalFSM, seeGoal, lookAtGoalState)

addTransition(findGoalFSM, detectTouch, stopWalkState)
addTransition(lookAtGoalState, detectTouch, stopWalkState)

addTransition(stopWalkState, lambda wm: True, sitState)
addTransition(sitState, lambda wm: True, restState)
addTransition(restState, lambda wm: True, shutdownState)

mainFSM = createFSM("mainFSM")
addStates(mainFSM, waitSittingState, standState, sitState,
          restState, shutdownState, findGoalFSM, lookAtGoalState,
          stopWalkState)
          
setInitialState(mainFSM, waitSittingState)

# Prints all the completed transitions

setPrintTransition(mainFSM, True)
