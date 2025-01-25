from SimConnect import *
from errorHandling import *
from enum import Enum

class EventType(Enum):
     GENERIC = 0    # Used for the base Event class that the others inherit from. Should never actually be used for an Event.
     SIM_VAR = 1    # Used for the SimVarEvent class. These Events modify Simulation Variables. SimVars Docs: https://docs.flightsimulator.com/html/Programming_Tools/SimVars/Simulation_Variables.htm
     SIM_EVENT = 2  # Used for the SimEventEvent class. These Events trigger Simulation Events. Event IDs Docs: https://docs.flightsimulator.com/html/Programming_Tools/Event_IDs/Event_IDs.htm
     SIM_METHOD = 3 # Used for SimMethodEvent class. These Events trigger various other methods built into SimConnect. SimConnect API Docs: https://docs.flightsimulator.com/html/Programming_Tools/SimConnect/SimConnect_API_Reference.htm
     CUSTOM = 4     # Used for all classes that begin with Custom. These Events allow for arbitrary code to be used for more complicated Events.

class Operation(Enum):
     ADD = 0
     SUB = 1
     MUL = 2
     DIV = 3
     EXP = 4

# All Events run through an instance of the EventHandler.
class EventHandler:
     def __init__(self, requestTime: int = 10) -> None:
          self._sm = SimConnect()
          self._aq = AircraftRequests(self._sm, requestTime)
          self._ae = AircraftEvents(self._sm)
          self.usedEventID = []
          self.largestEventID = 0

     # TODO: Make code more rebust. 
     def newEventID(self) -> int | Response:
          responseID = self.largestEventID + 1
          if responseID in self.usedEventID:
               return Response(ErrorHandler.newResponseID, ResponseStatus.ERROR, "Event ID Conflict", True)
          else:
               return responseID
          
     # Must quit at end of program to properly run Events.
     def exit(self) -> Response:
          self._sm.exit()
          return Response(ErrorHandler.newResponseID, ResponseStatus.OK)
          
     # TODO: Make method to generate random event.

     @property
     def sm(self):
          return self._sm
     
     @property
     def aq(self):
          return self._aq
     
     @property
     def ae(self):
          return self._ae

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
                    case Operation.ADD:
                         valToSet = value + modifyValue
                    case Operation.SUB:
                         valToSet = value - modifyValue
                    case Operation.MUL:
                         valToSet = value * modifyValue
                    case Operation.DIV:
                         valToSet = value / modifyValue
                    case Operation.EXP:
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
                    if command == self._commands[-1]:
                         return self._evalCommand(command)
                    else:
                         self._evalCommand(command)

# Container for SimEvents.
class SimEventNotation:
     def __init__(self, event: str, *args) -> None:
          self._event = event
          self._args = args

     @property
     def event(self) -> str:
          return self._event
     
     @property
     def args(self) -> tuple:
          return self._args
               
# Class for Events that trigger Simulation Events. Event IDs Docs: https://docs.flightsimulator.com/html/Programming_Tools/Event_IDs/Event_IDs.htm
class SimEventEvent(Event):
     def __init__(self, eventHandler: EventHandler, eventID: int, name: str, events: SimEventNotation | list[SimEventNotation], displayName: str = None, description: str = None) -> None:
          super().__init__(eventID, name, displayName, description)
          self._eventType = EventType.SIM_EVENT
          self._ae = eventHandler.ae
          self._aq = eventHandler.aq
          self._events = events

     # Triggers the SimEvent.
     def _triggerSimEvent(self, event: SimEventNotation) -> Response:
          toTrigger = self._ae.find(event.event)
          if toTrigger is None:
               return Response(ErrorHandler.newResponseID, ResponseStatus.WARNING, "Failed To Trigger Event")
          else:
               toTrigger(*event.args)
               return Response(ErrorHandler.newResponseID, ResponseStatus.OK)
          
     def run(self) -> Response:
          if type(self._events) == SimEventNotation:
               return self._triggerSimEvent(self._events)

          else:
               for event in self._events:
                    if event == self._events[-1]:
                         return self._triggerSimEvent(event)
                    else:
                         self._triggerSimEvent(event)

