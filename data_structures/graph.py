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

    @property
    def size(self):
        """
        Returns size of graph
        :return: size of graph :int
        """
        return len(self.vertex_list)

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
        new_vertex.index = len(self.vertex_list)

        self.vertex_list.append(new_vertex)

        self.adjacency_matrix.append([])
        for entry in range(0, new_vertex.index + 1):
            self.adjacency_matrix[new_vertex.index].append(0)

        for entry in range(0, new_vertex.index):
            self.adjacency_matrix[entry].append(0)

    def add_undirected_edge(self, vertex_a, vertex_b, weight=1):
        """
        Adds an undirected edge to the graph
        Returns if either of the provided vertices is not in the graph
        :param vertex_a: first vertex
        :param vertex_b: second vertex
        :param weight: optional weight, default value is 1
        :return: None

        Worst Case Runtime Complexity: O(N)
        Best Case Runtime Complexity: O(1)
        """
        if vertex_a not in self.vertex_list or vertex_b not in self.vertex_list:
            return

        self.adjacency_matrix[vertex_a.index][vertex_b.index] = weight
        self.adjacency_matrix[vertex_b.index][vertex_a.index] = weight

    def add_directed_edge(self, source, destination, weight=1):
        """
        Add a directed edge to the graph
        Returns if either of the provided vertices is not in graph
        :param source: source vertex
        :param destination: destination vertex
        :param weight: optional edge weigh, default value is 1
        :return: None

        Worst Case Runtime Complexity: O(N)
        Best Case Runtime Complexity: O(1)
        """

        if source not in self.vertex_list or destination not in self.vertex_list:
            return

        self.adjacency_matrix[source.index][destination.index] = weight

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

    def get_vertex_list(self):
        """
        Returns list of vertices in the graph
        :return: list of vertices in the graph :List<Vertex>
        """
        return self.vertex_list

    def get_vertex_by_index(self, vertex_index):
        """
        Get vertex by ID
        :param vertex_index: index to look for :int
        :return: vertex with given id :Vertex

        Worst Case Runtime Complexity: O(N)
        Best Case Runtime Complexity: O(1)
        """
        for vertex in self.vertex_list:
            if vertex.index == vertex_index:
                return vertex
        return None

    def get_adjacent_vertices(self, start_vertex):
        """
        Get all vertices adjacent to provided vertex
        :param start_vertex: vertex to get adjacent vertices of
        :return: List containing all adjacent vertices,
                Empty List if no adjacent vertices or provided vertex not found :List

        Worst Case Runtime Complexity: O(N)
        Best Case Runtime Complexity: O(N)
        """
        result = []
        if start_vertex not in self.vertex_list:
            return result

        for num, entry in enumerate(self.adjacency_matrix[start_vertex.index]):
            if entry != 0:
                result.append(self.vertex_list[num])
        return result

    def contains(self, vertex_label):
        if self.get_vertex(vertex_label) is not None:
            return True
        else:
            return False

    def get_edge_weight(self, source, destination):
        """
        Get the edge weight from source vertex to destination vertex
        :param source: source vertex
        :param destination: destination vertex
        :return: edge weight :float
        """
        return self.adjacency_matrix[source.index][destination.index]

    def print_adjacency_matrix(self):
        """
        Print the adjacency matrix
        :return: None

        Worst Case Runtime Complexity: O(1)
        Best Case Runtime Complexity: O(1)
        """
        for row in self.adjacency_matrix:
            print(row)

