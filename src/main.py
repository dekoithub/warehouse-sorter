from models.item import Item
from models.scanner import Scanner
from models.wms import WMS
from models.controller import Controller
from models.conveyor import Conveyor
from models.sensor import Sensor
from models.buffer import Buffer
from models.sorter import Sorter
from models.output_bin import OutputBin
from models.statistics import Statistics


def main():
    item = Item(
        id=1,
        barcode="4601234567890",
        weight=2.4,
        width=250,
        height=150,
        length=300,
        category="Electronics",
        delivery_type="Courier",
        is_flammable=False,
        status="CREATED",
        destination=None,
        location="Scanner",
    )

    second_item = Item(
        id=2,
        barcode="4601234567891",
        weight=1.5,
        width=200,
        height=100,
        length=250,
        category="Books",
        delivery_type="Courier",
        is_flammable=False,
        status="CREATED",
        destination=None,
        location="Sorter",
    )

    scanner = Scanner(
        scanner_id=1,
        is_active=True,
        error_rate=0.0,
    )

    wms = WMS(
        routes={},
        available_destinations=[1, 2, 3, 4, 5],
        is_available=True,
    )

    wms.register_route(item.barcode, 5)

    controller = Controller(
        scanner=scanner,
        wms=wms,
    )

    conveyor = Conveyor(
        conveyor_id=1,
        speed=1.5,
        capacity=2,
        is_available=True,
    )

    controller.conveyors.append(conveyor)

    sensor = Sensor(
        sensor_id=1,
        position="Scanner",
        is_active=True,
    )

    sorter_sensor = Sensor(
        sensor_id=2,
        position="Sorter",
        is_active=True,
    )

    buffer = Buffer(
        buffer_id=1,
        capacity=2,
    )

    sorter = Sorter(
        sorter_id=1,
        supported_directions=[1, 2, 3, 4, 5],
        is_available=True,
    )

    output_bin = OutputBin(
        bin_id=5,
        capacity=2,
    )

    statistics = Statistics()

    controller.buffers.append(buffer)
    controller.output_bins.append(output_bin)
    controller.statistics = statistics

    controller.register_item(item)

    detected = sensor.detect_item(item)

    if detected:
        sensor_event = sensor.send_signal(item)

        destination = controller.process_sensor_event(
            sensor_event,
            item,
        )

        if destination is not None:
            released_item = conveyor.release_item()

            if not conveyor.items:
                conveyor.stop()

            if released_item is not None:
                released_item.update_location("Sorter Sensor")

                sorter_detected = sorter_sensor.detect_item(
                    released_item
                )

                if sorter_detected:
                    sorter_event = sorter_sensor.send_signal(
                        released_item
                    )

                    result = controller.process_sorter_event(
                        sorter_event,
                        released_item,
                        sorter,
                    )

                    print("=== Final result ===")
                    print("Result item:", result.id if result is not None else None,)
                    print("Item status:", item.status)
                    print("Item destination:", item.destination)
                    print("Item location:", item.location)
                    print("Sorter direction:", sorter.current_direction,)
                    print("OutputBin load:", output_bin.current_load,)
                    print("OutputBin items:", [stored_item.id for stored_item in output_bin.items],)
                    print("Processed items:", statistics.processed_items,)
                    print("Sorted items:", statistics.sorted_items,)
                    
if __name__ == "__main__":
    main()