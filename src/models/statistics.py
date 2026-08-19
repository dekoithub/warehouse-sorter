class Statistics:
    def __init__(self):
        self.processed_items = 0
        self.sorted_items = 0
        self.manual_processing_items = 0
        self.scan_errors = 0
        self.routing_errors = 0
        self.buffer_usage = 0
        self.conveyor_load = {}
        self.output_bin_load = {}
        self.simulation_time = 0.0

    def register_processed_item(self):
        self.processed_items += 1

    def register_sorted_item(self):
        self.sorted_items += 1

    def register_manual_processing_item(self):
        self.manual_processing_items += 1

    def register_scan_error(self):
        self.scan_errors += 1

    def register_routing_error(self):
        self.routing_errors += 1

    def register_buffer_usage(self):
        self.buffer_usage += 1

    def generate_report(self):
        return {
            "processed_items": self.processed_items,
            "sorted_items": self.sorted_items,
            "manual_processing_items": self.manual_processing_items,
            "scan_errors": self.scan_errors,
            "routing_errors": self.routing_errors,
            "buffer_usage": self.buffer_usage,
            "conveyor_load": self.conveyor_load,
            "output_bin_load": self.output_bin_load,
            "simulation_time": self.simulation_time,
        }

    def reset(self):
        self.processed_items = 0
        self.sorted_items = 0
        self.manual_processing_items = 0
        self.scan_errors = 0
        self.routing_errors = 0
        self.buffer_usage = 0
        self.conveyor_load.clear()
        self.output_bin_load.clear()
        self.simulation_time = 0.0