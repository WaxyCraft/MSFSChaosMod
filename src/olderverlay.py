import tkinter as tk
from tkinter import ttk
import win32gui

def windowCallback(overlay, window: str) -> list:
    # Gives position and size of game window.
     try:
          hwnd = win32gui.FindWindow(None, window)
          rect = win32gui.GetWindowRect(hwnd)
          x = rect[0]
          y = rect[1]
          w = rect[2] - x
          h = rect[3] - y
          return(x, y, w, h)
     except:
          overlay.root.destroy()
          raise Exception('No window with name: "' + window + '"')

#https://github.com/notatallshaw/fall_guys_ping_estimate/blob/main/fgpe/overlay.py
#https://stackoverflow.com/questions/7142342/get-window-position-size-with-python

class Overlay:
     def __init__(self, updateDelay: int, overlayWindow: str, fracLocationOffset: tuple[float, float] = (0, 0), size: tuple[int, int] = (0, 0)) -> None:
          self.updateDelay = updateDelay
          self.overlayWindow = overlayWindow
          self.fracLocationOffset = fracLocationOffset
          self.root = tk.Tk()

          if size != None:
               self.width = size[0]
               self.height = size[1]

          self.root.overrideredirect(True) # Overides default window controls.
          self.root.lift()
          self.root.wm_attributes("-topmost", True) # Makes overlay always appear on top of other windows.

          self.transparentColor = "#000000"
          self.root.wm_attributes("-transparentcolor", self.transparentColor) # Replaces all colors of #000000 with transparency. #000000 is used since it helps prevent unwanted anti-aliasing with text. 

     def updatePosition(self) -> None:
          # Corrects position of overlay on window.
          overlayWidth = self.root.winfo_width()
          overlayHeight = self.root.winfo_height()
          wOffset = self.fracLocationOffset[0]
          hOffset = self.fracLocationOffset[1]

          x, y, w, h = windowCallback(self, self.overlayWindow)

          overlayX = int(w * wOffset - (overlayWidth // 4)) # Offsets the overlay and corrects for the overlay's own height.
          overlayY = int(h * hOffset - (overlayHeight // 4))
          self.root.geometry(str(overlayWidth) + "x" + str(overlayHeight) + "+" + str(x + max(overlayX, 0)) + "+" + str(y + max(overlayY, 0))) # Maxes overlay with 0 to prevent negative overlays.
          self.root.after(self.updateDelay, self.updatePosition)
          
     def run(self) -> None:
          self.root.after(self.updateDelay, self.updatePosition)
          self.root.mainloop()

class EventHUD(Overlay):
     def __init__(self, updateDelay: int, overlayWindow: str, initialText: str, fracLocationOffset: tuple[float, float] = (0, 0)):
          super().__init__(updateDelay, overlayWindow, fracLocationOffset)
          self.initialText = initialText

          self.root.config(bg = '')

          eventLabel = tk.Label(self.root, text=initialText, font=('Impact', 20), fg="white", bg="#000000")
          eventLabel.pack()
          self.text = eventLabel

          progress = tk.IntVar() # Defines progress as the value of the progress bar.
          progressbar = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate", value=100, variable=progress)
          progressbar.pack(pady=20)
          self.progressbar = progressbar
          self.progress = progress

     def setEvent(self, time: int, eventName: str, event: object, callbackFunction: object) -> None:
          # Changes label to upcoming event and set progress bar time.
          self.text["text"] = eventName
          self.eventFunction = event # Sets eventFunction to a function that triggers event.
          self.callbackFunction = callbackFunction # Sets callbackFunction to a function that callsback to alert that a new event is needed.
          self.progress.set(100)
          self.time = time
          self.updateProgress()

     def updateProgress(self) -> None:
          self.progressbar.step(-0.1)
          if self.progress.get() < 0:
               self.eventFunction()
               self.callbackFunction()
          else:
               self.root.after(int(self.time), self.updateProgress) # The first parameter in the after function is in milliseconds while self.time is in seconds so this is effectivly dividing the time by 1000.