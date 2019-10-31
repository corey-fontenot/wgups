from .linked_list import Node, LinkedList


class Queue:
    """
    First-In, First-Out (FIFO) Data Structure
    """
    def __init__(self):
        self._queue = LinkedList()

    def is_empty(self):
        """
        Determines if the queue is empty or not
        :return: True if queue is empty, False otherwise
        """
        return self._queue.is_empty()

    def push(self, item):
        """
        Add an item to the end of the queue
        :param item: item to be added
        :return: None
        """
        self._queue.append(Node(item))

    def pop(self):
        """
        Remove an item from the beginning of queue and return it
        :return: Removed item
        """
        popped_item = self._queue.head
        self._queue.remove_after(0)

        return popped_item

    def peek(self):
        """
        Return item from beginning of the queue without removing it
        :return: Item at beginning of the queue
        """
        return self._queue.head
