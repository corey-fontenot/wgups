from data_structures.graph import Graph, Vertex
from data_structures.queue import Queue
from .clock import Clock


class Truck:
    """
    Truck class to hold packages and deliver to destination
    """
    def __init__(self, truck_id, package_limit, speed, start_of_day, hub_location):
        """
        Create Truck Object
        :param truck_id: id of the truck :int
        :param package_limit: maximum number of packages truck can hold :int
        :param speed: speed of truck in miles per hour :int
        :param start_of_day: time of start of day :str
        :param hub_location: location of hub :Location
        :return: Truck Object
        """
        self._id = truck_id
        self._package_limit = package_limit
        self._speed = (speed / 60) / 60  # truck speed in miles per second
        self._locations = Graph()
        self._packages = []
        self._start_of_day = start_of_day
        self._locations.add_vertex(hub_location.name, hub_location)
        self._route = Queue()
        self._departure_time = None  # departure time in seconds since start
        self._distance_traveled = 0.0
        self._current_location = None
        self._next_location = None
        self._route_done = False

    @property
    def truck_id(self):
        """
        Read-only truck id. Cannot be changed after Object creation
        :return: Truck ID :int
        """
        return self._id

    @property
    def distance_traveled(self):
        """
        Read-only distance traveled. Cannot be set outside of class
        :return: distance traveled :float
        """
        return self._distance_traveled

    @property
    def package_limit(self):
        """
        Read-only truck package limit. Cannot be changed after Object creation
        :return: package limit for truck :int
        """
        return self._package_limit

    @property
    def next_location(self):
        return self._next_location

    def get_next_location(self, time):
        if not self._route.is_empty():
            self._next_location = self._route.pop()
        else:
            self._route_done = True
            print(f"{Clock.to_time_string(time, self._start_of_day)}: "
                  f"Truck {self.truck_id} finished route ({self.distance_traveled:.2f} miles driven)")

    def start_route(self, time):
        self._next_location = self._route.pop()
        for package in self._packages:
            package.status = "EN ROUTE"
        self._departure_time = time
        self._next_location = self._route.pop()
        print(f"{Clock.to_time_string(time, self._start_of_day)}: Truck {self.truck_id} leaving Hub")

    def get_package_count(self):
        """
        Return the number of packages currently on the truck
        :return: number of packages on truck :int
        """
        return len(self._packages)

    def move_truck(self):
        if not self._route_done:
            self._distance_traveled += self._speed
            return self._speed
        return 0

    def is_route_done(self):
        return self._route_done

    def get_package_list(self):
        """
        Returns list of packages on truck
        :return: list of packages :List<Package>
        """
        return self._packages

    def is_on_truck(self, package_id):
        """
        Returns True if package with given id is on the truck
        :param package_id: package_id to search for
        :return: True if package on truck, otherwise False

        Worst Case Runtime Complexity: O(N)
        Best Case Runtime Complexity: O(1)
        """
        for package in self._packages:
            if package.package_id == package_id:
                return True
        return False

    def load_package(self, package):
        """
        Add package to truck
        :param package: package to be added :Package
        :return: Void
        """
        self._packages.append(package)

    def set_locations(self, locations_graph):
        """
        Populate _locations graph with package locations and set edges for the graph
        :param locations_graph: Graph with locations data for all locations
        :return: Void
        """
        for package in self._packages:
            if package.location not in map(lambda x: x.data, self._locations.get_vertex_list()):
                for vertex in locations_graph.get_vertex_list():
                    if vertex.data == package.location:
                        self._locations.add_vertex(vertex.data.name, vertex.data)
                        break

        for location in map(lambda x: x.data, self._locations.get_vertex_list()):
            # index in truck graph
            index = self._locations.get_vertex_list().index(self._locations.get_vertex(location.name))

            # index in graph of all locations
            all_locations_index = locations_graph.get_vertex_list().index(locations_graph.get_vertex(location.name))

            for num, loc in enumerate(map(lambda x: x.data, self._locations.get_vertex_list())):
                cur_index = locations_graph.get_vertex(loc.name).index
                self._locations.adjacency_matrix[index][num] = locations_graph.adjacency_matrix[all_locations_index][cur_index]

    def deliver_package(self, package):
        """
        Remove package from truck and return package ID
        :param package: package to be removed
        :return: package ID of package removed :int
        """
        return self._packages.pop(self._packages.index(package)).package_id

    def find_route(self):
        """
        Calculate delivery route
        :return: Void

        Worst Case Runtime Complexity: O(N^2)
        Best Case Runtime Complexity: O(N^2)
        """
        # Worst Case Runtime Complexity: O(N^2)
        # Best Case Runtime Complexity: O(N^2)
        route = self._locations.calculate_tour(self._locations.get_vertex_list()[0])
        start = route.peek()
        total_distance = 0.0
        last_location = start
        while not route.is_empty():
            current_location = route.pop()
            distance = self._locations.get_edge_weight(last_location, current_location)
            total_distance += distance
            self._route.push((current_location, total_distance))
            last_location = current_location

    @staticmethod
    def sort_packages(packages, trucks, start_of_day, end_of_day):
        # Load packages that must be on same truck onto truck 1 along with any packages with same address
        same_truck_packages = []
        for package in filter(lambda x: x.special_instructions.startswith("Must be delivered with"), packages):
            deliver_with = package.special_instructions[23:].split(", ")
            if package not in same_truck_packages:
                same_truck_packages.append(package)

            for cur_package in filter(lambda x: str(x.package_id) in deliver_with, packages):
                if cur_package not in same_truck_packages:
                    same_truck_packages.append(cur_package)

        same_locations = []
        for package in same_truck_packages:
            if package.location not in same_locations:
                same_locations.append(package.location)
            trucks[0].load_package(package)
            packages.remove(package)

        found_packages = []
        for package in packages:
            if package.location in same_locations and not package.has_special_instructions():
                found_packages.append(package)

        for package in found_packages:
            trucks[0].load_package(package)
            packages.remove(package)

        # Load remaining packages with special instructions
        for package in filter(lambda x: x.has_special_instructions(), packages):
            if package.special_instructions == "Wrong address listed":
                trucks[-1].load_package(package)
                packages.remove(package)

            elif package.special_instructions.startswith("Delayed on flight"):
                trucks[1].load_package(package)
                packages.remove(package)

            elif package.special_instructions.startswith("Can only be on truck") and package in packages:
                trucks[int(package.special_instructions[-1]) - 1].load_package(package)
                packages.remove(package)

        # Load packages with no deadline onto truck 3
        no_deadline = []
        for package in filter(lambda x: not x.deadline < Clock.seconds_since_start(end_of_day, start_of_day), packages):
            no_deadline.append(package)

        for package in no_deadline:
            trucks[-1].load_package(package)
            packages.remove(package)

        current_truck = 0
        while len(packages) > 0:
            while current_truck < 3 and trucks[current_truck].get_package_count() < 16 and len(packages) > 0:
                trucks[current_truck].load_package(packages[-1])
                packages.remove(packages[-1])
            current_truck += 1

        return trucks
