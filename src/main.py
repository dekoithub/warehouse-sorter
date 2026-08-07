from models.item import Item

def main():
    item = Item(
        id=1,
        barcode="4601234567890",
        weight=2.4,
        width=250,
        height=150,
        length=300,
    )

    print(item.__dict__)

if __name__ == "__main__":
    main()