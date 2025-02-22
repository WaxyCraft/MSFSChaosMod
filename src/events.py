from eventBackend import *

eh = EventHandler()

# List of Event objects.
events = [

# ---------- SIM VAR EVENTS ---------- #

# https://docs.flightsimulator.com/html/Programming_Tools/SimVars/Simulation_Variables.htm

     # ----- DOUBLE ALTITUDE -----
     # Doubles the current plane altitude.
     SimVarEvent(eh, 
          "doubleAlt", 
          SimVarNotation("PLANE_ALTITUDE", "PLANE_ALTITUDE", Operation.MUL, 2),
          "Double Altitude"
     ),

     # ----- HALVE ALTITUDE -----
     # Halves the current plane altitude.
     SimVarEvent(eh, 
          "halveAlt", 
          SimVarNotation("PLANE_ALTITUDE", "PLANE_ALTITUDE", Operation.DIV, 2),
          "Halve Altitude"
     ),

     # # ----- OPEN CANOPY ----- SEEMS TO NOT WORK IN 2024
     # # Opens the plane canopy.
     # SimVarEvent(eh, 
     #      "openCanopy", 
     #      SimVarNotation("CANOPY_OPEN", 1.0),
     #      "Open Canopy"
     # ),

     # # ----- RANDOM CAMERA ----- SEEMS TO NOT BE SUPPORTED BY SIMCONNECT PYTHON
     # # Switches to a random camera state.
     # SimVarEvent(eh, 
     #      "randomCamera", 
     #      SimVarNotation("CAMERA_STATE", 2, Operation.RAN, 8),
     #      "Random Camera"
     # ),  

     # ----- STOP PLANE -----
     # Sets airspeed to 0.
     SimVarEvent(eh, 
          "stopPlane", 
          SimVarNotation("AIRSPEED_TRUE", 0),
          "Stop Plane"
     ),      

     # ----- MAX SPEED -----
     # Sets airspeed to 10000.
     SimVarEvent(eh, 
          "maxSpeed", 
          SimVarNotation("AIRSPEED_TRUE", 1000),
          "Max Plane"
     ),  

     # ----- DIVE -----
     # Makes the plane face straight down.
     SimVarEvent(eh, 
          "dive", 
          SimVarNotation("PLANE_PITCH_DEGREES", 2),
          "Dive"
     ),  

     # ----- RIGHT AILERON -----
     # Sets aileron position all the way to the right.
     SimVarEvent(eh, 
          "rightAileron", 
          SimVarNotation("AILERON_POSITION", 16000),
          "Right Aileron"
     ),  

     # ----- LEFT AILERON -----
     # Sets aileron position all the way to the left.
     SimVarEvent(eh, 
          "leftAileron", 
          SimVarNotation("AILERON_POSITION", -16000),
          "Left Aileron"
     ),  

     # ----- MAX FLAPS -----
     # Sets flaps to max position.
     SimVarEvent(eh, 
          "maxFlaps", 
          SimVarNotation("FLAP_POSITION_SET", 5),
          "Max Flaps"
     ), 

     # ----- RANDOM AILERON -----	
     # Sets aileron position to a random value.
     SimVarEvent(eh, 
          "randomAileron", 
          SimVarNotation("AILERON_POSITION", -16000, Operation.RAN, 16000),
          "Random Aileron"
     ),  

     # ----- RANDOM ELEVATOR -----
     # Sets elevator position to a random value.
     SimVarEvent(eh, 
          "randomElevator", 
          SimVarNotation("ELEVATOR_POSITION", -16000, Operation.RAN, 16000),
          "Random Elevator"
     ), 

     # ----- RANDOM RUDDER -----
     # Sets Rudder position to a random value.
     SimVarEvent(eh, 
          "randomRudder", 
          SimVarNotation("RUDDER_POSITION", -16000, Operation.RAN, 16000),
          "Random Rudder"
     ), 

     # ----- FLEXY WINGS -----
     # Sets wing flex to max.
     SimVarEvent(eh, 
          "flexyWings", 
          [SimVarNotation("WING_FLEX_PCT:1", 1), SimVarNotation("WING_FLEX_PCT:2", 1)],
          "Flexy Wings"
     ), 

     # ----- SLEW -----
     # Enables slew mode.
     SimVarEvent(eh, 
          "slewMode", 
          SimVarNotation("IS_SLEW_ACTIVE", True),
          "Slew Mode"
     ),

     # ----- NEGATIVE SPEED -----
     # Sets airspeed to -10000.
     SimVarEvent(eh, 
          "negativeSpeed", 
          SimVarNotation("AIRSPEED_TRUE", -10000),
          "Negative Speed"
     ),  

     # ----- TURN OFF CABIN LIGHT -----
     # Turns off the cabin light.
     SimVarEvent(eh, 
          "turnOffCabinLight", 
          SimVarNotation("LIGHT_CABIN", False),
          "Turn Off Cabin Light"
     ),  

# ---------- SIM EVENT EVENTS ---------- #

# https://docs.flightsimulator.com/html/Programming_Tools/Event_IDs/Event_IDs.htm
     
     # ----- TOGGLE LANDING GEAR -----
     # Toggles landing gear.
     SimEventEvent(eh, 
          "toggleGear", 
          SimEventNotation("GEAR_TOGGLE"),
          "Toggle Landing Gear"
     ),

     # ----- SHUTDOWN ENGINE -----
     # Auto shutdowns engine.
     SimEventEvent(eh, 
          "shutdownEngine", 
          SimEventNotation("ENGINE_AUTO_SHUTDOWN"),
          "Shutdown Engine"
     ),

     # ----- SHUTDOWN APU -----
     # Shutdowns the auxiliary power unit
     SimEventEvent(eh, 
          "shutdownAPU", 
          SimEventNotation("APU_OFF_SWITCH"),
          "Shutdown APU"
     )

# ---------- SIM METHOD EVENTS ---------- #

#https://docs.flightsimulator.com/html/Programming_Tools/SimConnect/SimConnect_API_Reference.htm

     # # ----- GO EAST -----
     # # Changes the plane's longitude by -0.005.
     # SimMethodEvent(eh, 
     #      "goEast", 
     #      SimMethodNotation(
     #           "set_pos",
     #           SimMethodArgument(None, Operation.SET, "PLANE_ALTITUDE"),
     #           SimMethodArgument(None, Operation.SET, "PLANE_LATITUDE"),
     #           SimMethodArgument(-0.005, Operation.ADD, "PLANE_LONGITUDE"),
     #           SimMethodArgument(None, Operation.INT, "AIRSPEED_TRUE")
     #      ),
     #      "Go East"
     # ),

     # # ----- GO WEST -----
     # # Changes the plane's longitude by 0.005.
     # SimMethodEvent(eh, 
     #      "goWest", 
     #      SimMethodNotation(
     #           "set_pos",
     #           SimMethodArgument(None, Operation.SET, "PLANE_ALTITUDE"),
     #           SimMethodArgument(None, Operation.SET, "PLANE_LATITUDE"),
     #           SimMethodArgument(0.005, Operation.ADD, "PLANE_LONGITUDE"),
     #           SimMethodArgument(None, Operation.INT, "AIRSPEED_TRUE")
     #      ),
     #      "Go West"
     # )
]

eh.addEvent(events)