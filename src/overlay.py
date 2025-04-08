from eventBackend import Event, EventHandler
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QMainWindow, QProgressBar, QLabel, QPushButton, QListWidget, QListWidgetItem
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
import win32gui

class Overlay(QMainWindow):
     def __init__(self, updateDelayMs: int, overlayWindow: str, locationOffsetX: float = 0, locationOffsetY: float = 0) -> None:
          super().__init__()          
          self._updateDelayMs = updateDelayMs
          self._overlayWindow = win32gui.FindWindow(None, overlayWindow)
          self._locationOffsetX = locationOffsetX
          self._locationOffsetY = locationOffsetY

          self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
          self.setWindowTitle("MSFSChoasMod")

          self._addContent()

          self._timer = QtCore.QTimer()
          self._timer.timeout.connect(self._loop)
          self._timer.start(self._updateDelayMs)

          self.show()

     # Adds content to Overlay. Should be overridden by child classes.
     def _addContent(self) -> None:
          pass

     # Corrects position of overlay to move with the overlayWindow.
     def _updatePosition(self) -> None:
          overlayWidth = self.frameGeometry().width()
          overlayHeight = self.frameGeometry().height()

          xOffset = self._locationOffsetX
          yOffset = self._locationOffsetY

          windowRect = win32gui.GetWindowRect(self._overlayWindow)
          x = windowRect[0]
          y = windowRect[1]
          w = windowRect[2] - x
          h = windowRect[3] - y

          # Offsets the overlay and corrects for the overlay's own height.
          overlayX = x + max(int(w * xOffset - (overlayWidth)), 0)
          overlayY = y + max(int(h * yOffset - (overlayHeight)), 0)

          self.move(overlayX, overlayY)

     # Main window loop.
     def _loop(self) -> None:
          self._updatePosition()

# TODO: Multithread EventOverlay
class EventOverlay(Overlay):
     def __init__(self, updateDelayMs: int, overlayWindow: str, eventHandler: EventHandler, initialEvent: Event, initialEventTimeMs: int = 15000, futureEventTimeMs: int = 15000, locationOffsetX: float = 0, locationOffsetY: float = 0) -> None:
          self._eh = eventHandler
          self._event = initialEvent
          self._eventTimeMs = initialEventTimeMs
          self._constantEventTimeMs = futureEventTimeMs
          self._eventTimeProgressMs = 100.0

          super().__init__(updateDelayMs, overlayWindow, locationOffsetX, locationOffsetY)

          self.setGeometry(300, 300, 280, 50) 

          self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

     # Initiates the eventLabel and progressBar. 
     def _addContent(self) -> None:
          layout = QVBoxLayout()
          
          self._eventLabel = QLabel(self._event.displayName)
          self._eventLabel.setAlignment(QtCore.Qt.AlignCenter)
          self._eventLabel.setFont(QFont('Impact', 18)) 
          self._eventLabel.setStyleSheet("color: white;")

          self._progressBar = QProgressBar()
          self._progressBar.setAlignment(QtCore.Qt.AlignCenter)
          self._progressBar.setTextVisible(False)
          self._progressBar.setValue(50)
          self._progressBar.setStyleSheet("QProgressBar::chunk {background-color: LimeGreen;}")

          layout.addWidget(self._eventLabel)
          layout.addWidget(self._progressBar)
          widget = QWidget()
          widget.setLayout(layout)
          self.setCentralWidget(widget)

     # Sets eventLabel text to the event name and resets the progress bar.
     def setEvent(self, event: Event, timeMs: int) -> None:
          self._event = event
          self._eventLabel.setText(self._event.displayName)
          self._eventTimeProgressMs = 100.0
          self._eventTimeMs = timeMs

     # Overrides loop method to also decrement progress bar.
     def _loop(self) -> None:
          self._updatePosition()

          if self._eventTimeProgressMs > 0:
               self._eventTimeProgressMs -= 100.0 / self._eventTimeMs * self._updateDelayMs
               self._progressBar.setValue(round(self._eventTimeProgressMs))
               self._progressBar.update()
          elif self._event:
               self._eh.runEvent(self._event)
               self.setEvent(self._eh.getRandomEvent(), self._constantEventTimeMs)       
     @property
     def progressValue(self) -> int:
          return self._progressBar.value()
     
     @progressValue.setter
     def progressValue(self, value: int) -> None:
          self._progressBar.setValue(value)

# Wrapper for QListWidgetItem that also contains an event. Used for EventTestingUtility.
class EventItemWrapper(QListWidgetItem):
     def __init__(self, event: Event) -> None:
          super().__init__(f"{event.displayName} ({event.name})")
          self._event = event

     @property
     def event(self) -> Event:
          return self._event

