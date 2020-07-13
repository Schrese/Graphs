"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        # pass  # TODO
        self.vertices[vertex_id] = set() # This set will hold the edges/connections to other vertices

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        # pass  # TODO
        if v1 in self.vertices and v2 in self.vertices: 
            self.vertices[v1].add(v2)
        else:
            raise IndexError("nonexistant vertex") # Could also use "Exception("nonexistant vertex")". Both are built-in

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        # pass  # TODO
        return self.vertices[vertex_id]

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        pass  # TODO
        # Create a queue to know what we are traversing next
        q = Queue()
        # Hold the visited vertices in a set
        visited = set()
        # Instantiate the queue with the starting_vertex
        q.enqueue(starting_vertex)
        # While there are still items in the queue
        while q.size() > 0:
            # dequeue the first item in the queue
            v = q.dequeue()
            # loop through the neighbors 
            if v not in visited:
                # Remove the vertex from the queue and add it to "visited"
                visited.add(v)

                print(v)

                # add each vertex's neighbor to the queue
                for next_vertex in self.get_neighbors(v):
                    q.enqueue(next_vertex)


    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        #pass  # TODO
        # Create a stack to know what we are traversing next
        s = Stack()
        # Hold the visited vertices in a set
        visited = set()
        # Instantiate the stack with the starting_vertex
        s.push(starting_vertex)
        # While there are still items in the stack
        while s.size() > 0:
            # pop the first item off of the stack
            v = s.pop()
            # if that item is not in visited, then:
            if v not in visited:
                # add the item to the visited set 
                visited.add(v)
                print(v)
                # Loop through neighbors
                for next_vertex in self.get_neighbors(v):
                    # push the neighbors onto the stack
                    s.push(next_vertex)

    def dft_recursive(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        pass  # TODO

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        pass  # TODO

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        pass  # TODO

    def dfs_recursive(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        pass  # TODO

if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)
    # graph.add_edge(4, 8) # Tests that adding an edge to non-existant vertex returns correct error

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)
    print(graph.get_neighbors(4)) # Tests that getNeighbors works

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    # graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    # print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    # print(graph.dfs(1, 6))
    # print(graph.dfs_recursive(1, 6))
