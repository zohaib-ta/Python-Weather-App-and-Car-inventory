from datetime import datetime

class Vehicle:
    def __init__(self, vin, make, model, year, price, mileage, mot_expiry, tax_status, import_status=False):
        self.vin = vin
        self.make = make
        self.model = model
        self.year = year
        self.price = price
        self.mileage = mileage
        self.mot_expiry = datetime.strptime(mot_expiry, '%d/%m/%Y')
        self.tax_status = tax_status
        self.import_status = import_status
        self.sold = False
        self.sale_date = None
        self.buyer_name = None

    def mark_as_sold(self, buyer_name, sale_date):
        self.sold = True
        self.buyer_name = buyer_name
        self.sale_date = datetime.strptime(sale_date, '%d/%m/%Y')

    def __str__(self):
        import_str = "Imported" if self.import_status else "UK Domestic"
        sale_info = f" | Sold to {self.buyer_name} on {self.sale_date.strftime('%d/%m/%Y')}" if self.sold else ""
        return (f"{self.year} {self.make} {self.model} (VIN: {self.vin}) - £{self.price}\n"
                f"Mileage: {self.mileage} miles | MOT Expiry: {self.mot_expiry.strftime('%d/%m/%Y')} | "
                f"Tax: {self.tax_status} | Status: {import_str} {sale_info}")

class Inventory:
    def __init__(self):
        self.vehicles = []

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)
        print(f"Added: {vehicle}")

    def remove_vehicle(self, vin):
        for vehicle in self.vehicles:
            if vehicle.vin == vin:
                self.vehicles.remove(vehicle)
                print(f"Removed: {vehicle}")
                return
        print(f"Vehicle with VIN {vin} not found.")

    def list_inventory(self):
        if not self.vehicles:
            print("Inventory is empty.")
        else:
            for vehicle in self.vehicles:
                print(vehicle)

    def sell_vehicle(self, vin, buyer_name, sale_date):
        for vehicle in self.vehicles:
            if vehicle.vin == vin:
                if vehicle.sold:
                    print(f"Vehicle with VIN {vin} is already sold.")
                else:
                    vehicle.mark_as_sold(buyer_name, sale_date)
                    print(f"Sold: {vehicle}")
                return vehicle  # Return the vehicle object for sales recording
        print(f"Vehicle with VIN {vin} not found.")
        return None

    def search_vehicle(self, **kwargs):
        results = self.vehicles
        for key, value in kwargs.items():
            results = [vehicle for vehicle in results if getattr(vehicle, key) == value]
        return results

    def filter_vehicles(self, **kwargs):
        results = self.vehicles
        for key, value in kwargs.items():
            if isinstance(value, tuple) and len(value) == 2:  # range filter
                results = [vehicle for vehicle in results if value[0] <= getattr(vehicle, key) <= value[1]]
            else:
                results = [vehicle for vehicle in results if getattr(vehicle, key) == value]
        return results

class Sales:
    def __init__(self):
        self.sales_records = []

    def record_sale(self, vehicle):
        if vehicle.sold:
            self.sales_records.append({
                "vehicle": vehicle,
                "buyer_name": vehicle.buyer_name,
                "sale_date": vehicle.sale_date
            })
            print(f"Sale recorded: {vehicle} to {vehicle.buyer_name} on {vehicle.sale_date.strftime('%d/%m/%Y')}")
        else:
            print(f"Vehicle with VIN {vehicle.vin} has not been marked as sold.")

    def list_sales(self):
        if not self.sales_records:
            print("No sales records found.")
        else:
            for record in self.sales_records:
                vehicle = record['vehicle']
                buyer_name = record['buyer_name']
                sale_date = record['sale_date'].strftime('%d/%m/%Y')
                print(f"Sold to {buyer_name} on {sale_date}: {vehicle}")

# Sample Data
inventory = Inventory()
sales = Sales()

# Adding vehicles to inventory
inventory.add_vehicle(Vehicle("SCBLC37F44CX09327", "Bentley", "Continental GT", 2018, 120000, 15000, "01/07/2024", "Taxed"))
inventory.add_vehicle(Vehicle("SALLDHMF7HA463248", "Land Rover", "Defender", 2016, 30000, 60000, "12/08/2023", "Taxed", import_status=True))
inventory.add_vehicle(Vehicle("WF0AXXWPMAFS40250", "Ford", "Fiesta", 2020, 15000, 10000, "25/12/2024", "Not Taxed"))

# Listing current inventory
print("\nCurrent Inventory:")
inventory.list_inventory()

# Selling a vehicle
sold_vehicle = inventory.sell_vehicle("SCBLC37F44CX09327", "John Smith", "15/07/2023")

# Recording the sale
if sold_vehicle:
    sales.record_sale(sold_vehicle)

# Listing sales records
print("\nSales Records:")
sales.list_sales()

# Listing inventory after sale
print("\nUpdated Inventory:")
inventory.list_inventory()

# Filtering vehicles based on criteria
print("\nFiltered Inventory (Price between £10,000 and £40,000):")
filtered_vehicles = inventory.filter_vehicles(price=(10000, 40000))
for vehicle in filtered_vehicles:
    print(vehicle)

# Searching for a specific vehicle
print("\nSearching for a specific vehicle (Model: Fiesta):")
search_results = inventory.search_vehicle(model="Fiesta")
for vehicle in search_results:
    print(vehicle)


