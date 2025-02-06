from eventBackend import Event
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication, QMainWindow, QProgressBar, QLabel
from PyQt5 import QtCore
import sys
import win32gui

class Overlay(QMainWindow):
     def __init__(self, updateDelay: int ,overlayWindow: str, locationOffsetX: float = 0, locationOffsetY: float = 0) -> None:
          super().__init__()          
          self._updateDelay = updateDelay
          self._overlayWindow = win32gui.FindWindow(None, overlayWindow)
          self._locationOffsetX = locationOffsetX
          self._locationOffsetY = locationOffsetY

          self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
          self.setWindowTitle("MSFSChoasMod")

          self._addContent()
          self._updatePosition()

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

          QtCore.QTimer.singleShot(self._updateDelay, self._updatePosition)

class EventOverlay(Overlay):
     def __init__(self, updateDelay: int, overlayWindow: str, initialEvent: Event, locationOffsetX: float = 0, locationOffsetY: float = 0) -> None:
          self._event = initialEvent

          super().__init__(updateDelay, overlayWindow, locationOffsetX, locationOffsetY)

          self.setGeometry(300, 300, 280, 170) 


          self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

     # Initiates the eventLabel and progressBar. 
     def _addContent(self) -> None:
          layout = QVBoxLayout()
          
          self._eventLabel = QLabel(str(self._event))
          self._eventLabel.setAlignment(QtCore.Qt.AlignCenter)

          self._progressBar = QProgressBar()
          self._progressBar.setAlignment(QtCore.Qt.AlignCenter)
          self._progressBar.setValue(50)

          layout.addWidget(self._eventLabel)
          layout.addWidget(self._progressBar)
          widget = QWidget()
          widget.setLayout(layout)
          self.setCentralWidget(widget)

app = QApplication(sys.argv)
m = EventOverlay(1, "New Tab - Google Chrome", Event("Dummy Event"), 0, 0.5)
m.show()

app.exec()