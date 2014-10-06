# Import the FSM functions
from fsm.functions import (
	createState , createFSM ,
	addTransition , addStates ,
	setInitialState)		# setMainFSM should be there
# Import primitive robot behaviors
from api.pubapi import sit, stand , rest, say , shutdown

# Create states
sitState = createState("sitState", sit)
standState = createState("standState", stand)
restState = createState("restState", rest)
shutdownState = createState("shutdownState",
				lambda : shutdown("Final state reached"))

# Create a state which commands the robot to say "Hello World!"
sayState = createState("sayState", lambda : say("Hello World")) 

# Add transitions between states
addTransition(standState , lambda wm: True , sayState)
addTransition(sayState , lambda wm: True , sitState)
addTransition(sitState , lambda wm: True , restState)
addTransition(restState , lambda wm: True , shutdownState)


# Create the FSM and add the states created above
myFSM = createFSM("fsm")
addStates(myFSM , standState , sayState , sitState , restState , shutdownState)

# Set the initial state to standState
setInitialState(myFSM , standState)
