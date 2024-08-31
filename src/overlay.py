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
     def __init__(self, initialText: str, updateDelay: int) -> None:
          self.initialText = initialText
          self.updateDelay = updateDelay
          self.root = tk.Tk()

          self.root.overrideredirect(True) # Overides default window controls.
          self.root.lift()
          self.root.wm_attributes("-topmost", True) # Makes overlay always appear on top of other windows.
          self.root.config(bg = '#000000')
          self.root.wm_attributes('-transparentcolor','#000000') # Replaces all colors of #000000 with transparency. #000000 is used since it helps prevent unwanted anti-aliasing with text. 

          eventLabel = tk.Label(self.root, text=initialText, font=('Impact', 20), fg="white", bg="#000000")
          eventLabel.pack()
          self.text = eventLabel

          progress = tk.IntVar()
          progressbar = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate", value=100, variable=progress)
          progressbar.pack(pady=20)
          self.progressbar = progressbar
          self.progress = progress

          self.height = self.root.winfo_height()
          self.width = self.root.winfo_height()

     def updatePosition(self) -> None:
          # Corrects position of overlay on window.
          x, y, w, h = windowCallback(self, "Microsoft Flight Simulator - 1.37.19.0")
          middleHeight = (h // 2) - (self.height // 4) # Vertically centers the overlay.
          self.root.geometry("+" + str(x) + "+" + str(y + middleHeight))
          self.root.after(self.updateDelay, self.updatePosition)

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
          
     def run(self) -> None:
          self.root.after(self.updateDelay, self.updatePosition)
          self.root.mainloop()

# def test():
#      print("hi")
#      x.setEvent(20, "NEXT EVENT: Drink Water", test)

# x = Overlay("If you are seeing this then something probably went wrong lol.", 1)
# x.setEvent(60, "Grace Period", test)
# x.run()
