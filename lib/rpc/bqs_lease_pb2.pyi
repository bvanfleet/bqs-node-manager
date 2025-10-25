from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LeaseRequest(_message.Message):
    __slots__ = ("callsign", "nodeId")
    CALLSIGN_FIELD_NUMBER: _ClassVar[int]
    NODEID_FIELD_NUMBER: _ClassVar[int]
    callsign: str
    nodeId: int
    def __init__(self, callsign: _Optional[str] = ..., nodeId: _Optional[int] = ...) -> None: ...

class Lease(_message.Message):
    __slots__ = ("nodeId", "expiry", "callsign")
    NODEID_FIELD_NUMBER: _ClassVar[int]
    EXPIRY_FIELD_NUMBER: _ClassVar[int]
    CALLSIGN_FIELD_NUMBER: _ClassVar[int]
    nodeId: int
    expiry: int
    callsign: str
    def __init__(self, nodeId: _Optional[int] = ..., expiry: _Optional[int] = ..., callsign: _Optional[str] = ...) -> None: ...
