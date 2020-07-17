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

visited = {}
completed_rooms = [0] * 2 
# incomplete_rooms.append(player.current_room.id)
try_this = False
last_direction = ""

def explore_room(r, d):
    incomplete_rooms = []
    # print(direction_facing, 'from in exploration')
    # previous_room_id = r.id
    # print(previous_room_id, "a;isjd;fije;oaijsd;ofijoeaijdf")
    print(d, 'direction facing coming into the room')
    if r.id not in visited:
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
        completed_rooms[1] = r.id
        # completed_rooms[0] = d
        completed_rooms[1], completed_rooms[0] = completed_rooms[0], completed_rooms[1]
        # print(exits, 'exits')
    if r.id in visited:
        print('continuing')
        pr = completed_rooms[1]
        fr = completed_rooms[0]
        # completed_rooms[0] = r.id
        # completed_rooms[1] = pr

        # completed_rooms[1], completed_rooms[0] = completed_rooms[0], completed_rooms[1]
        if d == "w":
            visited[r.id].update({"e": completed_rooms[1]})
            visited[fr].update({"w": r.id})
            print(';aosidjf;oeijao;sidjf;oijeoa;ijsdo;fijeo;aijs;dfijo;eijaf')
        if d == "n":
            visited[r.id].update({"s": completed_rooms[1]})
            visited[fr].update({"n": r.id})
        if d == "e":
            visited[r.id].update({"w": completed_rooms[1]})
            visited[fr].update({"e": r.id})
        if d == "s":
            visited[r.id].update({"n": completed_rooms[1]})
            visited[fr].update({"s": r.id})

        completed_rooms[1], completed_rooms[0] = pr,r.id
    # return previous_room_id



# while len(traversal_path) < len(room_graph):
def do_things():
    r = 0
    # This will need to be updated to be the last direction that the player moved in
    direction_facing = "n"
    # This will get updated when "direction_facing" gets updated. It's the next path that the player will look for
    travel_directions = {
        "left_path": "w",
        "forward_path": "n",
        "right_path": "e",
        "back_path": "s"
    }

    while r < 20:
        print(player.current_room.id, completed_rooms, 'what is this looking like?')
        # global direction_facing
        if len(traversal_path) > 0:
            direction_facing = traversal_path[-1]
        # print("player in: ", player.current_room.id, "regular room is: ", room.id)
        r += 1
        explore_room(player.current_room, direction_facing) 
        previ = completed_rooms[0]
        # print(direction_facing, travel_directions, 'there must be something wrong here')

        if direction_facing == "s":
            travel_directions.update({"left_path": "e", "forward_path": "s", "right_path": "w", "back_path": "n"})

        elif direction_facing == "n":
            travel_directions.update({"left_path": "w", "forward_path": "n", "right_path": "e", "back_path": "s"})
        
        elif direction_facing == "e":
            travel_directions.update({"left_path": "n", "forward_path": "e", "right_path": "s", "back_path": "w"})

        else:
            travel_directions.update({"left_path": "s", "forward_path": "w", "right_path": "n", "back_path": "e"})

        previ = 0

        # if player.current_room.id == room.id:
        #     print('move along, nothing to see here')

        if (travel_directions.get("left_path") not in player.current_room.get_exits()) and (travel_directions.get("forward_path") not in player.current_room.get_exits()) and (travel_directions.get("right_path") not in player.current_room.get_exits()):
            # print("hello")
            back_path = travel_directions.get("back_path")
            direction_facing = back_path
            player.travel(back_path)
            # visited[previ].update({back_path: player.current_room.id})
            # visited[player.current_room.id].update({forward_path: previ})
            traversal_path.append(back_path)
        elif (travel_directions.get("left_path") not in player.current_room.get_exits()) and (travel_directions.get("forward_path") not in player.current_room.get_exits()):
            # print("drakness")
            right_path = travel_directions.get("right_path")
            player.travel(right_path)
            # visited[previ].update({right_path: player.current_room.id})
            # visited[player.current_room.id].update({left_path: previ})
            traversal_path.append(right_path)
            # update_dir_facing(right_path, direction_facing)
        elif (travel_directions.get("left_path") not in player.current_room.get_exits()):
        # else:
            # print(forward_path, "my old friend")
            forward_path = travel_directions.get("forward_path")
            player.travel(forward_path)
            # visited[previ].update({forward_path: player.current_room.id})
            # visited[player.current_room.id].update({back_path: previ})
            traversal_path.append(forward_path)
            # update_dir_facing(forward_path, direction_facing)
        # elif (left_path in room.get_exits()) and (forward_path not in room.get_exits()) and (right_path not in room.get_exits()) and (left_path not in room.get_exits()):
        else:
            print('I can go left')
            left_path = travel_directions.get("left_path")
            player.travel(left_path)
            # visited[previ].update({left_path: player.current_room.id})
            # visited[player.current_room.id].update({right_path: previ})
            traversal_path.append(left_path) 
            # update_dir_facing(left_path, direction_facing)
        
        if len(player.current_room.get_exits()) == 1:
            orig_direction = direction_facing
            back_path = travel_directions.get("back_path")
            print(back_path, 'this should be east for all of these')
            only_room = player.current_room.get_exits()
            # print(only_room[0], 'for the love of GOD')
            # visited[previ].update({orig_direction: player.current_room.id})
            # visited[player.current_room.id].update({back_path: previ})s
            # update_dir_facing(only_room[0], direction_facing)
        # for i in visited:
        #     print(visited[i])
        # for d in incomplete_rooms:
        #     # print(incomplete_rooms)
        #     if "?" not in visited[d].values():
        #         print('completed')
        #         incomplete_rooms.remove(d)
        #         try_this = True
do_things()

player.current_room.print_room_description(player)

print(visited, traversal_path, len(room_graph), "all the things")

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
