# Import the FSM functions
from fsm.functions import (
	createState, createFSM,
	addTransition, addStates,
	setInitialState, readWM)	

# Import primitive robot behaviors
from api.pubapi import (sit, stand, rest, say, shutdown)

# Define the event function which detects touch
def detectTouch(wm):
    return readWM(wm, "tactile", "middle")

## CREATE STATES ##

sitState = createState("sitState", sit)
standState = createState("standState", stand)
restState = createState("restState", rest)
shutdownState = createState("shutdownState",
				lambda : shutdown("Final state reached"))

# Create states for talking

sayHelloState = createState("sayHelloState", lambda: say("Hello World"))
sayGoodbyeState = createState("sayGoodbyeState", lambda: say("Goodbye World!"))
 
# Create states for waiting for touch

waitSittingState = createState("waitSittingState", lambda : None)
waitStandingState = createState("waitStandingState", lambda : None)

# Add transitions according to the state diagram
addTransition(waitSittingState, detectTouch, standState)
addTransition(standState, lambda wm: True, sayHelloState)
addTransition(sayHelloState, lambda wm: True, waitStandingState)
addTransition(waitStandingState, detectTouch, sayGoodbyeState)
addTransition(sayGoodbyeState, lambda wm: True, sitState)
addTransition(sitState, lambda wm: True, restState)
addTransition(restState, lambda wm: True, shutdownState)

# Create the FSM and add the states created above
myFSM = createFSM("fsm")
addStates(myFSM, waitSittingState, waitStandingState,  standState, 
          sayHelloState, sayGoodbyeState, sitState, restState, shutdownState)

# Set the initial state to waitSittingState
setInitialState(myFSM, waitSittingState)
