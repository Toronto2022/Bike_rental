import csv
import datetime

#represents a type of bike
class Bike:
    def __init__(self, quantity): #Initializes a Bike object with a given quantity.
        self.quantity = quantity
#Checks if the requested quantity
    def check_availability(self, requested_quantity):
        return self.quantity >= requested_quantity
#Decreases the quantity of bikes
    def decrease_quantity(self, requested_quantity):
        self.quantity -= requested_quantity
#Increases the quantity of bikes
    def increase_quantity(self, returned_quantity):
        self.quantity += returned_quantity


class BikeRentalShop:

#Initializes a BikeRentalShop object, loads the inventory and revenue data from CSV files.
    def __init__(self):
        self.inventory_file = "inventory.csv"
        self.revenue_file = "revenue.csv"
        self.inventory = {}
        self.rental_prices = {
            'hourly': 5,
            'daily': 20,
            'weekly': 60
        }
        self.revenue = 0
        self.current_rentals = {}

        self.load_inventory()
        self.load_revenue()

# Loads the inventory data from the "inventory.csv" file or creates a new inventory if the file doesn't exist
    def load_inventory(self):
        try:
            with open(self.inventory_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    rental_type = row['RentalType']
                    quantity = int(row['Quantity'])
                    self.inventory[rental_type] = Bike(quantity)
        except FileNotFoundError:
            self.inventory = {
                'hourly': Bike(7),
                'daily': Bike(49),
                'weekly': Bike(17)
            }
            self.save_inventory()

# Saves the current inventory data
    def save_inventory(self):
        with open(self.inventory_file, 'w', newline='') as file:
            fieldnames = ['RentalType', 'Quantity']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for rental_type, bike in self.inventory.items():
                writer.writerow({'RentalType': rental_type, 'Quantity': bike.quantity})

#Loads the revenue data from the "revenue.csv" file or initializes the revenue if the file doesn't exist.
    def load_revenue(self):
        try:
            with open(self.revenue_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.revenue = float(row['Revenue'])
        except FileNotFoundError:
            self.revenue = 0.0
            self.save_revenue()

# Saves the current revenue data
    def save_revenue(self):
        with open(self.revenue_file, 'w', newline='') as file:
            fieldnames = ['Revenue']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'Revenue': str(self.revenue)})

# Displays the current inventory of bikes
    def display_inventory(self):
        print("Current Bike Inventory:")
        for rental_type, bike in self.inventory.items():
            print(f"{rental_type.capitalize()}: {bike.quantity}")

#Calculates the rental time and based on the rental type and period.
    def get_rental_time(self, rental_type, rental_period):
        if rental_type == "hourly":
            rental_time = rental_period
            time_unit = "hour(s)"
        elif rental_type == "daily":
            rental_time = rental_period * 24
            time_unit = "day(s)"
        elif rental_type == "weekly":
            rental_time = rental_period * 24 * 7
            time_unit = "week(s)"
        return rental_time, time_unit

#Calculates the rental cost based on the rental type, period, and rental hours
    def calculate_rental_cost(self, rental_type, rental_period, rental_hours=None):
        if rental_hours is None:
            rental_hours = rental_period

        rental_price = self.rental_prices[rental_type]
        rental_cost = rental_price * rental_period

        if rental_hours > rental_period:
            # Calculate additional hours
            additional_hours = rental_hours - rental_period
            additional_cost = additional_hours * rental_price
            additional_cost = additional_hours * rental_price * 1.5
            rental_cost += additional_cost
        return rental_cost

#Checks if the requested number of bikes is available
    def is_available(self, rental_type, requested_quantity):
        bike = self.inventory.get(rental_type)
        return bike and bike.check_availability(requested_quantity)

#Reserves the bikes for rental by decreasing the inventory quantity.
    def reserve_bikes(self, rental_type, requested_quantity):
        bike = self.inventory.get(rental_type)
        if bike:
            bike.decrease_quantity(requested_quantity)

#Releases the bikes that were rented by increasing the quantity
    def release_bikes(self, rental_type, returned_quantity):
        bike = self.inventory.get(rental_type)
        if bike:
            bike.increase_quantity(returned_quantity)

#Processes the bike rental by taking input from the user, checking availability, calculating cost, reserving bikes, and updating revenue
    def process_rental(self):
        rental_type = input("What type of rental would you like? (hourly, daily, weekly, or family): ")
        rental_quantity = int(input("How many bikes would you like to rent? "))
        rental_duration = int(input("How many hours/days/weeks would you like to rent for? "))

        # Check if the requested number of bikes is available
        if not self.is_available(rental_type, rental_quantity):
            print("Sorry, we don't have that many bikes available for {} rental.".format(rental_type))
            return

        # Calculate rental cost
        rental_cost = self.calculate_rental_cost(rental_type, rental_duration)

        # Reserve the bikes
        self.reserve_bikes(rental_type, rental_quantity)

        # Update revenue
        self.revenue += rental_cost
        self.save_revenue()

        # Display rental confirmation
        print("You have rented {} bike(s) for {} {}.".format(rental_quantity, rental_duration, rental_type))
        print("The total cost of your rental is ${}.".format(rental_cost))
        print("Please return the bikes in good condition.")

# Processes the return of rented bikes by taking input from the user, releasing bikes, calculating cost, and updating revenue.
    def process_return(self):
        rental_type = input("What type of rental did you have? (hourly, daily, weekly, or family): ")
        rental_quantity = int(input("How many bikes did you rent? "))
        rental_duration = int(input("How many hours/days/weeks did you rent for? "))

        return_time = datetime.datetime.now()
        rental_duration_str = ""
        if rental_type == "hourly":
            rental_duration_str = "{} hour(s)".format(rental_duration)
        elif rental_type == "daily":
            rental_duration_str = "{} day(s)".format(rental_duration)
        elif rental_type == "weekly":
            rental_duration_str = "{} week(s)".format(rental_duration)

        # Release the bikes
        self.release_bikes(rental_type, rental_quantity)

        # Calculate rental cost
        rental_cost = self.calculate_rental_cost(rental_type, rental_duration)

        # Update revenue
        self.revenue += rental_cost
        self.save_revenue()

        # Display rental summary
        print("You rented {} bike(s) for {}.".format(rental_quantity, rental_duration_str))
        print("You returned the bike(s) at {}.".format(return_time))
        print("Your rental cost is ${}.".format(rental_cost))

# Runs the main loop, displaying a menu of options and executing the selected action.
    def run(self):
        print("Inventory loaded successfully.")
        while True:
            print("\nBike Rental Shop")
            print("1. Display available bikes")
            print("2. Rent a bike")
            print("3. Return a bike")
            print("4. Display shop revenue")
            print("5. Exit")

            choice = input("Enter your choice (1-5): ")
            if choice == "1":
                self.display_inventory()
            elif choice == "2":
                self.process_rental()
            elif choice == "3":
                self.process_return()
            elif choice == "4":
                print("Shop revenue: ${}".format(self.revenue))
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")

        self.save_inventory()

if __name__ == "__main__":
    shop = BikeRentalShop() #object of class BikeRentalShop
    shop.run() #calls run method to start the program

