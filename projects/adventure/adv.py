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
# world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
# This is the path for test_cross map
# traversal_path = ["n", "n", "s", "s", "w", "w", "e", "e", "s", "s", "n", "n", "e", "e"]

traversal_path = []

room = player.current_room
# This will need to be updated to be the last direction that the player moved in
direction_facing = "n"
# This will get updated when "direction_facing" gets updated. It's the next path that the player will look for
left_path = "w"
forward_path = "n"
right_path = "e"
back_path = "s"

# updates direction facing and calls update_dir_paths function to run at the same time
def update_dir_facing(dir, direction_facing):
    direction_facing = dir
    update_dir_paths(dir)

# Takes a direction and directional paths above as arguments and updates the paths with correct directions
def update_dir_paths(dir):
    print(dir)
    if dir == "w":
        left_path = "s"
        forward_path = "w"
        right_path = "n"
        back_path = "e"
        print('west', left_path, forward_path, right_path, back_path)

    elif dir == "n":
        left_path = "w"
        forward_path = "n"
        right_path = "e"
        back_path = "s"        
        print('north', left_path, forward_path, right_path, back_path)
    
    elif dir == "e":
        left_path = "n"
        forward_path = "e"
        right_path = "s"
        back_path = "w"
        print('east', left_path, forward_path, right_path, back_path)
    
    else:
        left_path = "e"
        forward_path = "s"
        right_path = "w"
        back_path = "n"
        print("south", left_path, forward_path, right_path, back_path)


# update_dir_facing("e", direction_facing)

def exploration(current, direction_facing):
    print(len(room_graph))

    while len(traversal_path) < len(room_graph):
        # print(left_path, forward_path, right_path, back_path)

        # if left_path in room.get_exits():
        #     print('option 1')
        #     player.travel(left_path, True)
        #     traversal_path.append(left_path)
        #     update_dir_facing(left_path, direction_facing)
        #     # direction_facing = left_path
        #     # print(direction_facing)
        #     # exploration(player.current_room)

        # else:
        #     if forward_path in room.get_exits():
        #         print('option 1')
        #         player.travel(forward_path, True)
        #         traversal_path.append(forward_path)
        #         direction_facing = forward_path

        #     else:
        #         if right_path in room.get_exits():
        #             print('option 3')
        #             player.travel(right_path, True)
        #             traversal_path.append(right_path)
        #             direction_facing = right_path
        #         else:
        #             print('option 4')
        #             player.travel(back_path, True)
        #             traversal_path.append(back_path)
        #             direction_facing = right_path

exploration(room, direction_facing)
print(player.current_room, room.id, traversal_path, direction_facing, ';aoisjd;ofije;oaij;sodifjo;eijaof')
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