# Container for arguments for SimMethod.
class SimMethodArgument:
     def __init__(self, argValue, operation: Operation = None, modifyValue: str | int | float = None) -> None:
          self._argValue = argValue # Base value of the argument.
          self._operation = operation         # The operation between the value and modifyValue.
          self._modifyValue = modifyValue     # Value to modify the value with.

     @property
     def argValue(self) -> str:
          return self._argValue
     
     @property
     def operation(self) -> tuple:
          return self._operation
     
     @property
     def modifyValue(self) -> tuple:
          return self._modifyValue

# Container for SimMethods.
class SimMethodNotation:
     def __init__(self, method: str, *args: SimMethodArgument) -> None:
          self._method = method
          self._args = args

     @property
     def method(self) -> str:
          return self._method
     
     @property
     def args(self) -> tuple:
          return self._args

class SimMethodEvent(Event):
     def __init__(self, eventHandler: EventHandler, eventID: int, name: str, methods: SimMethodNotation | list[SimMethodNotation], displayName: str = None, description: str = None) -> None:
          super().__init__(eventID, name, displayName, description)
          self._eventType = EventType.SIM_METHOD
          self._sm = eventHandler.sm
          self._aq = eventHandler.aq
          self._methods = methods

     def _evalArgument(self, arg: SimMethodArgument) -> any:
          print(arg)
          argValue = arg.argValue
          modifyValue = arg.modifyValue
          operation = arg.operation

          if type(modifyValue) == str: 
               modifyValue = self._aq.get(modifyValue)
               
          outValue = argValue

          if operation and modifyValue:
               match operation:
                    case Operation.ADD:
                         outValue = argValue + modifyValue
                    case Operation.SUB:
                         outValue = argValue - modifyValue
                    case Operation.MUL:
                         outValue = argValue * modifyValue
                    case Operation.DIV:
                         outValue = argValue / modifyValue
                    case Operation.EXP:
                         outValue = argValue ** modifyValue

          return outValue

     def _convertArgumentsToValues(self, args: tuple[SimMethodArgument]) -> tuple:
          out = []
          for arg in args:
               out.append(self._evalArgument(arg))

          return tuple(out)

     def _callSimMethod(self, method: SimMethodNotation) -> Response:
          toCall = getattr(self._sm, method.method)
          try: 
               print(*self._convertArgumentsToValues(method.args))
               toCall(*self._convertArgumentsToValues(method.args))
               return Response(ErrorHandler.newResponseID, ResponseStatus.OK)
          except:
               return Response(ErrorHandler.newResponseID, ResponseStatus.WARNING, "Failed To call SimMethod")


     def run(self): 
          if type(self._methods) == SimMethodNotation:
               return self._callSimMethod(self._methods)
          else:
               for method in self._methods:
                    if method == self._methods[-1]:
                         return self._callSimMethod(method)
                    else:
                         self._callSimMethod(method)

# ----------------------------- TESTING CODE ----------------------------- #

# import time

# ev = EventHandler(2000)

# # event = SimEventEvent(ev, ev.newEventID(), "test", [SimEventNotation("AP_ALT_VAR_SET_ENGLISH", 8000), SimEventNotation("THROTTLE_40")])
# # time.sleep(3)
# # print(event.run())

# # bta = SimVarEvent(ev, ev.newEventID(), "test", [SimVarNotation("PLANE_ALTITUDE", "PLANE_ALTITUDE", Operation.ADD, 4000), SimVarNotation("AIRSPEED_TRUE", 0)])
# # time.sleep(3)
# # print(bta.run())

# method = SimMethodEvent(ev, ev.newEventID(), "test", SimMethodNotation("createSimulatedObject", SimMethodArgument("Windsock"), SimMethodArgument(0, Operation.ADD, "PLANE_LATITUDE"), SimMethodArgument(0, Operation.ADD, "PLANE_LONGITUDE"), SimMethodArgument(ev.sm.new_request_id()), SimMethodArgument(360), SimMethodArgument(1), SimMethodArgument(0, Operation.ADD, "PLANE_ALTITUDE"), SimMethodArgument(0), SimMethodArgument(0), SimMethodArgument(0)))
# # ev.sm.createSimulatedObject("A330-BelugaXL", "PLANE_LATITUDE", "PLANE_LONGITUDE", ev.sm.new_request_id, 360, 0, "PLANE_ALTITUDE", 0, 0, 0)
# time.sleep(3)
# print(method.run())
# ev.exit()