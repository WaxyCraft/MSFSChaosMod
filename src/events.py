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

# ---------- SIM METHOD EVENTS ---------- #

#https://docs.flightsimulator.com/html/Programming_Tools/SimConnect/SimConnect_API_Reference.htm

     # ----- GO EAST -----
     # Changes the plane's longitude by -0.005.
     SimMethodEvent(eh, 
          "goEast", 
          SimMethodNotation(
               "set_pos",
               SimMethodArgument(None, Operation.SET, "PLANE_ALTITUDE"),
               SimMethodArgument(None, Operation.SET, "PLANE_LATITUDE"),
               SimMethodArgument(-0.005, Operation.ADD, "PLANE_LONGITUDE"),
               SimMethodArgument(None, Operation.INT, "AIRSPEED_TRUE")
          ),
          "Go East"
     ),

     # ----- GO WEST -----
     # Changes the plane's longitude by 0.005.
     SimMethodEvent(eh, 
          "goWest", 
          SimMethodNotation(
               "set_pos",
               SimMethodArgument(None, Operation.SET, "PLANE_ALTITUDE"),
               SimMethodArgument(None, Operation.SET, "PLANE_LATITUDE"),
               SimMethodArgument(0.005, Operation.ADD, "PLANE_LONGITUDE"),
               SimMethodArgument(None, Operation.INT, "AIRSPEED_TRUE")
          ),
          "Go West"
     )
]

eh.addEvent(events)