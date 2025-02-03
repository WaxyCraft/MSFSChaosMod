import tkinter as tk
from tkinter import ttk
from eventBackend import *
import pyautogui
import win32gui

class Overlay:
     def __init__(self, updateDelay: int, overlayWindow: str, fracLocationOffset: tuple[float, float] = (0, 0), size: tuple[int, int] = (0, 0)) -> None:
          self._updateDelay = updateDelay
          self._overlayWindow = hwnd = win32gui.FindWindow(None, overlayWindow)
          self._fracLocationOffset = fracLocationOffset
          self._root = tk.Tk()

          if size != None:
               self.width = size[0]
               self.height = size[1]

          # Overides default window controls and makes overlay always appear on top of other windows.
          self._root.overrideredirect(True)
          self._root.lift()
          self._root.wm_attributes("-topmost", True)

     # Corrects position of overlay.
     def _updatePosition(self) -> None:
          # Corrects position of overlay on window.
          overlayWidth = self._root.winfo_width()
          overlayHeight = self._root.winfo_height()
          wOffset = self._fracLocationOffset[0]
          hOffset = self._fracLocationOffset[1]

          windowRect = win32gui.GetWindowRect(self._overlayWindow)
          x = windowRect[0]
          y = windowRect[1]
          w = windowRect[2] - x
          h = windowRect[3] - y

          # Offsets the overlay and corrects for the overlay's own height.
          overlayX = int(w * wOffset - (overlayWidth // 4))
          overlayY = int(h * hOffset - (overlayHeight // 4))

          self._root.geometry(str(overlayWidth) + "x" + str(overlayHeight) + "+" + str(x + max(overlayX, 0)) + "+" + str(y + max(overlayY, 0)))
          self._root.after(self._updateDelay, self._updatePosition)
          
     def run(self) -> None:
          self._root.after(self._updateDelay, self._updatePosition)
          self._root.mainloop()

     def exit(self) -> None:
          self._root.destroy()

class EventOverlay(Overlay):
     def __init__(self, updateDelay: int, overlayWindow: str, initialEvent: str, fracLocationOffset: tuple[float, float] = (0, 0), size: int = (0, 0)):
          super().__init__(updateDelay, overlayWindow, fracLocationOffset, size)
          self._event = initialEvent

          eventLabel = tk.Label(self._root, text = str(initialEvent), font = ('Impact', 20), fg = "white", bg = "white")
          eventLabel.pack()
          self.text = eventLabel

          self._root.config(bg = '')

     def _getTextAntiAliasingColor(self) -> str:
          x, y = 100, 100  # Replace with pixel coordinates
          color = pyautogui.pixel(x, y)
          print(f"RGB color at ({x}, {y}): {color}")

x = EventOverlay(10, "MoodLight - Free Online Strobe/Disco/Party/Mood Light - Google Chrome", Event("dummyEvent", "Dummy Event"), (0, 0.5))
x.run()