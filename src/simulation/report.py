from models.statistics import StatisticsReport


class SimulationReport(StatisticsReport):
    generated_items: int

    scanner_current_queue: int
    scanner_in_use: int
    scanner_max_queue: int
    scanner_average_wait_seconds: float

    conveyor_current_queue: int
    conveyor_in_use: int

    sorter_current_queue: int
    sorter_in_use: int

    buffer_current_load: int
    output_bin_current_load: int

    arrival_rate_items_per_second: float
    arrival_rate_items_per_hour: float

    sorted_throughput_items_per_second: float
    sorted_throughput_items_per_hour: float

    in_flight_items: int
