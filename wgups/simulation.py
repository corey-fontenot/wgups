import sys
import time
from wgups.clock import Clock
from wgups.truck import Truck
from wgups.location import Location
from data_structures.hashtable import HashTable
from data_structures.queue import Queue
from data_structures.graph import Graph


class Simulation:
    def __init__(self, start_time, delayed_flight_time, table_size):
        self._start_time = start_time
        self._clock = Clock(0, start_time)
        self._packages = HashTable(table_size)
        self._active_trucks = []
        self._trucks = Queue()
        self.simulation_over = False
        self._delayed_flight_time = Clock.seconds_since_start(delayed_flight_time, start_time)
        self._delayed_packages_departed = False
        self._total_miles = 0.0
        self.locations = Graph()
        self.wrong_address_fixed = False

    def add_package(self, package):
        self._packages.insert(package)

    def setup(self, num_trucks, packages_per_truck, truck_mph, start_of_day, end_of_day):
        truck_list = []
        for truck_id in range(1, num_trucks + 1):
            truck_list.append(Truck(truck_id, packages_per_truck, truck_mph, start_of_day, self.locations.get_vertex_by_index(0).data))

        truck_queue = Queue()
        for truck in Truck.sort_packages([x for x in self._packages], truck_list, start_of_day, end_of_day):
            # Add location data for packages in truck
            truck.set_locations(self.locations)
            truck.find_route()

            # Add truck to truck queue
            self._trucks.push(truck)

    def main_menu(self):
        selection = 0
        min_choice = 1
        max_choice = 3
        print("-------------------------------------------------------------------------------------------------------")
        while selection not in range(min_choice, max_choice + 1):
            print()
            print("1.\tPrint Package Data")
            print("2.\tMove Time Forward")
            print("3.\tExit Application")
            print()

            selection = int(input("Enter Selection: "))

        if selection == 1:
            self.package_menu()
        elif selection == 2:
            self.clock_menu()
        elif selection == 3:
            sys.exit()

    def package_menu(self):
        selection = 0
        min_choice = 1
        max_choice = 3
        while selection not in range(min_choice, max_choice + 1):
            print()
            print("1.\tPrint package by ID")
            print("2.\tPrint all packages")
            print("3.\tMain Menu")
            print()

            selection = int(input("Enter Selection: "))

        if selection == 1:
            selection = None
            while not isinstance(selection, int):
                print()
                selection = int(input("Enter Package ID: "))
            package = self._packages.search(selection)
            package.print(self._start_time)
        elif selection == 2:
            for package in self._packages:
                package.print(self._start_time)
        elif selection == 3:
            self.main_menu()

    def clock_menu(self):
        selection = 0
        min_choice = 1
        max_choice = 4
        while selection not in range(min_choice, max_choice + 1):
            print()
            print("1.\tHours")
            print("2.\tMinutes")
            print("3.\tSeconds")
            print("4.\tMain Menu")
            print()

            selection = int(input("Enter Selection: "))

        if selection == 1:
            num_hours = int(input("How many hours? "))
            time_amount = self._clock.forward_hours(num_hours)
            self.advance_simulation(time_amount)
        elif selection == 2:
            num_minutes = int(input("How many minutes? "))
            time_amount = self._clock.forward_minutes(num_minutes)
            self.advance_simulation(time_amount)
        elif selection == 3:
            num_seconds = int(input("How many seconds? "))
            time_amount = self._clock.forward_seconds(num_seconds)
            self.advance_simulation(time_amount)
        elif selection == 4:
            self.main_menu()

    def start_simulation(self):
        self._active_trucks.append(self._trucks.pop())
        for truck in self._active_trucks:
            truck.start_route(self._clock.time)
        while not self.simulation_over:
            self.main_menu()

    def print_summary(self):
        print(f"Total Distance: {self._total_miles:.2f} Miles")

        late_packages = 0
        print("-------------------------------------------------------------------------------------------------------")
        print("Late Packages:")
        for package in self._packages:
            if package.time_delivered is not None and package.time_delivered > package.deadline:
                late_packages += 1
                package.print(self._start_time)
        print(f"Total Late Packages: {late_packages}")
        print("-------------------------------------------------------------------------------------------------------")
        print("Undelivered Packages:")
        undelivered_packages = 0
        for package in self._packages:
            if package.status != "DELIVERED":
                undelivered_packages += 1
                package.print(self._start_time)
        print(f"Total Undelivered Packages: {undelivered_packages}")

    def advance_simulation(self, time_amount):
        # Run simulation for amount of time selected in clock menu
        while self._clock.time < time_amount and not self.simulation_over:

            # advance time forward
            self._clock.advance_time()

            if self._clock.time >= Clock.seconds_since_start("10:20 AM", self._start_time) \
                    and not self.wrong_address_fixed:
                new_location = Location("410 S State St", "Salt Lake City", "UT", "84111", "")
                self._packages.search(9).location = new_location
                self.wrong_address_fixed = True
                print(f"{Clock.to_time_string(self._clock.time, self._start_time)} : Package 9 address changed to {new_location}")

            # for each truck update truck and package data
            for truck in self._active_trucks:

                # move truck for one second
                self._total_miles += truck.move_truck()

                # if truck distance is greater or equal to distance to next location
                if truck.distance_traveled >= truck.next_location[1]:

                    # deliver packages for current location
                    delivered_packages = [x for x in truck.get_package_list() if x.location == truck.next_location[0].data]
                    for package in delivered_packages:
                        truck.deliver_package(package)
                        # set status of delivered package to delivered
                        self._packages.search(package.package_id).status = "DELIVERED"

                        # set time delivered for delivered package to current time
                        self._packages.search(package.package_id).time_delivered = self._clock.time

                        # Display information about current delivery
                        print(f"{Clock.to_time_string(self._clock.time, self._start_time)} : Package {package.package_id} "
                              f"delivered to {truck.next_location[0].data.name}, {truck.next_location[0].data}")

                        # wait a short time so that delivery activity can be read more easily
                        time.sleep(.2)

                    # Get truck's next location
                    truck.get_next_location(self._clock.time)

                    # if truck's route is done, remove it from active trucks
                    if truck.is_route_done():
                        self._active_trucks.remove(truck)

            # When delayed packages arrive send out second truck
            if self._clock.time >= self._delayed_flight_time and not self._delayed_packages_departed:
                self._active_trucks.append(self._trucks.pop())
                self._delayed_packages_departed = True
                self._active_trucks[-1].start_route(self._clock.time)

            # If active trucks is less than 2 and delayed packages have left send out next truck
            if self._delayed_packages_departed and len(self._active_trucks) < 2 and not self._trucks.is_empty():
                self._active_trucks.append(self._trucks.pop())
                self._active_trucks[-1].start_route(self._clock.time)

            # If not more active trucks, end simulation
            if len(self._active_trucks) == 0:
                self.simulation_over = True
                self.print_summary()
                break

        # Separator for better output readability
        print("-------------------------------------------------------------------------------------------------------")

        # Print data for each package
        for package in self._packages:
            package.print(self._start_time)
