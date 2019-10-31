# Corey Fontenot #001027553

import csv
from configparser import ConfigParser
from wgups.clock import Clock
from wgups.location import Location
from wgups.package import Package
from data_structures.hashtable import HashTable

packages = HashTable(120)
# Read package data from csv file and load into program
parser = ConfigParser()
parser.read("config.ini")

# Read package data from file
with open(parser.get("files", "package_file"), 'r') as f:
    reader = csv.reader(f)
    for row in reader:

        # Create Location Object
        location = Location(row[1], row[2], row[3], row[4])

        # If deadline is EOD convert to time for end of day
        deadline = row[5]
        if deadline == "EOD":
            deadline = parser.get("application", "end_of_day")

        # Create package object and insert into hashtable
        package = Package(int(row[0]), location, Clock.seconds_since_start(deadline), float(row[6]), row[7])
        packages.insert(package)

