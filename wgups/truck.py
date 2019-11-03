from data_structures.graph import Graph
from .location import Location
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
        self._speed = speed
        self._locations = Graph()
        self._packages = []
        self._start_of_day = Clock.parse_time_string(start_of_day)
        self._locations.add_vertex(hub_location.name, hub_location)

    @property
    def truck_id(self):
        """
        Read-only truck id. Cannot be changed after Object creation
        :return: Truck ID :int
        """
        return self._id

    @property
    def package_limit(self):
        """
        Read-only truck package limit. Cannot be changed after Object creation
        :return: package limit for truck :int
        """
        return self._package_limit

    def get_package_count(self):
        """
        Return the number of packages currently on the truck
        :return: number of packages on truck :int
        """
        return len(self._packages)

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
            found_vertices = [x for x in locations_graph.get_vertex_list()
                              if x.data == package.location]
            if len(found_vertices) > 0:
                if found_vertices[0].data not in map(lambda x: x.data, self._locations.get_vertex_list()):
                    self._locations.add_vertex(found_vertices[0].data.name, found_vertices[0].data)

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

    @staticmethod
    def sort_into_trucks(packages, trucks, start_of_day, end_of_day):
        """
        Sort package into correct truck
        :param packages: list of unsorted packages :List<Packages>
        :param trucks: list of unloaded trucks :List<Trucks>
        :param start_of_day: time of start of day
        :param end_of_day: time of end of day
        :return: list of trucks with packages loaded :List<Trucks>
        """

        # Load all packages that must be on same truck onto first truck
        # Worst Case Runtime Complexity: O(N^2)
        # Best Case Runtime Complexity: O(N^2)
        same_truck_packages = []
        for package in filter(lambda x: x.special_instructions.startswith("Must be delivered with"), packages):
            # length of "Must be delivered with " is 23
            deliver_with = package.special_instructions[23:].split(", ")
            if package not in same_truck_packages:
                same_truck_packages.append(package)

            for cur_package in filter(lambda x: str(x.package_id) in deliver_with, packages):
                if cur_package not in same_truck_packages:
                    same_truck_packages.append(cur_package)

        for package in same_truck_packages:
            trucks[0].load_package(package)
            packages.remove(package)

        # Load remaining packages that have special instructions
        # Worst Case Runtime Complexity: O(N)
        # Best Case Runtime Complexity: O(N)
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

        for package in filter(lambda x: x.deadline < Clock.seconds_since_start(end_of_day, start_of_day), packages):
            trucks[0].load_package(package)
            packages.remove(package)

        # find highest concentration of a particular zipcode for each truck
        # add packages with same zipcode
        # then add packages from remaining packages until truck is full or all packages are loaded
        # Worst Case Runtime Complexity: O(N)
        # Best Case Runtime Complexity: O(N)
        for truck in trucks:
            zipcodes = []
            zipcode_count = []

            while len(packages) > 0 and truck.get_package_count() < truck.package_limit:
                for package in truck.get_package_list():
                    if package.location.zipcode in zipcodes:
                        index = zipcodes.index(package.location.zipcode)
                        zipcode_count[index] += 1
                    else:
                        zipcodes.append(package.location.zipcode)
                        zipcode_count.append(1)
                highest_volume_zip = zipcodes[zipcode_count.index(max(zipcode_count))]
                for package in filter(lambda x: x.location.zipcode == highest_volume_zip, packages):
                    truck.load_package(package)
                    packages.remove(package)

                for package in packages:
                    if truck.get_package_count() == truck.package_limit:
                        break
                    if package in packages:
                        truck.load_package(package)
                        packages.remove(package)

                zipcodes = []
                zipcode_count = []

        return trucks
