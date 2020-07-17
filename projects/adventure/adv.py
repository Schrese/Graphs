from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
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
    # print(dir)
    if dir == "w":
        left_path = "s"
        forward_path = "w"
        right_path = "n"
        back_path = "e"
        # print('west', left_path, forward_path, right_path, back_path)

    elif dir == "n":
        left_path = "w"
        forward_path = "n"
        right_path = "e"
        back_path = "s"        
        # print('north', left_path, forward_path, right_path, back_path)
    
    elif dir == "e":
        left_path = "n"
        forward_path = "e"
        right_path = "s"
        back_path = "w"
        # print('east', left_path, forward_path, right_path, back_path)
    
    else:
        left_path = "e"
        forward_path = "s"
        right_path = "w"
        back_path = "n"
        # print("south", left_path, forward_path, right_path, back_path)

visited = {}
incomplete_rooms = []
completed_rooms = []
# incomplete_rooms.append(player.current_room.id)
# previous_room_id = 0
cardinal_directions = ["n", "s", "e", "w"]
def go_forward(direct):
    player.travel(direct, True)

try_this = False


def explore_room(r):
    previous_room_id = r.id
    if r not in visited:
        visited[r.id] = {"w": "?", "n": "?", "e": "?", "s": "?"}
        # print(r.get_exits()) 
        if "w" not in r.get_exits():
            visited[r.id].update({"w": None})
        if "n" not in r.get_exits():
            visited[r.id].update({"n": None})
        if "e" not in r.get_exits():
            visited[r.id].update({"e": None})
        if "s" not in r.get_exits():
            visited[r.id].update({"s": None})
        incomplete_rooms.append(r.id)
        # print(exits, 'exits')


    # print(visited[r.id].values(), r.id, 'maybe this will give me a better idea')
    # if "?" not in visited[r.id].values():
    #     print('completed')
    #     incomplete_rooms.remove(r.id)
    #     try_this = True
    # else:
    #     print('more to get done')
    #     incomplete_rooms.append(r.id)

    # print(previous_room_id, 'prevvvvvvvvvvvvvvv')
    return previous_room_id



# while len(traversal_path) < len(room_graph):
# r = 0
while len(incomplete_rooms) < len(room_graph) :
    # r += 1
    previ = explore_room(player.current_room) 
    # print(previ, 'please be here')  
    # print(direction_facing, 'there must be something wrong here')
    if (left_path not in player.current_room.get_exits()) and (forward_path not in player.current_room.get_exits()) and (right_path not in player.current_room.get_exits()):
        # print("hello")
        update_dir_facing(back_path, direction_facing)
        player.travel(back_path)
        visited[previ].update({back_path: player.current_room.id})
        # visited[player.current_room.id].update({forward_path: previ})
        traversal_path.append(back_path)
    elif (left_path not in player.current_room.get_exits()) and (forward_path not in player.current_room.get_exits()):
        # print("drakness")
        update_dir_facing(right_path, direction_facing)
        player.travel(right_path)
        visited[previ].update({right_path: player.current_room.id})
        # visited[player.current_room.id].update({left_path: previ})
        traversal_path.append(right_path)
    elif (left_path not in player.current_room.get_exits()):
    # else:
        # print(forward_path, "my old friend")
        update_dir_facing(forward_path, direction_facing)
        player.travel(forward_path)
        visited[previ].update({forward_path: player.current_room.id})
        # visited[player.current_room.id].update({back_path: previ})
        traversal_path.append(forward_path)
    # elif (left_path in room.get_exits()) and (forward_path not in room.get_exits()) and (right_path not in room.get_exits()) and (left_path not in room.get_exits()):
    else:
        # print('I can go left')
        update_dir_facing(left_path, direction_facing)
        player.travel(left_path)
        visited[previ].update({left_path: player.current_room.id})
        # visited[player.current_room.id].update({right_path: previ})
        traversal_path.append(left_path) 

    if len(player.current_room.get_exits()) == 1:
        orig_direction = direction_facing
        only_room = player.current_room.get_exits()
        # print(only_room[0], 'for the love of GOD')
        # visited[previ].update({orig_direction: player.current_room.id})
        update_dir_facing(only_room[0], direction_facing)

    for d in incomplete_rooms:
        print(incomplete_rooms)
        if "?" not in visited[d].values():
            print('completed')
            incomplete_rooms.remove(d)
            try_this = True

    print(player.current_room.id, 'I think this might be the way')
    # for d in player.current_room.get_exits():
    #     print(visited[player.current_room.id].values())

player.current_room.print_room_description(player)

print(incomplete_rooms, room.id, visited, direction_facing, traversal_path, len(room_graph), "all the things")
# traveling(player.current_room)
# print(visited[0].get("completed"))
# print(len(visited[0]), 'length')
# print(visited[0].update({"w": 10}))

# update_dir_facing("e", direction_facing)


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