# Class for EventTestingUtility overlay.
class EventTestingUtility(Overlay):
     def __init__(self, updateDelayMs: int, overlayWindow: str, eventHandler: EventHandler, locationOffsetX: float = 1, locationOffsetY: float = 0, widthPx: int = 300, heighPx: int = 500) -> None:
          self._widthPx = widthPx
          self._heightPx = heighPx
          self._eh = eventHandler
          self._testActive = False
          self._lastEventFlag = False
          self._eventCount = 0
          self._results = {}

          self._currentEvent = None

          super().__init__(updateDelayMs, overlayWindow, locationOffsetX, locationOffsetY)

          self.setWindowTitle("Event Testing Utility")
          self.setGeometry(0, 0, widthPx, heighPx) 

     # Initiates the eventLabel and buttons. 
     def _addContent(self) -> None:          
          self._startTestButton = QPushButton("Start Test", self)
          self._startTestButton.setGeometry(0, 0, int(self._widthPx * 0.5), int(self._heightPx * 0.1))
          self._startTestButton.clicked.connect(self._startTest)

          self._endTestButton = QPushButton("End Test", self)
          self._endTestButton.setGeometry(int(self._widthPx * 0.5), 0, int(self._widthPx * 0.5), int(self._heightPx * 0.1))
          self._endTestButton.setEnabled(False)
          self._endTestButton.clicked.connect(self._endTest)

          self._eventLabel = QLabel("Current Event:\nNone", self)
          self._eventLabel.setGeometry(0, int(self._heightPx * 0.15), self._widthPx, int(self._heightPx * 0.1))
          self._eventLabel.setFont(QFont('TimesNewRoman', 10)) 
          self._eventLabel.setAlignment(QtCore.Qt.AlignCenter)

          self._nextEventLabel = QLabel("Next Event:\nNone", self)
          self._nextEventLabel.setGeometry(0, int(self._heightPx * 0.25), self._widthPx, int(self._heightPx * 0.1))
          self._nextEventLabel.setFont(QFont('TimesNewRoman', 10)) 
          self._nextEventLabel.setAlignment(QtCore.Qt.AlignCenter)

          self._eventSuccessButton = QPushButton("Yay", self)
          self._eventSuccessButton.setGeometry(0, int(self._heightPx * 0.4), int(self._widthPx * 0.5), int(self._heightPx * 0.1))
          self._eventSuccessButton.setEnabled(False)
          self._eventSuccessButton.clicked.connect(self._eventSuccess)

          self._eventFailureButton = QPushButton("Nah", self)
          self._eventFailureButton.setGeometry(int(self._widthPx * 0.5), int(self._heightPx * 0.4), int(self._widthPx * 0.5), int(self._heightPx * 0.1))
          self._eventFailureButton.setEnabled(False)
          self._eventFailureButton.clicked.connect(self._eventFailure)

          self._eventList = QListWidget(self)
          self._eventList.setGeometry(0, int(self._heightPx * 0.5), self._widthPx, int(self._heightPx * 0.3))

          for event in self._eh.events:
               self._eventList.addItem(EventItemWrapper(event))

          self._triggerEventButton = QPushButton("Trigger Selected Event", self)
          self._triggerEventButton.setGeometry(int(self._widthPx * 0.25), int(self._heightPx * 0.8), int(self._widthPx * 0.5), int(self._heightPx * 0.1))
          self._triggerEventButton.clicked.connect(lambda: self._triggerEvent(self._eventList.currentItem().event))

          self._logResultsButton = QPushButton("Log Results", self)
          self._logResultsButton.setGeometry(int(self._widthPx * 0.25), int(self._heightPx * 0.9), int(self._widthPx * 0.5), int(self._heightPx * 0.1))
          self._logResultsButton.clicked.connect(self._logResults)

          self._exitButton = QPushButton("X", self)
          self._exitButton.setGeometry(int(self._widthPx * 0.95), int(self._heightPx * 0.95), int(self._widthPx * 0.05), int(self._heightPx * 0.05))
          self._exitButton.clicked.connect(self.close)

     # Prints out current results. TODO: Save results to a file.
     def _logResults(self) -> None:
          print("----- Test Results -----")
          for result in self._results:
               print(f"Event: {result} | Success: {self._results[result]}")

     # Is called when the user presses the eventSuccessButton indicating that an event ran successfully.
     def _eventSuccess(self) -> None:
          self._results[self._currentEvent.name] = True
          if self._testActive:
               self._triggerNextEvent()
          else:
               self._eventSuccessButton.setEnabled(False)
               self._eventFailureButton.setEnabled(False)
               self._currentEvent = None
               self._eventLabel.setText("Current Event:\nNone")

     # Is called when the user presses the eventFailureButton indicating that an event failed.
     def _eventFailure(self) -> None:
          self._results[self._currentEvent.name] = False
          if self._testActive:
               self._triggerNextEvent()
          else:
               self._eventSuccessButton.setEnabled(False)
               self._eventFailureButton.setEnabled(False)
               self._currentEvent = None
               self._eventLabel.setText("Current Event:\nNone")

     # Initiates a systematic event test. 
     def _startTest(self) -> None:
          self._startTestButton.setEnabled(False)
          self._endTestButton.setEnabled(True)
          self._testActive = True
          self._triggerEventButton.setEnabled(False)
          self._triggerNextEvent()

     # Prematurely a systematic event test. 
     def _endTest(self) -> None:
          self._startTestButton.setEnabled(True)
          self._endTestButton.setEnabled(False)
          self._eventSuccessButton.setEnabled(False)
          self._eventFailureButton.setEnabled(False)
          self._triggerEventButton.setEnabled(True)
          self._lastEventFlag = False
          self._testActive = False
          self._currentEvent = None
          self._eventLabel.setText("Current Event:\nNone")
          self._eventCount = 0

     # Runs an event and changes the currentEvent and eventLabel to match.
     def _triggerEvent(self, event: Event) -> None:
          self._eventLabel.setText(f"Current Event:\n{event.displayName} ({event.name})")
          self._currentEvent = event
          event.run()
          self._eventSuccessButton.setEnabled(True)
          self._eventFailureButton.setEnabled(True)

     # Triggers the next event in a systematic event test.
     def _triggerNextEvent(self) -> None:
          if not self._lastEventFlag:
               self._currentEvent = self._eh.events[self._eventCount]
               self._triggerEvent(self._currentEvent)
               if len(self._eh.events) - 1 > self._eventCount:
                    self._eventCount += 1
                    nextEvent = self._eh.events[self._eventCount]
                    self._nextEventLabel.setText(f"Next Event:\n{nextEvent.displayName} ({nextEvent.name})")
               else:
                    self._lastEventFlag = True
                    self._nextEventLabel.setText("Next Event:\nNone")
          else:
               self._testActive = False
               self._endTest()