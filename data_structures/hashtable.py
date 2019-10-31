from data_structures.linked_list import Node, LinkedList


class HashTable:
    """
    Hashtable using Chaining for collision resolution
    """
    def __init__(self, initial_capacity=10):
        """
        Creates a HashTable Object

        :param initial_capacity initial capacity of the hash table

        Worst Case Runtime Complexity: O(N)
        Best Case Runtime Complexity: O(N)
        """
        self._table = []
        self._length = 0
        for i in range(initial_capacity):
            self._table.append(LinkedList())

    def hash(self, key):
        return int(key) % 40

    def get_num_buckets(self):
        """
        Returns number of buckets in the hash table
        :return: number of buckets :int
        """
        return len(self._table)

    @property
    def length(self):
        """
        Read-only property to return number of items in table
        :return: number of items in table :int
        """
        return self._length

    def get_bucket(self, bucket):
        return self._table[bucket % self.get_num_buckets()]

    def insert(self, item):
        """
        Insert a new item into the hashtable if it does not already exist

        Worst Case Time Complexity: O(N)
        Best Case Time Complexity: O(1)
        :param item: Item to be inserted
        :return: True if item was inserted, otherwise False
        """
        # If item is not already in the hashtable, insert it
        if self.search(item.key) is None:
            bucket = self._table[self.hash(item.key) % len(self._table)]
            node = Node()
            node.next = None
            node.data = item
            bucket.append(node)
            self._length += 1
            return True  # Successfully inserted
        return False  # Not inserted

    def remove(self, item):
        """
        Remove item from the hashtable if it exists
        :param item: key of item to be removed
        :return: True if item removed, otherwise False
        """
        bucket = self._table[self.hash(item.key) % len(self._table)]
        removed = bucket.remove(item)
        if removed:
            self._length -= 1
        return removed

    def search(self, key):
        bucket = self._table[self.hash(key) % len(self._table)]
        return bucket.search(key)
