import sys
import time
from wgups.clock import Clock


class Simulation:
    def __init__(self, start_time, packages, trucks, delayed_flight_time):
        self._start_time = start_time
        self._clock = Clock(0, start_time)
        self._packages = packages
        self._trucks = trucks
        self._active_trucks = []
        self.simulation_over = False
        self._delayed_flight_time = Clock.seconds_since_start(delayed_flight_time, start_time)
        self._delayed_packages_departed = False
        self._total_miles = 0.0

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

            # for each truck update truck and package data
            for truck in self._active_trucks:

                # move truck for one second
                self._total_miles += truck.move_truck()

                # if truck distance is greater or equal to distance to next location
                if truck.distance_traveled >= truck.next_location[1]:

                    # deliver packages for current location
                    for package_id in truck.deliver_packages(truck.next_location[0].data):

                        # set status of delivered package to delivered
                        self._packages.search(package_id).status = "DELIVERED"

                        # set time delivered for delivered package to current time
                        self._packages.search(package_id).time_delivered = self._clock.time

                        # Display information about current delivery
                        print(f"{Clock.to_time_string(self._clock.time, self._start_time)} : Package {package_id} "
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
