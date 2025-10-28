from enum import Enum

class States(Enum):
    NEW = "NEW"
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"