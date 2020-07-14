from util import Queue
from graph import Graph

def earliest_ancestor(ancestors, starting_node):
    g = Graph()

    for family in ancestors:
        g.add_vertex(family[0])
        g.add_vertex(family[1])

    for family in ancestors:
        g.add_edge(family[1], family[0]) # Had to do opposite of pair order so that each entry now points to its parents

    # print(g.vertices, g.vertices[2], g.get_neighbors(6))
    visited = set()
    # Create a queue and put the starting_node at the top
    q = Queue()    
    q.enqueue([starting_node])

    if len(g.get_neighbors(starting_node)) < 1:
        return -1

    while q.size() > 0:
        path = q.dequeue()
        # print(path)
        v = path[-1]
        print(path)

        if v not in visited:
            visited.add(v)



        # for i, child in ancestors:
        #     print(child, i)
        for parent in g.get_neighbors(v):
            path_copy = list(path)
            path_copy.append(parent)
            q.enqueue(path_copy)
            


# def get_parents(child_id):
#     return 
