from overlay import *
from eventBackend import EventManager

hud = EventHUD(1, "Microsoft Flight Simulator - 1.37.19.0", "Text Goes Here", (0, 0.5))
manager = EventManager()

# Temporary code that I will fix later
def nothing():
     pass

def newEvent():
     event = manager.getRandomEvent()
     hud.setEvent(20, "NEXT EVENT: " + event[0], event[1], newEvent)

hud.setEvent(90, "Grace Period", nothing, newEvent)
hud.run()
