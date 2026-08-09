from models.item import Item
from models.scanner import Scanner
from models.wms import WMS

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

if __name__ == "__main__":
    main()