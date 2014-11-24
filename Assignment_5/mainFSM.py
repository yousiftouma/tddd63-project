# Import the FSM functions
from fsm.functions import (
	createState, createFSM,
	addTransition, addStates,
	setInitialState, readWM, setPrintTransition)

# Import primitive robot behaviors
from api.pubapi import (sit, stand, rest, shutdown, stopWalking)
                      
# Import functions we've written
from functions import (detectTouch)

# Import FSM
from walkObstacleFSM import (walkObstacleFSM)


# Create states

waitSittingState = createState("waitSittingState", lambda : None)
standState = createState("standState", stand)
sitState = createState("sitState", sit)
restState = createState("restState", rest)
stopWalkState = createState("stopWalkState", stopWalking)
shutdownState = createState("shutdownState",
				lambda : shutdown("Final state reached"))



# Add transitions 

addTransition(waitSittingState, detectTouch, standState)
addTransition(standState, lambda wm: True, walkObstacleFSM)
addTransition(walkObstacleFSM, detectTouch, stopWalkState)
addTransition(stopWalkState, lambda wm: True, sitState)
addTransition(sitState, lambda wm: True, restState)
addTransition(restState, lambda wm: True, shutdownState)

# Create the FSM and add the states created above
mainFSM = createFSM("mainFSM")
addStates(mainFSM, walkObstacleFSM, waitSittingState, standState, stopWalkState,
          sitState, restState, shutdownState)

# Set the initial state to waitSittingState
setInitialState(mainFSM, waitSittingState)

setPrintTransition(mainFSM, True)
