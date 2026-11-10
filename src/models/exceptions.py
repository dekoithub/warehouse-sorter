class WarehouseError(Exception):
    pass


class EquipmentUnavailableError(WarehouseError):
    pass


class RouteNotFoundError(WarehouseError):
    pass


class BufferFullError(WarehouseError):
    pass


class UnsupportedDirectionError(WarehouseError):
    pass


class OutputBinNotFoundError(WarehouseError):
    pass


class OutputBinFullError(WarehouseError):
    pass
