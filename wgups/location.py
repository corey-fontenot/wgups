class Location:
    """
    Represents a package location (address)
    """
    def __init__(self, address, city, state, zipcode, name=""):
        """
        Creates a Location object
        :param address: location address
        :param city: location city
        :param state: location state
        :param zipcode: location zipcode

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.name = name

    def __str__(self):
        """
        Returns a string representation of the object
        :return: string representation of the object

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """
        return f"{self.address}, {self.city}, {self.state}, {self.zipcode}"

    def __eq__(self, other):
        """
        :param other: location object to be compared with
        :return: boolean representing whether the objects are equal or not :Boolean

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """
        return self.address == other.address and self.zipcode == other.zipcode
