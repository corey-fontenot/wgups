# Corey Fontenot #001027553

import csv
from wgups.clock import Clock
from wgups.location import Location
from wgups.package import Package
from configparser import ConfigParser

# Read package data from csv file and load into program
parser = ConfigParser()
parser.read("config.ini")
with open(parser.get("files", "package_file"), 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        location = Location(row[1], row[2], row[3], row[4])
        deadline = row[5]
        if deadline == "EOD":
            deadline = parser.get("application", "end_of_day")
        package = Package(row[0], location, Clock.seconds_since_start(deadline), row[6], row[7])
        # do something with package object
