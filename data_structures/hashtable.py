class EmptyBucket:
    pass


class HashTable:
    """
    Hashtable using Linear Probing for collision resolution
    """
    def __init__(self, initial_capacity=10):
        """
        Creates a HashTable Object

        :param initial_capacity initial capacity of the hash table

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """

        # Special constants to represent two types of empty buckets
        self.EMPTY_SINCE_START = EmptyBucket()
        self.EMPTY_AFTER_REMOVAL = EmptyBucket()

        # Initialize table with EMPTY_SINCE_START buckets
        self.table = [self.EMPTY_SINCE_START] * initial_capacity

        self._num_items = 0

    @property
    def num_items(self):
        """
        Read-only property to get number of items in table
        :return: number of items in table
        """
        return self._num_items

    def hash(self, key):
        """
        Returns a hash of the provided key
        :param key: key to be hashed :str, int
        :return: hashed key :int

        Hashes a key using the multiplicative hash algorithm
        Key can be a string or any time that can be converted to a string using the str() method
        The value 223 was chosen for N using trial and error to minimize collisions

        Worst Case Runtime Complexity: O(N)
        Best Case Runtime Complexity: O(N)
        """
        string_hash = 5381
        for char in str(key):
            string_hash = (string_hash * 33) + ord(char)
        return string_hash % 223

    def insert(self, item):
        """
        Insert a new item into the hashtable if it does not already exist

        :param item to be inserted, item must have a key attribute for hashing
        :return True if item is inserted, False otherwise
        """
        if not hasattr(item, "key"):
            return False

        bucket = self.hash(item.key) % len(self.table)
        buckets_probed = 0
        while buckets_probed < len(self.table):
            if type(self.table[bucket]) is EmptyBucket:
                # Bucket is empty, insert item
                self.table[bucket] = item
                self._num_items += 1

                # If hashtable has a load factor greater than 0.75, resize table
                if self.num_items / len(self.table) > 0.75:
                    self._resize()

                return True

            # Bucket full continue probing with next bucket in the table
            bucket = (bucket + 1) % len(self.table)
            buckets_probed += 1

        # Table is full, cannot be inserted
        return False

    def remove(self, key):
        """
        Remove item from the hashtable if it exists
        :param key: key of item to be removed
        :return: True if item removed, otherwise False

        Worst Case Runtime Complexity: O(N)
        Best Case Runtime Complexity: O(1)
        """
        bucket = self.hash(key) % len(self.table)
        buckets_probed = 0
        while self.table[bucket] is not self.EMPTY_SINCE_START and buckets_probed < len(self.table):
            if type(self.table[bucket]) != EmptyBucket and self.table[bucket].key == key:
                self.table[bucket] = self.EMPTY_AFTER_REMOVAL
                self._num_items -= 1
                # Item found and removed
                return True

            # bucket was occupied, so keep probing
            bucket = (bucket + 1) % len(self.table)
            buckets_probed += 1
        # Item not found
        return False

    def search(self, key):
        """
        Finds item based on specified key
        :param key: key of item being searched
        :return: found item or None if not found :Object, None

        Worst Case Runtime Complexity: O(N)
        Best Case Runtime Complexity: O(1)
        """
        bucket = self.hash(key) % len(self.table)
        buckets_probed = 0
        while self.table[bucket] is not self.EMPTY_SINCE_START and buckets_probed < len(self.table):

            # Item was found
            if type(self.table[bucket]) != EmptyBucket and self.table[bucket].key == key:
                return self.table[bucket]

            # bucket was occupied, keep probing
            bucket = (bucket + 1) % len(self.table)
            buckets_probed += 1

        # Item not found
        return None

    def _resize(self):
        """
        Resize table to make more room for new items

        Worst Case Runtime Complexity: O(N)
        Best Case Runtime Complexity: O(N)
        :return: None
        """
        temp = self.table
        self.table = [self.EMPTY_SINCE_START] * (len(self.table) * 2)

        for item in temp:
            self.insert(item)

    def __iter__(self):
        return HashTableIterator(self)

    def __str__(self):
        """
        Returns a string representation of the HashTable
        Only works if object can be converted to a string (__str__ method is implemented)
        :return: String representation of the HashTable

        Worst Case Runtime Complexity: O(N)
        Best Case Runtime Complexity: O(N)
        """
        result = ""
        for item in self:
            result += str(item)
        return result


class HashTableIterator:
    """
    Iterator for HashTable Objects
    """
    def __init__(self, hashtable):
        """
        Create HashTableIterator Object
        :param hashtable: hashtable being iterated over
        """
        self._hashtable = hashtable

        # index of next item to be returned
        self._index = 0

    def __next__(self):
        """
        Returns next item in current iteration
        :return: next item :Object

        Worst Case Runtime Complexity: O(N)
        Best Case Runtime Complexity: O(1)
        """
        if self._index < len(self._hashtable.table):

            # While current item is an EmptyBucket, Go to next item
            while self._index < len(self._hashtable.table) and type(self._hashtable.table[self._index]) is EmptyBucket:
                self._index += 1

            # If current index is out of bounds, End iteration
            if self._index >= len(self._hashtable.table):
                raise StopIteration

            # Return result and and increment index
            result = self._hashtable.table[self._index]
            self._index += 1
            return result
        raise StopIteration


