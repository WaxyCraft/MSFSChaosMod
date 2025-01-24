from enum import Enum

class ResponseStatus(Enum):
     OK = 0
     WARNING = 1
     UNKNOWN_WARNING = 2
     ERROR = 3
     UNKNOWN_ERROR = 4
  
class Response:
     def __init__(self, responseID: int, status: ResponseStatus, comment: str = None, fatal: bool = False) -> None:
          self.responseID = responseID
          self.status = status
          self.note = comment
          self.fatal = False

     def __str__(self) -> str:
          return f"{"FATAL" if self.fatal else "NONFATAL"} {self.status.name}: {self.note if self.note else "No Comment Provided"}"
     
class ErrorHandler:
     usedResponseID = []
     largestResponseID = 0

     # TODO: Fix this method.
     def newResponseID() -> int | Response:
          responseID = ErrorHandler.largestResponseID + 1
          if responseID in ErrorHandler.largestResponseID:
               return Response(-1, ResponseStatus.ERROR, "Response ID Conflict", True)
          else:
               return responseID