from wgups.clock import Clock


class Simulation:
    def __init__(self, start_time, packages, trucks):
        self._start_time = start_time
        self._clock = Clock(0, start_time)
        self._packages = packages
        self._trucks = trucks
        self._time_target = 0

    def main_menu(self):
        selection = 0
        min_choice = 1
        max_choice = 2
        while selection not in range(min_choice, max_choice + 1):
            print()
            print("1.\tPrint Package Data")
            print("2.\tMove Time Forward")
            print()

            selection = int(input("Enter Selection: "))

        if selection == 1:
            self.package_menu()
        elif selection == 2:
            self.clock_menu()

    def package_menu(self):
        selection = 0
        min_choice = 1
        max_choice = 2
        while selection not in range(min_choice, max_choice + 1):
            print()
            print("1.\tPrint package by ID")
            print("2.\tPrint all packages")
            print()

            selection = int(input("Enter Selection: "))

        if selection == 1:
            selection = None
            while not isinstance(selection, int):
                print()
                selection = int(input("Enter Package ID"))
            package = self._packages.search(selection)
            package.print(self._start_time)
        elif selection == 2:
            for package in self._packages:
                package.print(self._start_time)

    def clock_menu(self):
        selection = 0
        min_choice = 1
        max_choice = 3
        while selection not in range(min_choice, max_choice + 1):
            print()
            print("1.\tHours")
            print("2.\tMinutes")
            print("3.\tMinutes")
            print()

            selection = int(input("Enter selections"))

        if selection == 1:
            num_hours = int(input("How many hours? "))
            time = self._clock.forward_hours(num_hours)
            self.advance_simulation(time)
        elif selection == 2:
            num_minutes = int(input("How many minutes? "))
            time = self._clock.forward_minutes(num_minutes)
            self.advance_simulation(time)
        elif selection == 3:
            num_seconds = int(input("How many seconds? "))
            time = self._clock.forward_seconds(num_seconds)
            self.advance_simulation(time)

    def advance_simulation(self, time):
        while self._clock.time < time:
            self._clock.advance_time()
