import json

from simulation.config import SimulationConfig
from simulation.runner import SimulationRunner


def main() -> None:
    config = SimulationConfig(
        duration_seconds=60.0,
        item_interval_seconds=0.5,
        scan_duration_seconds=0.1,
        scanner_capacity=1,
        scanner_error_rate=0.0,
        conveyor_length_meters=10.0,
        conveyor_speed_mps=2.0,
        conveyor_capacity=10,
        buffer_capacity=100,
        buffer_retry_interval_seconds=0.05,
        default_destination=1,
        sorter_duration_seconds=0.1,
        output_bin_capacity=1000,
    )

    runner = SimulationRunner(config)
    report = runner.run()

    print(
        json.dumps(
            report,
            indent=4,
        )
    )


if __name__ == "__main__":
    main()