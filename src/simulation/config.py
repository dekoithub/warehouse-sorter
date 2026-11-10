from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SimulationConfig:
    duration_seconds: float
    item_interval_seconds: float = 1.0
    scan_duration_seconds: float = 0.1
    scanner_capacity: int = 1
    conveyor_length_meters: float = 10.0
    conveyor_speed_mps: float = 2.0
    conveyor_capacity: int = 10
    buffer_capacity: int = 100
    buffer_retry_interval_seconds: float = 0.05
    default_destination: int = 1
    destination_count: int = 1
    sorter_duration_seconds: float = 0.1
    sorter_capacity: int = 1
    output_bin_capacity: int = 100
    scanner_error_rate: float = 0.0

    def __post_init__(self) -> None:
        if self.duration_seconds <= 0:
            raise ValueError(
                "Simulation duration must be greater than 0"
            )

        if self.destination_count <= 0:
            raise ValueError(
                "Destination count must be greater than 0"
            )

        if self.item_interval_seconds <= 0:
            raise ValueError(
                "Item interval must be greater than 0"
            )

        if self.scan_duration_seconds <= 0:
            raise ValueError(
                "Scan duration must be greater than 0"
            )

        if self.scanner_capacity <= 0:
            raise ValueError(
                "Scanner capacity must be greater than 0"
            )

        if self.conveyor_length_meters <= 0:
            raise ValueError(
                "Conveyor length must be greater than 0"
            )

        if self.conveyor_speed_mps <= 0:
            raise ValueError(
                "Conveyor speed must be greater than 0"
            )

        if self.conveyor_capacity <= 0:
            raise ValueError(
                "Conveyor capacity must be greater than 0"
            )

        if self.buffer_capacity <= 0:
            raise ValueError(
                "Buffer capacity must be greater than 0"
            )

        if self.buffer_retry_interval_seconds <= 0:
            raise ValueError(
                "Buffer retry interval must be greater than 0"
            )

        if self.default_destination <= 0:
            raise ValueError(
                "Default destination must be greater than 0"
            )

        if self.sorter_duration_seconds <= 0:
            raise ValueError(
                "Sorter duration must be greater than 0"
            )

        if self.sorter_capacity <= 0:
            raise ValueError(
                "Sorter capacity must be greater than 0"
            )

        if self.output_bin_capacity <= 0:
            raise ValueError(
                "Output bin capacity must be greater than 0"
            )

        if not 0.0 <= self.scanner_error_rate <= 1.0:
            raise ValueError(
                "Scanner error rate must be between 0 and 1"
            )