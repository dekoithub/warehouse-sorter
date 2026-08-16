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
        error_rate=0.01,
    )

    wms = WMS(
        routes={},
        available_destinations=[1, 2, 3, 4, 5],
        is_available=True,
    )

    wms.register_route(item.barcode, 5)

    controller = Controller(
        scanner = scanner,
        wms=wms,
    )

    conveyor = Conveyor(
        conveyor_id=1,
        speed=1.5,
        capacity=2,
        is_available=True,
    )

    sensor = Sensor(
        sensor_id=1,
        position="Scanner",
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
        bin_id=1,
        capacity=2,
    )   

    statistics = Statistics()

if __name__ == "__main__":
    main()