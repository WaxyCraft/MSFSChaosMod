from eventBackend import EventHandler, Event
from PyQt5.QtWidgets import QApplication
from events import events
from overlay import EventOverlay
import sys

eh = EventHandler()
eh.addEvent(events)
app = QApplication(sys.argv)

eventOverlay = EventOverlay(1, "Microsoft Flight Simulator 2024 - 1.3.25.0", eh, Event("gracePeriod", "Grace Period"), 60000, 15000, 0, 0.5) # TODO: Use Regex and pyWinAuto to automatically find game window.
app.exec()