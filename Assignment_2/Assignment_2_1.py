# Import the FSM functions
from fsm.functions import (
	createState , createFSM ,
	addTransition , addStates ,
	setInitialState, readWM )		# setMainFSM should be there

# Import primitive robot behaviors
from api.pubapi import sit, stand , rest, say , shutdown ,\
    startWalking , stopWalking

# Define the functions for world model
def detectTouch(wm):
    return readWM(wm, "tactile", "middle")
def walkTime(wm):
    return readWM(wm, "time", "entry + 5")

## CREATE STATES ##

sitState = createState("sitState", sit)
standState = createState("standState", stand)
restState = createState("restState", rest)
walkState = createState("walkState", startWalking)
stopWalkState = createState("stopWalkState", stopWalking)
shutdownState = createState("shutdownState",
				lambda : shutdown("Final state reached"))

# Create states for talking

sayLetsWalkState = createState("sayLetsWalkState", lambda : say("Lets walk!"))
sayGoodbyeState = createState("sayGoodbyeState", lambda : say("Goodbye World!"))
 
# Create states for waiting for touch

waitSittingState = createState("waitSittingState", lambda : None)
#waitStandingState = createState("waitStandingState", lambda : None)

# Add transitions according to the state diagram
addTransition(waitSittingState , detectTouch , standState)
addTransition(standState , lambda wm: True , sayLetsWalkState)
addTransition(standState , lambda wm: True , walkState)
addTransition(walkState , walkTime , stopWalkState)
addTransition(stopWalkState, lambda wm: True , sayGoodbyeState)
addTransition(sayGoodbyeState , lambda wm: True , sitState)
addTransition(sitState , lambda wm: True , restState)
addTransition(restState , lambda wm: True , shutdownState)

# Create the FSM and add the states created above
myFSM = createFSM("fsm")
addStates(myFSM , waitSittingState , waitStandingState ,  standState , 
          sayHelloState , sayGoodbyeState , sitState , restState , shutdownState)

# Set the initial state to waitSittingState
setInitialState(myFSM , waitSittingState)


