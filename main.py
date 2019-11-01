# Corey Fontenot #001027553

import csv
from configparser import ConfigParser
from wgups.clock import Clock
from wgups.location import Location
from wgups.package import Package
from data_structures.hashtable import HashTable
from data_structures.graph import Vertex, Graph

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
NUM_TRUCKS = parser.get("trucks", "num_trucks")
NUM_DRIVERS = parser.get("trucks", "num_drivers")
PACKAGES_PER_TRUCK = parser.get("trucks", "packages_per_truck")
TRUCK_MPH = parser.get("trucks", "truck_mph")

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
            locations.add_undirected_edge(location.name, temp_locations[index].name, float(distance))
