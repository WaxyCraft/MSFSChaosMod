from SimConnect import *
from errorHandling import *
from enum import Enum

# EVENTS DO NOT WORK IF LIVE TIME IS ENABLED IN GAME!

class EventType(Enum):
     GENERIC = 0    # Used for the base Event class that the others inherit from. Should never actually be used for an Event.
     SIM_VAR = 1    # Used for the SimVarEvent class. These Events modify Simulation Variables. SimVars Docs: https://docs.flightsimulator.com/html/Programming_Tools/SimVars/Simulation_Variables.htm
     SIM_EVENT = 2  # Used for the SimEventEvent class. These Events trigger Simulation Events. Event IDs Docs: https://docs.flightsimulator.com/html/Programming_Tools/Event_IDs/Event_IDs.htm
     SIM_METHOD = 3 # Used for SimMethodEvent class. These Events trigger various other methods built into SimConnect. SimConnect API Docs: https://docs.flightsimulator.com/html/Programming_Tools/SimConnect/SimConnect_API_Reference.htm
     CUSTOM = 4     # Used for all classes that begin with Custom. These Events allow for arbitrary code to be used for more complicated Events.

# All Events run through an instance of the EventHandler.
class EventHandler:
     def __init__(self, requestTime: int = 10) -> None:
          self._sm = SimConnect()
          self._aq = AircraftRequests(self._sm, requestTime)
          self.usedEventID = []
          self.largestEventID = 0

     # TODO: Make code more rebust. 
     def newEventID(self) -> int | Response:
          responseID = self.largestEventID + 1
          if responseID in self.usedEventID:
               return Response(ErrorHandler.newResponseID, ResponseStatus.ERROR, "Event ID Conflict", True)
          else:
               return responseID
          
     # TODO: Make method to generate random event.

     @property
     def sm(self):
          return self._sm
     
     @property
     def aq(self):
          return self._aq

# Base Event class.
class Event:
     def __init__(self, eventID: int, name: str, displayName: str = None, description: str = None) -> None:
          self._eventID = eventID
          self._name = name
          self._description = description
          self._eventType = EventType.GENERIC

          if displayName:
               self._displayName = displayName
          else:
               self._displayName = name

     def run(self) -> Response:
          return Response(ErrorHandler.newResponseID(), ResponseStatus.WARNING, "Placeholder Code For Event Class")

     @property
     def eventID(self) -> str:
          return self._eventID
     
     @property
     def name(self) -> str:
          return self._name
     
     @property
     def displayName(self) -> str:
          return self._displayName

     @property
     def description(self) -> str:
          return self._description
     
     @property
     def eventType(self) -> str:
          return self._eventType
     
     def __str__(self) -> str:
          return self._name

# Instuctions that get passed to a SimVarEvent telling it what to set each variable to (IE: Set SimVar "PLANE_ALTITUDE" to "PLANE_ALTITUDE" + 1000).
class SimVarNotation:
     class Operation(Enum):
          ADD = 0
          SUB = 1
          MUL = 2
          DIV = 3
          EXP = 4

     def __init__(self, setVar: str, value: str | int | float, operation: Operation = None, modifyValue: str | int | float = None) -> None:
          self._setVar = setVar           # Varible to be set.
          self._value = value             # Value to set to.
          self._operation = operation     # The operation between the value and modifyValue.
          self._modifyValue = modifyValue # Value to modify the value with.

     @property
     def setVar(self) -> str:
          return self._setVar
     
     @property
     def value(self) -> str | int | float:
          return self._value
     
     @property
     def operation(self) -> Operation:
          return self._operation
     
     @property
     def modifyValue(self) -> str | int | float:
          return self._modifyValue

# Class for Events that modify Simulation Variables. SimVars Docs: https://docs.flightsimulator.com/html/Programming_Tools/SimVars/Simulation_Variables.htm
class SimVarEvent(Event):
     def __init__(self, eventHandler: EventHandler, eventID: int, name: str, commands: SimVarNotation | list[SimVarNotation], displayName: str = None, description: str = None) -> None:
          super().__init__(eventID, name, displayName, description)
          self._eventType = EventType.SIM_VAR
          self._sm = eventHandler.sm
          self._aq = eventHandler.aq
          self._commands = commands

     # Run command from SimVarNotation object.
     def _evalCommand(self, command: SimVarNotation) -> Response:
          setVar = command.setVar
          value = command.value
          operation = command.operation
          modifyValue = command.modifyValue

          # If modifyValue or value are strings then they must be Simulation Variables. 
          if type(modifyValue) == str: 
               modifyValue = self._aq.get(modifyValue)
          if type(value) == str:
               value = self._aq.get(value)
               
          valToSet = value

          if operation and modifyValue:
               match operation:
                    case SimVarNotation.Operation.ADD:
                         valToSet = value + modifyValue
                    case SimVarNotation.Operation.SUB:
                         valToSet = value - modifyValue
                    case SimVarNotation.Operation.MUL:
                         valToSet = value * modifyValue
                    case SimVarNotation.Operation.DIV:
                         valToSet = value / modifyValue
                    case SimVarNotation.Operation.EXP:
                         valToSet = value ** modifyValue
                         
          if self._aq.set(setVar, valToSet):
               return Response(ErrorHandler.newResponseID, ResponseStatus.OK)
          else:
               return Response(ErrorHandler.newResponseID, ResponseStatus.WARNING, "Failed To Set SimVar")

     def run(self) -> Response:
          if type(self._commands) == SimVarNotation:
               return self._evalCommand(self._commands)
          else:
               for command in self._commands:
                    return self._evalCommand(command)