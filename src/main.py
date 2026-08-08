from models.item import Item
from models.scanner import Scanner

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


if __name__ == "__main__":
    main()