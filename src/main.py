from overlay import Overlay
from events import EventManager

overlay = Overlay("Text Goes Here", 1)
manager = EventManager()

# Temporary code that I will fix later
def nothing():
     pass

def newEvent():
     event = manager.getRandomEvent()
     overlay.setEvent(20, "NEXT EVENT: " + event[0], event[1], newEvent)

overlay.setEvent(90, "Grace Period", nothing, newEvent)
overlay.run()