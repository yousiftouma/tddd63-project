# Import the FSM functions
from fsm.functions import (
	createState, createFSM,
	addTransition, addStates,
	setInitialState)		

# Import primitive robot behaviors
from api.pubapi import (sit, stand, rest, shutdown)

# Create states
sitState = createState("sitState", sit)
standState = createState("standState", stand)
restState = createState("restState", rest)
shutdownState = createState("shutdownState",
				lambda : shutdown("Final state reached"))

# Add transitions between states
addTransition(standState, lambda wm: True, sitState)
addTransition(sitState, lambda wm: True, restState)
addTransition(restState, lambda wm: True, shutdownState)


# Create the FSM and add the states created above
myFSM = createFSM("myFSM")
addStates(myFSM, standState, sitState, restState, shutdownState)

# Set the initial state to standState
setInitialState(myFSM, standState)
