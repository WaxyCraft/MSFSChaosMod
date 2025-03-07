from eventBackend import *
from playsound import playsound
import multiprocessing
import math
import os
import time

class GoToFrance(Event):
     def __init__(self, eventHandler: EventHandler, name: str, displayName: str = None, description: str = None) -> None:
          super().__init__(name, displayName, description)
          self._eh = eventHandler
          self._sm = eventHandler.sm
          self._aq = eventHandler.aq

     def run(self) -> None:
          self._priorPos = {"alt": self._aq.get("PLANE_ALTITUDE"), "lat": self._aq.get("PLANE_LATITUDE"), "lon": self._aq.get("PLANE_LONGITUDE"), "hdg": int(math.degrees(self._aq.get("PLANE_HEADING_DEGREES_TRUE")))}
          self._sm.set_pos(700, 48.847351767212565, 2.3115069143603484, int(self._aq.get("AIRSPEED_TRUE")), 0, 0, 315)
          self._songProcess = multiprocessing.Process(target=playsound, args=(os.path.dirname(__file__) + "\\assets\\france.mp3",))
          self._songProcess.start()

     def recall(self) -> None:
          self._sm.set_pos(self._priorPos["alt"], self._priorPos["lat"], self._priorPos["lon"], int(self._aq.get("AIRSPEED_TRUE")), 0, 0, self._priorPos["hdg"])
          self._songProcess.terminate()

if __name__ == '__main__':
     eh = EventHandler()
     x = GoToFrance(eh, "hsg")
     time.sleep(15)
     x.run()
     time.sleep(15)
     x.recall()