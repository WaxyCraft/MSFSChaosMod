# Microsoft Flight Simulator Chaos Mod

<p align="center">
    <img src="https://github.com/WaxyCraft/MSFSChaosMod/blob/main/assets/samples/space.png" alt="Logo?"/>
</p>

#### **DISCLAIMER: MOD IS A WORK IN PROGRESS**

## Description

MSFS Choas Mod is a Python program that runs on top of Microsoft Flight Simulator 2024 (Although it should still be mostly compatible with MSFS2020.) With the mod running in a flight every 15 seconds a random event will occur. These events range from mild annoyances to major challenges to a flight. The goal of the mod is, as the name implies, to make MSFS more chaotic. It is not completely unfair, however, as a graphical overlay prepares the player for the next event.

## Features

### Window Overlay

A graphical overlay is displayed over the game that shows the next event and how long until it triggers. The overlay  is bound to the game window and moves with it. This way the overlay is effectivly part of the game window.

<p align="center">
    <img src="https://github.com/WaxyCraft/MSFSChaosMod/blob/main/assets/samples/overlay.gif" alt="GIF of Overlay"/>
    <br>
    <em>The overlay is attached to the game window.</em>
</p>

### Events

There are currently 18+ events implemented in the mod, and more to come. Currently the focus is on polishing the mod but after that is complete many more events will be made.

<p align="center">
    <img src="https://github.com/WaxyCraft/MSFSChaosMod/blob/main/assets/samples/dive.gif" alt="GIF of Dive Event"/>
    <br>
    <em>Event that causes the plane to dive.</em>
</p>

### Event Testing Utility

Though initially meant for just testing new events, the Event Testing Utility can also be used to individualy trigger specific events. Using the Start Test button will cycle through every event.

<p align="center">
    <img src="https://github.com/WaxyCraft/MSFSChaosMod/blob/main/assets/samples/testingUtility.gif" alt="Image of Event Testing Utility"/>
    <br>
    <em>The Event Testing Utility being used to trigger the Dive event.</em>
</p>

## Installation & Execution

### Installation

Python is required to use the mod. If you do not already have Python installed it can be downloaded from [here](https://www.python.org/downloads/). Once Python is installed you need to download/clone this repository, then navigate to the repository's directory in terminal and run the following command:

```
pip install -r requirements.txt
```

### Execution

After the mod is installed it can be run by running the file `src\main.py` while the game is running and in flight. To run the Event Testing Utility run `src\testingUtility.py`
