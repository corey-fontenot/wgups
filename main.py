# Corey Fontenot #001027553

import csv
from configparser import ConfigParser

from data_structures.graph import Graph
from data_structures.hashtable import HashTable
from data_structures.queue import Queue
from wgups.clock import Clock
from wgups.location import Location
from wgups.package import Package
from wgups.truck import Truck
from wgups.simulation import Simulation


packages = HashTable(120)
locations = Graph()

# Get configuration data
parser = ConfigParser()
parser.read("config.ini")

# Application Constants
START_OF_DAY = parser.get("application", "start_of_day")
END_OF_DAY = parser.get("application", "end_of_day")
PACKAGE_FILE = parser.get("files", "package_file")
DISTANCE_TABLE = parser.get("files", "distance_table")
NUM_TRUCKS = int(parser.get("trucks", "num_trucks"))
NUM_DRIVERS = int(parser.get("trucks", "num_drivers"))
PACKAGES_PER_TRUCK = int(parser.get("trucks", "packages_per_truck"))
TRUCK_MPH = int(parser.get("trucks", "truck_mph"))
DELAYED_FLIGHT_TIME = parser.get("application", "delayed_flight_time")

# Read package data from file
with open(PACKAGE_FILE, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        # Create Location Object
        location = Location(row[1], row[2], row[3], row[4])

        # If deadline is EOD convert to time for end of day
        deadline = row[5]
        if deadline == "EOD":
            deadline = END_OF_DAY

        # Create package object and insert into hashtable
        package = Package(int(row[0]), location, Clock.seconds_since_start(deadline, START_OF_DAY), float(row[6]), row[7])
        packages.insert(package)

# Read distance table from file
with open(DISTANCE_TABLE, 'r') as f:
    reader = csv.reader(f)
    temp_locations = []
    for row in reader:
        # Create a Location object
        location = Location(row[1], row[2], row[3], row[4], row[0])
        # Add location to temp_locations and to locations graph
        temp_locations.append(location)
        locations.add_vertex(location.name, location)

        # Add undirected edge to graph with each distance value
        for index, distance in enumerate(row[5:]):
            vertex_a = locations.get_vertex(location.name)
            vertex_b = locations.get_vertex(temp_locations[index].name)
            locations.add_undirected_edge(vertex_a, vertex_b, float(distance))

# Create trucks
# Added in the order they will leave
truck_list = []
for truck_id in range(1, NUM_TRUCKS + 1):
    truck_list.append(Truck(truck_id, PACKAGES_PER_TRUCK, TRUCK_MPH, START_OF_DAY, locations.get_vertex_by_index(0).data))

# Queue trucks to leave hub
truck_queue = Queue()
for truck in Truck.sort_into_trucks([x for x in packages], truck_list, START_OF_DAY, END_OF_DAY):
    # Add location data for packages in truck
    truck.set_locations(locations)
    truck.find_route()

    # Add truck to truck queue
    truck_queue.push(truck)

# Start simulation
simulation = Simulation(START_OF_DAY, packages, truck_queue, DELAYED_FLIGHT_TIME)
simulation.start_simulation()
