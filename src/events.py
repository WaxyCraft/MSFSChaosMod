from SimConnect import *
import random

class EventManager: 

     def __init__(self, eventsToExclude: list[int] = None) -> None:
          # Defines the list of events that can be chosen from. This is not constant and can be changed.
          self.events = [
               ("No Speed", EventManager.noSpeed),
               ("Max Speed", EventManager.maxSpeed),
               ("Turn Off Engine", EventManager.turnOffEngine),
               ("Barrel Roll", EventManager.barrelRoll),
               ("-1000 Altitude", EventManager.lowerAltitude),
               ("+1000 Altitude", EventManager.higherAltitude),
               ("Dive", EventManager.dive),
               ("Look Up", EventManager.up)
               ]
          
          if eventsToExclude != None:
               for event in eventsToExclude:
                    self.events.pop(event)

          EventManager.sm = SimConnect()
          EventManager.aq = AircraftRequests(EventManager.sm, _time=2000)
          EventManager.altitude = EventManager.aq.find("PLANE_ALTITUDE")
          EventManager.altitude.time = 200
     
     # The following is a list of event methods. What they do should be self explanatory by their names.

     def noSpeed():
          EventManager.aq.set("AIRSPEED_TRUE",0)

     def maxSpeed():
          EventManager.aq.set("AIRSPEED_TRUE",150)

     def turnOffEngine():
          EventManager.aq.set("GENERAL_ENG_THROTTLE_LEVER_POSITION:1",0)

     def barrelRoll():
          EventManager.aq.set("ROTATION_VELOCITY_BODY_Z",12000)

     def lowerAltitude():
          altitude = EventManager.aq.get("PLANE_ALTITUDE")
          EventManager.aq.set("PLANE_ALTITUDE", altitude - 1000)

     def higherAltitude():
          altitude = EventManager.aq.get("PLANE_ALTITUDE")
          EventManager.aq.set("PLANE_ALTITUDE", altitude + 1000)

     def dive():
          EventManager.aq.set("PLANE_PITCH_DEGREES",2)

     def up():
          EventManager.aq.set("PLANE_PITCH_DEGREES",5)


     def getRandomEvent(self) -> tuple:
          # Chooses a random event and returns it.
          return(random.choice(self.events))