import time
from models.enums import ItemStatus, SensorStatus, WMSStatus

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
) -> Item:
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
) -> Item:
    controller.register_item(item)

    detected = sensor.detect_item(item)

    if not detected:
        controller.send_to_manual_processing(item)
        return item

    sensor_event = sensor.send_signal(item)

    controller.process_sensor_event(
        sensor_event,
        item,
    )

    if item.status != ItemStatus.MOVING:
        return item

    return process_conveyor_to_sorter(
        item,
        controller,
        sorter_sensor,
        sorter,
    )


def main() -> None:
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
        status=ItemStatus.CREATED,
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
        status=ItemStatus.CREATED,
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
        status=ItemStatus.CREATED,
        destination=None,
        location="Scanner",
    )

    fourth_item = Item(
        id=4,
        barcode="4601234567893",
        weight=2.0,
        width=220,
        height=120,
        length=280,
        category="Clothes",
        delivery_type="Courier",
        is_flammable=False,
        status=ItemStatus.CREATED,
        destination=None,
        location="Scanner",
    )

    fifth_item = Item(
        id=5,
        barcode="4601234567894",
        weight=1.8,
        width=210,
        height=110,
        length=260,
        category="Toys",
        delivery_type="Courier",
        is_flammable=False,
        status=ItemStatus.CREATED,
        destination=None,
        location="Scanner",
    )

    sixth_item = Item(
        id=6,
        barcode="4601234567895",
        weight=2.2,
        width=230,
        height=130,
        length=290,
        category="Sports",
        delivery_type="Courier",
        is_flammable=False,
        status=ItemStatus.CREATED,
        destination=None,
        location="Scanner",
    )

    seventh_item = Item(
        id=7,
        barcode="4601234567896",
        weight=1.9,
        width=210,
        height=120,
        length=270,
        category="Kitchen",
        delivery_type="Courier",
        is_flammable=False,
        status=ItemStatus.CREATED,
        destination=None,
        location="Scanner",
    )

    eighth_item = Item(
        id=8,
        barcode="4601234567897",
        weight=2.6,
        width=240,
        height=140,
        length=310,
        category="Office",
        delivery_type="Courier",
        is_flammable=False,
        status=ItemStatus.CREATED,
        destination=None,
        location="Scanner",
    )

    ninth_item = Item(
        id=9,
        barcode="4601234567898",
        weight=2.1,
        width=225,
        height=125,
        length=285,
        category="Garden",
        delivery_type="Courier",
        is_flammable=False,
        status=ItemStatus.CREATED,
        destination=None,
        location="Scanner",
    )

    tenth_item = Item(
        id=10,
        barcode="4601234567899",
        weight=2.3,
        width=235,
        height=135,
        length=295,
        category="Tools",
        delivery_type="Courier",
        is_flammable=False,
        status=ItemStatus.CREATED,
        destination=None,
        location="Scanner",
    )

    eleventh_item = Item(
        id=11,
        barcode="4601234567900",
        weight=1.7,
        width=205,
        height=115,
        length=255,
        category="Accessories",
        delivery_type="Courier",
        is_flammable=False,
        status=ItemStatus.CREATED,
        destination=None,
        location="Scanner",
    )

    twelfth_item = Item(
        id=12,
        barcode="4601234567901",
        weight=2.4,
        width=230,
        height=130,
        length=300,
        category="Decor",
        delivery_type="Courier",
        is_flammable=False,
        status=ItemStatus.CREATED,
        destination=None,
        location="Scanner",
    )

    items = [item, second_item, third_item, fourth_item]

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
    wms.register_route(fifth_item.barcode, 5)
    wms.register_route(sixth_item.barcode, 5)
    wms.register_route(seventh_item.barcode, 5)
    wms.register_route(eighth_item.barcode, 5)
    wms.register_route(ninth_item.barcode, 5)
    wms.register_route(tenth_item.barcode, 5)
    wms.register_route(eleventh_item.barcode, 5)
    wms.register_route(twelfth_item.barcode, 4)

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

    start_time = time.perf_counter()

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

    scanner.error_rate = 1.0

    process_item(
        fifth_item,
        controller,
        sensor,
        sorter_sensor,
        sorter,
    )

    scanner.error_rate = 0.0

    items.append(fifth_item)

    sorter.is_available = False

    process_item(
        sixth_item,
        controller,
        sensor,
        sorter_sensor,
        sorter,
    )

    sorter.is_available = True

    items.append(sixth_item)

    sorter.is_available = False

    process_item(
        seventh_item,
        controller,
        sensor,
        sorter_sensor,
        sorter,
    )

    process_item(
        eighth_item,
        controller,
        sensor,
        sorter_sensor,
        sorter,
    )

    sorter.is_available = True

    items.append(seventh_item)
    items.append(eighth_item)

    wms.is_available = False
    wms.status = WMSStatus.UNAVAILABLE

    process_item(
        ninth_item,
        controller,
        sensor,
        sorter_sensor,
        sorter,
    )

    wms.is_available = True
    wms.status = WMSStatus.AVAILABLE

    items.append(ninth_item)

    backup_buffer = Buffer(
        buffer_id=2,
        capacity=2,
    )

    controller.buffers.append(backup_buffer)

    conveyor.is_available = False

    process_item(
        tenth_item,
        controller,
        sensor,
        sorter_sensor,
        sorter,
    )

    conveyor.is_available = True

    items.append(tenth_item)

    sensor.is_active = False
    sensor.status = SensorStatus.INACTIVE

    process_item(
        eleventh_item,
        controller,
        sensor,
        sorter_sensor,
        sorter,
    )

    sensor.is_active = True
    sensor.status = SensorStatus.ACTIVE

    items.append(eleventh_item)

    process_item(
        twelfth_item,
        controller,
        sensor,
        sorter_sensor,
        sorter,
    )

    items.append(twelfth_item)

    end_time = time.perf_counter()

    statistics.simulation_time = end_time - start_time

    for current_item in items:
        print()
        print("=== Item result ===")
        print("Item id:", current_item.id)
        print("Status:", current_item.status)
        print("Destination:", current_item.destination)
        print("Location:", current_item.location)

    report = controller.update_statistics()

    if report is None:
        raise RuntimeError("Statistics report is unavailable")

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
    print("Simulation time:", report["simulation_time"])
    print("Throughput:", report["throughput"])
                    
if __name__ == "__main__":
    main()