from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
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

traversal_path = []

room = player.current_room
# This will need to be updated to be the last direction that the player moved in
direction_facing = "s"
# This will get updated when "direction_facing" gets updated. It's the next path that the player will look for
left_path = "w"
forward_path = "n"
right_path = "e"
back_path = "s"

if direction_facing == "n":
    left_path = "w"
    forward_path = "n"
    right_path = "e"
    back_path = "s"

if direction_facing == "e":
    left_path = "n"
    forward_path = "e"
    right_path = "s"
    back_path = "w"

if direction_facing == "s":
    left_path = "e"
    forward_path = "s"
    right_path = "w"
    back_path = "n"

if direction_facing == "w":
    left_path = "s"
    forward_path = "w"
    right_path = "n"
    back_path = "e"

def exploration(current):
    print(len(room_graph))

    while len(traversal_path) < len(room_graph):
        if left_path in room.get_exits():
            print('option 1')
            player.travel(left_path, True)
            traversal_path.append(left_path)
            direction_facing = left_path
            # print(direction_facing)
            exploration(player.current_room)

        elif left_path not in room.get_exits():
            print('option 1')
            player.travel(forward_path, True)
            traversal_path.append(forward_path)
            direction_facing = forward_path
            exploration(player.current_room)

        elif left_path and forward_path not in room.get_exits():
            print('option 3')
            player.travel(right_path, True)
            traversal_path.append(right_path)
            direction_facing = right_path
            exploration(player.current_room)

        elif left_path and forward_path and right_path not in room.get_exits():
            print('option 4')
            player.travel(back_path, True)
            traversal_path.append(back_path)
            direction_facing = right_path
            exploration(player.current_room)
        
        else:
            print('idk what to do here')
    print(player)

exploration(room)
print(player.current_room, room.id, traversal_path, ';aoisjd;ofije;oaij;sodifjo;eijaof')
# print(room, 'were in the room mr hat')

# # TRAVERSAL TEST
# visited_rooms = set()
# player.current_room = world.starting_room
# visited_rooms.add(player.current_room)

# for move in traversal_path:
#     player.travel(move)
#     visited_rooms.add(player.current_room)

# if len(visited_rooms) == len(room_graph):
#     print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
# else:
#     print("TESTS FAILED: INCOMPLETE TRAVERSAL")
#     print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



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
