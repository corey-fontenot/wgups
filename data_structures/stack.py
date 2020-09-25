from .linked_list import Node, LinkedList


class Stack:
    """
    Stack Data Structure

    space complexity: O(N)
    """
    def __init__(self):
        """
        Creates a new stack
        :return: new stack object :Stack

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """
        self._stack = LinkedList()

    def push(self, item):
        """
        Adds a new item to the stack
        :param item: item to be added
        :return: Void

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """
        new_node = Node(item)
        self._stack.prepend(new_node)

    def pop(self):
        """
        Remove item from top of stack
        :return: removed item :<Item>

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """
        popped_item = self._stack.head.data
        self._stack.remove_after(0)

        return popped_item

    def peek(self):
        """
        Returns item at top of stack without removing it
        :return: item at top of stack :<Item>

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """
        return self._stack.head.data

    def is_empty(self):
        """
        Returns True if stack is empty, False otherwise
        :return: True if stack is empty, False otherwise :boolean

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """
        return self._stack.is_empty()
