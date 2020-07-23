from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

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

"""
Went through the entirity of the main_maze and traversed it with just drawings. I think I understand what I need to change, now. 

The only time I'll be choosing a random direction is when the player is at room 0. This way I can still obey the "turn left if possible" rule, but still have a chance of not needing to traverse all the way back on one of the 2 longer paths just to traverse a path of 1 or 2 more rooms

SO... I need to start keeping track of my paths back to the "last unknown"
I went through a few of the map-files and drew out the paths I want the player to take. 

I still want the player to always take the "left" path (this will mean that everything gets visited, and will make it easier to keep track of my paths)

The player continues to take the "next" path until they reach a dead-end (meaning, they ignore any off-shoot rooms until after the dead-end is reached). 

Once the dead-end is reached, the player traverses back along a path of my creation (not the "traversal_path"). 

If the player reaches a room that has "?" in more than 1 direction, they continue along the normal path, BUT a new list is made to get back to that point. As soon as there are no more "?"'s in a room, the "mark" is removed and the player goes to the next "unknown"/"?" path. It would basically look like this (for the fork part of the loop... not exact because I'm tired and don't remember what this actually looks like): 
[e[e, n, e, n, n ]] ---> at the "n" is a dead-end (room 122). The second array is a marker that there are 2 unknowns in the room
                         So go back up to the last unknown room (which is 3, but the directions in the list give instructions back to it)
[e[]] --- > because there is still an unknown at 3.
[e[s, e, e, [s]]] ---> leads to dead-end of room 076
[e[s, e, e, e, n, n, [n, n, [n, [n, n, [n, [n, n, n, [w, [w, n, [n, w]]]]]]]]] ------> This reaches its dead end at room 495
[e[s, e, e, e, n, n, [n, n, [n, [n, n, [n, [n, n, n, [w, [w, n, [n, [n, e]]]]]]]]]] ------> This reaches its dead end at room 485
[e[s, e, e, e, n, n, [n, n, [n, [n, n, [n, [n, n, n, [w, [w, n, [n,]]]]]]]]] ------> no longer an unknown at "n" (room 472)
[e[s, e, e, e, n, n, [n, n, [n, [n, n, [n, [n, n, n, [w, [w]]]]]]]] -----> Still an unknown at "w" (room 336)
[e[s, e, e, e, n, n, [n, n, [n, [n, n, [n, [n, n, n, [w, [w, n]]]]]]]] --------> Dead-end at "n" (room 346)

... and so on and so-forth. Eventually I'll get back to room 0, and choose a random direction again

I think I just need to add in the "backtracking" path to make this all work correctly


"""

# path the test will take
traversal_path = []

room = player.current_room

# dictionary of each visited room. Each entry has values for n,s,e,w
# visited = {0: {'w': '?', 'n': '?', 'e': '?', 's': '?'}}
visited = {}








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
