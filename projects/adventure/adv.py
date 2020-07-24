from room import Room
from player import Player
from world import World

from ast import literal_eval
import random
from collections import deque

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
# This is the path for test_cross map
# traversal_path = ["n", "n", "s", "s", "w", "w", "e", "e", "s", "s", "n", "n", "e", "e"]


# path the test will take
traversal_path = []

# room = player.current_room

# dictionary of each visited room. Each entry has values for n,s,e,w
# visited = {0: {'w': '?', 'n': '?', 'e': '?', 's': '?'}}
visited = {}
un_visited_directions = []
past_rooms = []

# Gets exits for the room and creates a dict entry in "visited" for it
def get_neighboring_rooms(r, unvisited):
    # print(f"FROM NEIGBOR METHOD ---> \n Traveled Directions: {unvisited}, \n Current Room: {r.id}, \n Past Rooms: {past_rooms}, \n Visited: {visited}, \n ---------------------------------")

    exits = r.get_exits()

    visited[r.id] = {}

    past_rooms.append(r.id)

    for e in exits:
        visited[r.id].update({e: "?"})
        if visited[r.id].get(e) == "?":
            unvisited.append(e)

    if "n" not in exits:
        visited[r.id].update({"n": None})
    if "s" not in exits:
        visited[r.id].update({"s": None})
    if "e" not in exits:
        visited[r.id].update({"e": None})
    if "w" not in exits:
        visited[r.id].update({"w": None})
    # else: 
    opposites = {"n": "s", 
                "e": "w", 
                "s": "n", 
                "w": "e"
                }
    if len(past_rooms) > 1:
    #     visited[r.id].update({unvisited[-1]: past_rooms[-1]})
        visited[r.id].update({"w": past_rooms[-2]})


    return exits


# get_neighboring_rooms(player.current_room)
# player.travel("s")
# get_neighboring_rooms(player.current_room)
# player.travel("s")
# get_neighboring_rooms(player.current_room)

def dfs(room, unvisited):
    # print(f"FROM DFT ------> \n Traveled Directions: {un_visited_directions}, \n Current Room: {room.id}, \n Past Rooms: {past_rooms}, \n Visited: {visited}, \n ---------------------------------")
    possible_directions = get_neighboring_rooms(room, un_visited_directions)
    random.shuffle(possible_directions)
    new_direction = un_visited_directions.pop()
    player.travel(new_direction)
    traversal_path.append(new_direction)
    if len(past_rooms) > 0:
        visited[past_rooms[-1]].update({new_direction: player.current_room.id})
        # print(player.current_room.id, past_rooms)
    # dft()
    if len(room.get_exits()) == 1:
        get_neighboring_rooms(room, un_visited_directions)
        go_back(room, unvisited)


def go_back(room, unvisited):
    # pass
    # While the current room doesn't have a "?", continue travelling in the popped off value of the "un_visited_directions" list
    # player.travel(un_visited_directions.pop())
    cont = True
    for d in player.current_room.get_exits():
        if visited[room.id].get(d) == "?":
            cont = False
            print(room.id, ';aosidjf;oiejao;sijdfo;jieo;fa')
            return dfs(player.current_room, unvisited)           
        else:
            next_backtracking_room = unvisited.pop()
            player.travel(next_backtracking_room)
            go_back(player.current_room, unvisited)
r = 0

while r < 5:
    dfs(player.current_room, un_visited_directions)   
    r += 1 
    print(player.current_room.id, 'in while loop')

print(visited)
player.current_room.print_room_description(player)








# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
