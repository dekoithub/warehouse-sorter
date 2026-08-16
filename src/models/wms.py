class WMS:
    def __init__(self, routes, available_destinations, is_available):
        self.routes = routes
        self.available_destinations = available_destinations
        self.request_count = 0
        self.status = "AVAILABLE" if is_available else "UNAVAILABLE"
        self.is_available = is_available

    def register_route(self, barcode, destination):
        self.routes[barcode] = destination

    def get_destination(self, barcode):
        self.request_count += 1
        return self.routes.get(barcode)

    def remove_route(self, barcode):
        self.routes.pop(barcode, None)

    def is_destination_available(self, destination):
        return destination in self.available_destinations

    def report_status(self):
        return self.status