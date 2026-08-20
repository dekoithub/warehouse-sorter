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


def process_conveyor_to_sorter(
        item: Item,
        controller: Controller,
        sorter_sensor: Sensor,
        sorter: Sorter,
):
    item_conveyor = None 

    for conveyor in controller.conveyors:
        if item in conveyor.items:
            item_conveyor = conveyor
            break

    if item_conveyor is None:
        controller.send_to_manual_processing(item)
        return item

    released_item = item_conveyor.release_item()

    if not item_conveyor.items:
        item_conveyor.stop()

    if released_item is None:
        controller.send_to_manual_processing(item)
        return item

    released_item.update_location("Sorter Sensor")

    sorter_detected = sorter_sensor.detect_item(released_item)

    if not sorter_detected:
        controller.send_to_manual_processing(released_item)
        return released_item

    sorter_event = sorter_sensor.send_signal(released_item)

    controller.process_sorter_event(sorter_event, released_item, sorter)

    controller.update_statistics()

    return released_item


def process_item(
    item: Item,
    controller: Controller,
    sensor: Sensor,
    sorter_sensor: Sensor,
    sorter: Sorter,
):
    controller.register_item(item)

    detected = sensor.detect_item(item)

    if not detected:
        return item

    sensor_event = sensor.send_signal(item)

    controller.process_sensor_event(
        sensor_event,
        item,
    )

    if item.status != "MOVING":
        return item

    return process_conveyor_to_sorter(
        item,
        controller,
        sorter_sensor,
        sorter,
    )


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
        location="Scanner",
    )

    third_item = Item(
        id=3,
        barcode="4601234567892",
        weight=3.0,
        width=300,
        height=180,
        length=350,
        category="Home",
        delivery_type="Courier",
        is_flammable=False,
        status="CREATED",
        destination=None,
        location="Scanner",
    )

    items = [item, second_item, third_item]

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
    wms.register_route(second_item.barcode, 5)
    wms.register_route(third_item.barcode, 5)

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

    for current_item in items:
        process_item(
            current_item,
            controller,
            sensor,
            sorter_sensor,
            sorter,
        )

    output_bin.remove_all_items()

    buffered_item = controller.release_from_buffer(buffer)

    if buffered_item is not None:
        process_conveyor_to_sorter(
            buffered_item,
            controller,
            sorter_sensor,
            sorter,
        )

    for current_item in items:
        print()
        print("=== Item result ===")
        print("Item id:", current_item.id)
        print("Status:", current_item.status)
        print("Destination:", current_item.destination)
        print("Location:", current_item.location)

    report = controller.update_statistics()

    print()
    print("=== System report ===")
    print("Processed items:", report["processed_items"])
    print("Sorted items:", report["sorted_items"])
    print("Manual processing items:", report["manual_processing_items"])
    print("Scan errors:", report["scan_errors"])
    print("Routing errors:", report["routing_errors"])
    print("Buffer usage:", report["buffer_usage"])
    print("Conveyor load:", report["conveyor_load"])
    print("OutputBin load:", report["output_bin_load"])
    print("Success rate:", report["success_rate"])
                    
if __name__ == "__main__":
    main()