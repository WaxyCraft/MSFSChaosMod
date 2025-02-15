from eventBackend import Event
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication, QMainWindow, QProgressBar, QLabel
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
import sys
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
          overlayX = x + max(int(w * xOffset - (overlayWidth // 4)), 0)
          overlayY = y + max(int(h * yOffset - (overlayHeight // 4)), 0)

          self.move(overlayX, overlayY)

     # Main window loop.
     def _loop(self) -> None:
          self._updatePosition()

# TODO: Multithread EventOverlay
class EventOverlay(Overlay):
     def __init__(self, updateDelayMs: int, overlayWindow: str, initialEvent: Event, initialEventTimeMs: int = 1000, locationOffsetX: float = 0, locationOffsetY: float = 0) -> None:
          self._event = initialEvent
          self._eventTimeMs = initialEventTimeMs
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
          self._progressValue = 100.0

     # Overrides loop method to also decrement progress bar.
     def _loop(self) -> None:
          self._updatePosition()

          if self._eventTimeProgressMs > 0:
               self._eventTimeProgressMs -= 100.0 / self._eventTimeMs * self._updateDelayMs
               self._progressBar.setValue(round(self._eventTimeProgressMs))
               self._progressBar.update()
          elif self._event:
               self._event.run()
               self._event = None
          
     @property
     def progressValue(self) -> int:
          return self._progressBar.value()
     
     @progressValue.setter
     def progressValue(self, value: int) -> None:
          self._progressBar.setValue(value)