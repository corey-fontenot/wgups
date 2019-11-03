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
        """
        return f"{self.address}, {self.city}, {self.state}, {self.zipcode}"

    def __eq__(self, other):
        return self.address == other.address and self.zipcode == other.zipcode
