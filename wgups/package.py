from .clock import Clock


class Package:
    """
    Package object represent a package in the WGUPS system
    """

    def __init__(self, package_id, location, deadline, weight, special_instructions, status, start_time):
        """
        Create a Package object
        :param package_id: id of package :int
        :param location: location of the package :Location
        :param deadline: delivery deadline in seconds since start :int
        :param weight: weight of package :float
        :param special_instructions: special instructions, if none, empty string :string
        :param status: status of package :string
        :param start_time: start_time (for converting deadline to correct time string :str

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """
        self._package_id = package_id
        self._location = location
        self._deadline = deadline
        self._weight = weight
        self._special_instructions = special_instructions
        self._status = status
        self._start_time = start_time

    # read-only package id
    @property
    def package_id(self):
        """
        Returns id of package
        :return: package id :int

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """
        return self._package_id

    @property
    def location(self):
        """
        Returns location of object
        :return: location of package :Location

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """
        return self._location

    @location.setter
    def location(self, location):
        """
        Set package location
        :param location: location of the package :Location
        :return: none

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """
        self._location = location

    @property
    def deadline(self):
        """
        Retrieves package deadline in number of seconds since start time
        :return: package deadline :int

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """
        return self._deadline

    @deadline.setter
    def deadline(self, time):
        """
        Set deadline for package

        :param time: number of seconds since start time :int
        :return: none

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """
        self._deadline = time

    @property
    def weight(self):
        """
        Return weight of package
        :return: weight of package :float

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """
        return self._weight

    @weight.setter
    def weight(self, weight):
        """
        Set weight of package
        :param weight: weight of package :float
        :return: none

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """
        self._weight = weight

    @property
    def special_instructions(self):
        """
        Return special_instructions for package, if empty string returned there are no special instructions
        :return: special instructions for package :str

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """
        return self._special_instructions

    @special_instructions.setter
    def special_instructions(self, instructions):
        """
        Set special instructions for package, if no special instructions set as empty string
        :param instructions: special instructions for package :str
        :return: none

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """
        self._special_instructions = instructions

    @property
    def status(self):
        """
        Returns status of package
        :return: status of package :str

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Set status of package
        :param status: status of package :str
        :return: none

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """
        self._status = status

    def has_special_instructions(self):
        """
        Checks if package has special instructions (_special_instructions is not an empty string)
        :return: True if has special instructions, otherwise False :boolean

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Caomplexity: O(1)
        """
        # evaluate to false if _special_instructions is an empty string
        if not self._special_instructions:
            return False

        # return True if _special_instructions has a non-empty value
        return True

    def __str__(self):
        clock = Clock(self._start_time, self._deadline)

        special_instructions = self._special_instructions
        if not special_instructions:
            special_instructions = "None"
        result = f"""
        Package ID: {self._package_id}
        Location: {str(self._location)}
        Deadline: {clock.to_time_string()}
        Weight: {self._weight}
        Special Instructions: {special_instructions}
        Status: {self._status}
        """
        return result
