from enum import StrEnum


class ItemStatus(StrEnum):
    CREATED = "CREATED"
    SCANNING = "SCANNING"
    ROUTING = "ROUTING"
    MOVING = "MOVING"
    BUFFERED = "BUFFERED"
    SORTED = "SORTED"
    MANUAL_PROCESSING = "MANUAL_PROCESSING"
    ERROR = "ERROR"

class SensorStatus(StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    ERROR = "ERROR"

class BufferStatus(StrEnum):
    EMPTY = "EMPTY"
    OCCUPIED = "OCCUPIED"
    FULL = "FULL"
    ERROR = "ERROR"

class OutputBinStatus(StrEnum):
    EMPTY = "EMPTY"
    OCCUPIED = "OCCUPIED"
    FULL = "FULL"

class SorterStatus(StrEnum):
    IDLE = "IDLE"
    UNAVAILABLE = "UNAVAILABLE"
    ERROR = "ERROR"

class ConveyorStatus(StrEnum):
    STOPPED = "STOPPED"
    RUNNING = "RUNNING"
    UNAVAILABLE = "UNAVAILABLE"
    
class WMSStatus(StrEnum):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"