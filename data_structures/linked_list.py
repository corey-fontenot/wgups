class Node:
    """
    Node Class to be used as an element in a Linked List
    """

    def __init__(self, data=None):
        """
        Creates a Node object
        :param data: data to be stored in Node

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """
        self.data = data
        self.next = None


class LinkedList:
    """
    Singly-Linked List
        holds nodes which each point to the next node in the list
    """

    def __init__(self):
        """
        Creates a LinkedList object
        :return LinkedList Object

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """
        self.head = None  # represents first node in the list
        self.tail = None  # represents the last node in the list
        self._length = 0

    @property
    def length(self):
        """
        Read only length property
        :return: length of list :int

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """
        return self._length

    def is_empty(self):
        """
        Check if Linked List is empty
        :return: True if list is empty, otherwise False

        Worst Case Time Complexity: O(1)
        Best Case Time Complexity: O(1)
        """
        if self.head is None:
            return True
        return False

    def append(self, new_node):
        """
        Adds a node to the end of the list
        :param new_node: node to be added to the list :Node

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """

        # If head is None, add node as only element in list
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self._length += 1

        # Otherwise add node after tail node
        else:
            self.tail.next = new_node
            self.tail = new_node
            self._length += 1

    def prepend(self, new_node):
        """
        Adds a node to the beginning of the list
        :param new_node: node to be added to the list :Node

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """

        # if head is None, add node as only element in the list
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self._length += 1

        # Otherwise, add node after tail node
        else:
            new_node.next = self.head
            self.head = new_node
            self._length += 1

    def search(self, key):
        """
        Search for an element in the list
        :param key: item for which to search
        :return: node found, or None if item not found :Node, None

        Worst Case Runtime Complexity: O(N)
        Best Case Runtime Complexity: O(1)
        """

        # Iterate over list until item is found or end of list is reached
        cur_node = self.head
        while cur_node is not None:
            if cur_node.data.key == key:
                return cur_node.data  # Item found
            cur_node = cur_node.next
        return None  # Item not found

    def insert_after(self, cur_node, new_node):
        """
        Insert node after a specified node in the list
        :param cur_node: node that current node will be inserted after :Node
        :param new_node: node to be inserted :Node

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """

        # If list empty, add node as only element in the list
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self._length += 1

        # If cur_node is the tail, insert new_node as list tail
        elif cur_node == self.tail:
            self.tail.next = new_node
            self.tail = new_node
            self._length += 1
        else:

            # Otherwise, insert node after specified node, and point new_node.next to cur_node.next
            new_node.next = cur_node.next
            cur_node.next = new_node
            self._length += 1

    def remove_after(self, cur_node):
        """
        Remove node after specified node
        :param cur_node: node before node to be removed
        :return: Whether removal was successful or not :boolean

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """

        # Remove the head node
        if cur_node == 0 and self.head is not None:
            suc_node = self.head.next
            self.head = suc_node

            # Removed only element in the list
            if suc_node is None:
                self.tail = None

            self._length -= 1

            # Successfully removed node
            return True

        # If cur_node is not the tail, remove next node
        elif cur_node.next is not None:
            suc_node = cur_node.next.next
            cur_node.next = suc_node

            # if removed node was the tail, set cur_node as the tail node
            if suc_node is None:
                self.tail = cur_node

            self._length -= 1

            # Successfully removed node
            return True

        # node was not removed
        return False

    def remove(self, item):
        """
        Remove specified item from linked list
        :param item: item to be removed
        :return: True if item removed, otherwise False

        Worst Case Runtime Complexity: O(N)
        Best Case Runtime Complexity: O(1)
        """
        pred_node = None
        cur_node = self.head
        while cur_node is not None:
            if cur_node.data == item:
                if pred_node is None:
                    return self.remove_after(0)
                else:
                    return self.remove_after(pred_node)
            pred_node = cur_node
            cur_node = cur_node.next
        return False  # unable to remove node

    def __iter__(self):
        """
        Return Iterator Object for Linked List
        :return: iterator object :LinkedListIterator
        """
        return LinkedListIterator(self)

    def __str__(self):
        result = ''
        for item in self:
            result += str(item)
        return result


class LinkedListIterator:
    """
    Iterator for Linked List Class
    """
    def __init__(self, linked_list):
        self._linked_list = linked_list
        self._index = 0

    def __next__(self):
        """
        Returns next object from Linked List
        :return: Linked List node
        """
        if self._index < self._linked_list.length:
            cur_node = self._linked_list.head
            result = cur_node.data
            cur_index = 0
            while cur_index <= self._index:
                result = cur_node.data
                cur_node = cur_node.next
                cur_index += 1
            self._index += 1
            return result
        raise StopIteration


