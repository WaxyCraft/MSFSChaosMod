from eventBackend import EventHandler
from PyQt5.QtWidgets import QApplication
from events import events
from overlay import EventTestingUtility
import sys

eh = EventHandler()
eh.addEvent(events)
app = QApplication(sys.argv)

utility = EventTestingUtility(1, "Microsoft Flight Simulator 2024 - 1.3.25.0", eh)
app.exec()