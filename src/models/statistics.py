class Statistics:
    def __init__(self) -> None:
        self.processed_items: int = 0
        self.sorted_items: int = 0
        self.manual_processing_items: int = 0
        self.scan_errors: int = 0
        self.routing_errors: int = 0
        self.buffer_usage: int = 0
        self.conveyor_load: dict[int, int] = {}
        self.output_bin_load: dict[int, int] = {}
        self.simulation_time: float = 0.0

    def register_processed_item(self) -> None:
        self.processed_items += 1

    def register_sorted_item(self) -> None:
        self.sorted_items += 1

    def register_manual_processing_item(self) -> None:
        self.manual_processing_items += 1

    def register_scan_error(self) -> None:
        self.scan_errors += 1

    def register_routing_error(self) -> None:
        self.routing_errors += 1

    def register_buffer_usage(self) -> None:
        self.buffer_usage += 1

    def generate_report(self) -> dict[str, object]:
        average_conveyor_load = (
            sum(self.conveyor_load.values()) / len(self.conveyor_load)
            if self.conveyor_load
            else 0
        )

        average_output_bin_load = (
            sum(self.output_bin_load.values()) / len(self.output_bin_load)
            if self.output_bin_load
            else 0
        )

        throughput = (
            self.processed_items / self.simulation_time
            if self.simulation_time > 0
            else 0
        )

        success_rate = (
            self.sorted_items / self.processed_items * 100
            if self.processed_items > 0
            else 0
        )

        return {
            "processed_items": self.processed_items,
            "sorted_items": self.sorted_items,
            "manual_processing_items": self.manual_processing_items,
            "scan_errors": self.scan_errors,
            "routing_errors": self.routing_errors,
            "buffer_usage": self.buffer_usage,
            "conveyor_load": self.conveyor_load,
            "output_bin_load": self.output_bin_load,
            "average_conveyor_load": average_conveyor_load,
            "average_output_bin_load": average_output_bin_load,
            "simulation_time": self.simulation_time,
            "throughput": throughput,
            "success_rate": success_rate,
        }

    def reset(self) -> None:
        self.processed_items = 0
        self.sorted_items = 0
        self.manual_processing_items = 0
        self.scan_errors = 0
        self.routing_errors = 0
        self.buffer_usage = 0
        self.conveyor_load.clear()
        self.output_bin_load.clear()
        self.simulation_time = 0.0