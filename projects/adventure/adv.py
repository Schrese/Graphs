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
# map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
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


traversal_path = []

room = player.current_room

visited = {}
completed_rooms = [0] * 2 

incomplete_rooms = []

backtracking_path = {}

def explore_room(r, d):
    # last_unknown = room.id
    print(incomplete_rooms)
    print(d, 'direction facing coming into the room')
    pr = completed_rooms[1]
    cr = completed_rooms[0]
    if r.id not in visited:
        visited[r.id] = {"w": "?", "n": "?", "e": "?", "s": "?"}
        if "w" not in r.get_exits():
            visited[r.id].update({"w": None})
        if "n" not in r.get_exits():
            visited[r.id].update({"n": None})
        if "e" not in r.get_exits():
            visited[r.id].update({"e": None})
        if "s" not in r.get_exits():
            visited[r.id].update({"s": None})
        if d == "w":
            visited[r.id].update({"e": completed_rooms[1]})
        if d == "n":
            visited[r.id].update({"s": completed_rooms[1]})
        if d == "e":
            visited[r.id].update({"w": completed_rooms[1]})
        if d == "s":
            visited[r.id].update({"n": completed_rooms[1]})
        incomplete_rooms.append(r.id)
        completed_rooms[1] = r.id
        pr = completed_rooms[0]
        completed_rooms[1], completed_rooms[0] = r.id, pr

    if r.id in visited:
        print('continuing', visited[r.id])
        pr = completed_rooms[1]
        cr = completed_rooms[0]
        # backtracking_path[r.id].append(d)

        if visited[r.id].get(d) is not None:
            if d == "w":
                visited[r.id].update({"e": completed_rooms[1]})
                visited[cr].update({"w": r.id})
            if d == "n":
                visited[r.id].update({"s": completed_rooms[1]})
                visited[cr].update({"n": r.id})
            if d == "e":
                visited[r.id].update({"w": completed_rooms[1]})
                visited[cr].update({"e": r.id})
            if d == "s":
                visited[r.id].update({"n": completed_rooms[1]})
                visited[cr].update({"s": r.id})

            completed_rooms[1], completed_rooms[0] = pr,r.id
    
            if "?" not in visited[completed_rooms[1]]:
                print('completed', completed_rooms[1])

    completed_rooms[0], completed_rooms[1] = completed_rooms[0], r.id


    if len(player.current_room.get_exits()) > 2 and (player.current_room.id in visited):
        backtracking_path[player.current_room.id] = list()
        backtracking_path[player.current_room.id].append(player.current_room.id)
        # backtracking_path[player.current_room.id].append(d)
        last_unknown = player.current_room.id

    print(backtracking_path, 'back it up!!!!!!')


    for e in incomplete_rooms:
        if "?" not in visited[e].values():
            incomplete_rooms.remove(e)
            print('removed', e)
            return

    # backtracking_path[1].update({tuple()})
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

    last_unknown = 0
    continuing = True

    # if (len(incomplete_rooms) <= 0) and (len(visited) == len(room_graph)):
    #     continuing = False

    # while r < 3000:
    while r < 17:
        print(player.current_room.id, completed_rooms, 'what is this looking like?')
        # global direction_facing
        if len(traversal_path) > 0:
            direction_facing = traversal_path[-1]
        # print("player in: ", player.current_room.id, "regular room is: ", room.id)
        r += 1
        explore_room(player.current_room, direction_facing) 
        previ = completed_rooms[0]
        # print(direction_facing, travel_directions, 'there must be something wrong here')

        # Sets travel directions depending on the direction facing
        if direction_facing == "s":
            travel_directions.update({"left_path": "e", "forward_path": "s", "right_path": "w", "back_path": "n"})

        elif direction_facing == "n":
            travel_directions.update({"left_path": "w", "forward_path": "n", "right_path": "e", "back_path": "s"})
        
        elif direction_facing == "e":
            travel_directions.update({"left_path": "n", "forward_path": "e", "right_path": "s", "back_path": "w"})

        else:
            travel_directions.update({"left_path": "s", "forward_path": "w", "right_path": "n", "back_path": "e"})


        # Actual Traversal Instructions
        if (travel_directions.get("left_path") not in player.current_room.get_exits()) and (travel_directions.get("forward_path") not in player.current_room.get_exits()):
            # print("drakness")
            right_path = travel_directions.get("right_path")
            player.travel(right_path)
            # visited[previ].update({right_path: player.current_room.id})
            # visited[player.current_room.id].update({left_path: previ})
            traversal_path.append(right_path)
            backtracking_path[last_unknown].append(right_path)
            # update_dir_facing(right_path, direction_facing)
        elif (travel_directions.get("left_path") not in player.current_room.get_exits()) and (travel_directions.get("right_path") not in player.current_room.get_exits()):
        # else:
            # print(forward_path, "my old friend")
            forward_path = travel_directions.get("forward_path")
            player.travel(forward_path)
            # visited[previ].update({forward_path: player.current_room.id})
            # visited[player.current_room.id].update({back_path: previ})
            traversal_path.append(forward_path)
            backtracking_path[last_unknown].append(forward_path)
            # update_dir_facing(forward_path, direction_facing)
        # elif (left_path in room.get_exits()) and (forward_path not in room.get_exits()) and (right_path not in room.get_exits()) and (left_path not in room.get_exits()):
        else:
            # print('I can go left')
            left_path = travel_directions.get("left_path")
            player.travel(left_path)
            # visited[previ].update({left_path: player.current_room.id})
            # visited[player.current_room.id].update({right_path: previ})
            traversal_path.append(left_path) 
            backtracking_path[last_unknown].append(left_path)
            # update_dir_facing(left_path, direction_facing)

        # if len(player.current_room.get_exits()) == 2:
        #     backtracking_path[last_unknown].append(direction_facing)

        # if  (player.current_room.id == last_unknown) and (len(backtracking_path) > 1):
        #     next_dir = backtracking_path[last_unknown].pop()

            # if next_dir == "n":
            #     player.travel("s")
            # if next_dir == "s":
            #    player.travel("n")
            # if next_dir == "e":
            #     player.travel("w")
            # if next_dir == "w":
            #     player.travel("e")

        # if len(player.current_room.get_exits()) == 1:
        #         # orig_direction = direction_facing
        #         # back_path = travel_directions.get("back_path")
        #         # print(back_path, 'this should be east for all of these')
        #         # only_room = player.current_room.get_exits()
        #     next_dir = backtracking_path[last_unknown].pop()
        #     if next_dir == "n":
        #         player.travel("s")
        #     if next_dir == "s":
        #         player.travel("n")
        #     if next_dir == "e":
        #         player.travel("w")
        #     if next_dir == "w":
        #         player.travel("e")
        #     if next_dir == last_unknown:
        #         player.travel("e")
        # #     # else:
        
        print(visited, 'interesting things')
        player.current_room.print_room_description(player)
do_things()


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
