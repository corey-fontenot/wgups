from .queue import Queue


class Vertex:
    """
    Element in a graph
    """
    def __init__(self, label, data=None):
        """
        Create a vertex
        :param label: vertex label
        """
        self.label = label
        self.data = data
        self.index = None

    def __str__(self):
        result = self.label
        if self.data is not None:
            result = f"{result}: {str(self.data)}"
        return result


class Graph:
    """
    Graph Data Structure
    """
    def __init__(self):
        self.adjacency_matrix = []
        self.vertex_list = []
        self.last_index = None

    def add_vertex(self, label, data=None):
        """
        Add a vertex to the graph
        :param label: label for new vertex
        :param data: data for new vertex
        :return: None

        Worst Case Runtime Complexity: O(N)
        Best Case Runtime Complexity: O(N)
        """
        new_vertex = Vertex(label, data)
        if self.last_index is None:
            self.last_index = 0
        else:
            self.last_index += 1
        new_vertex.index = self.last_index

        self.vertex_list.append(new_vertex)

        self.adjacency_matrix.append([])
        for entry in range(0, new_vertex.index + 1):
            self.adjacency_matrix[new_vertex.index].append(0)

        for entry in range(0, new_vertex.index):
            self.adjacency_matrix[entry].append(0)

    def add_undirected_edge(self, label_a, label_b, weight=1):
        """
        Adds an undirected edge to the graph
        Returns if either of the provided vertices is not in the graph
        :param label_a: label of the first vertex
        :param label_b: label of the second vertex
        :param weight: optional weight, default value is 1
        :return: None

        Worst Case Runtime Complexity: O(N)
        Best Case Runtime Complexity: O(1)
        """
        vertex_a = self.get_vertex(label_a)
        vertex_b = self.get_vertex(label_b)

        if vertex_a is None or vertex_b is None:
            return

        self.adjacency_matrix[vertex_a.index][vertex_b.index] = weight
        self.adjacency_matrix[vertex_b.index][vertex_a.index] = weight

    def add_directed_edge(self, source_label, destination_label, weight=1):
        """
        Add a directed edge to the graph
        Returns if either of the provided vertices is not in graph
        :param source_label: label of the source vertex
        :param destination_label: label of the destination vertex
        :param weight: optional edge weigh, default value is 1
        :return: None

        Worst Case Runtime Complexity: O(N)
        Best Case Runtime Complexity: O(1)
        """
        source_vertex = None
        destination_vertex = None

        source_vertex = self.get_vertex(source_label)
        destination_vertex = self.get_vertex(destination_label)

        if source_vertex is None or destination_vertex is None:
            return

        self.adjacency_matrix[source_vertex.index][destination_vertex.index] = weight

    def get_vertex(self, vertex_label):
        """
        Get vertex by label
        :param vertex_label: label of desired vertex
        :return: Found Vertex, None otherwise :Vertex, None

        Worst Case Runtime Complexity: O(N)
        Best Case Runtime Complexity: O(1)
        """
        for vertex in self.vertex_list:
            if vertex.label == vertex_label:
                return vertex
        return None

    def get_adjacent_vertices(self, vertex_label):
        """
        Get all vertices adjacent to provided vertex
        :param vertex_label: label of provided vertex
        :return: List containing all adjacent vertices,
                Empty List if no adjacent vertices or provided vertex not found :List

        Worst Case Runtime Complexity: O(N)
        Best Case Runtime Complexity: O(N)
        """
        start_vertex = self.get_vertex(vertex_label)
        result = []
        if start_vertex is None:
            return result
        for vertex in self.vertex_list:
            if vertex.label == vertex_label:
                start_vertex = vertex

        for num, entry in enumerate(self.adjacency_matrix[start_vertex.index]):
            if entry != 0:
                result.append(self.vertex_list[num])
        return result

    def print_adjacency_matrix(self):
        """
        Print the adjacency matrix
        :return: None

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """
        for row in self.adjacency_matrix:
            print(row)
