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

# path the test will take
traversal_path = []

room = player.current_room

# dictionary of each visited room. Each entry has values for n,s,e,w
visited = {}

# List of rooms that still have "?" as a value in the visited entry for that room
incomplete_rooms = []

# Current room at [1], past room at [0]
curent_and_past_rooms = [0] * 2 

# Dictionary that has the paths from the last room with "?'s" to the current room. A new entry is made each time a new room with more than 1 direction that has not been explored yet
backtracking_path = {}

# Explores current player-room. Used in 
def explore_room(r, d):
    pr = curent_and_past_rooms[0] # past room from "curent_and_past_rooms"
    cr = curent_and_past_rooms[1] # curent room from "curent_and_past_rooms"

    # If this is a new room (not in visited dictionary)
    if r.id not in visited:
        # Create an "visited" dictionary entry
        visited[r.id] = {"w": "?", "n": "?", "e": "?", "s": "?"}

        # Set "None" as the default value for each of the 4 directions
        if "w" not in r.get_exits():
            visited[r.id].update({"w": None})
        if "n" not in r.get_exits():
            visited[r.id].update({"n": None})
        if "e" not in r.get_exits():
            visited[r.id].update({"e": None})
        if "s" not in r.get_exits():
            visited[r.id].update({"s": None})
        
        # Update the directional values for whatever the past room's directions
        if d == "w":
            visited[r.id].update({"e": curent_and_past_rooms[0]})
        if d == "n":
            visited[r.id].update({"s": curent_and_past_rooms[0]})
        if d == "e":
            visited[r.id].update({"w": curent_and_past_rooms[0]})
        if d == "s":
            visited[r.id].update({"n": curent_and_past_rooms[0]})

        # add this room to "incomplete_rooms" list    
        incomplete_rooms.append(r.id)

        # Swapping the "current_and_past_rooms" for the next room
        curent_and_past_rooms[1] = r.id
        pr = curent_and_past_rooms[0]
        curent_and_past_rooms[1], curent_and_past_rooms[0] = r.id, pr

    # If this room has been visited, then update the values for both in visited
    if r.id in visited:
        pr = curent_and_past_rooms[1] 
        cr = curent_and_past_rooms[0]

        # Updates past and curent rooms' directions
        if visited[r.id].get(d) is not None:
            if d == "w":
                visited[r.id].update({"e": curent_and_past_rooms[1]})
                visited[cr].update({"w": r.id})
            if d == "n":
                visited[r.id].update({"s": curent_and_past_rooms[1]})
                visited[cr].update({"n": r.id})
            if d == "e":
                visited[r.id].update({"w": curent_and_past_rooms[1]})
                visited[cr].update({"e": r.id})
            if d == "s":
                visited[r.id].update({"n": curent_and_past_rooms[1]})
                visited[cr].update({"s": r.id})

            curent_and_past_rooms[1], curent_and_past_rooms[0] = pr,r.id
    
            if "?" not in visited[curent_and_past_rooms[1]]:
                print('completed', curent_and_past_rooms[1])

        # Swaps the "curent_and_past_rooms" list values at 0 and 1
        curent_and_past_rooms[0], curent_and_past_rooms[1] = curent_and_past_rooms[0], r.id


    if len(player.current_room.get_exits()) > 2 and (player.current_room.id in visited):
        backtracking_path[player.current_room.id] = list()
        backtracking_path[player.current_room.id].append(player.current_room.id)
        last_unknown = player.current_room.id

    # checks to see if there are any "completed" rooms that can be removed from the "incomplete_rooms" list
    for e in incomplete_rooms:
        if "?" not in visited[e].values():
            incomplete_rooms.remove(e)
            print('removed', e)
            return


# Calls "explore_room", and gives directions for which way the player should move
def traversing():
    r = 0 # Counter for my temporary while-loop

    # Direction the player is facing (for updating the left, forward, right, and back paths)
    direction_facing = "n"

    # Base travel directions for when the player is facing north (updated in the while-loop)
    travel_directions = {
        "left_path": "w",
        "forward_path": "n",
        "right_path": "e",
        "back_path": "s"
    }

    # The last room with unexplored rooms (MAYBE I SHOULD MAKE THIS INTO A LIST INSTEAD???????)
    last_unknown = 0

    # for the while loop once completed
    continuing = True


    while r < 17:
        r += 1 # Temporary to keep from having tons of loops

        # Calls explore_room with the curent room and the direction the player is facing
        explore_room(player.current_room, direction_facing) 

        # Updates the direction the player is facing to be the last travel_direction used
        if len(traversal_path) > 0:
            direction_facing = traversal_path[-1]

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
        # If the left and forward paths are not in the room, then travel in the "right" path
        if (travel_directions.get("left_path") not in player.current_room.get_exits()) and (travel_directions.get("forward_path") not in player.current_room.get_exits()):
            right_path = travel_directions.get("right_path")
            player.travel(right_path)
            traversal_path.append(right_path)
            backtracking_path[last_unknown].append(right_path)
        # If the left and right paths are not in the room, then travel in the "forward" path
        elif (travel_directions.get("left_path") not in player.current_room.get_exits()) and (travel_directions.get("right_path") not in player.current_room.get_exits()):
            forward_path = travel_directions.get("forward_path")
            player.travel(forward_path)
            traversal_path.append(forward_path)
            backtracking_path[last_unknown].append(forward_path)
        # otherwise, take the left path
        else:
            left_path = travel_directions.get("left_path")
            player.travel(left_path)
            traversal_path.append(left_path) 
            backtracking_path[last_unknown].append(left_path)


        # If there are 2 exits in the room, append the direction and create a new list at this room
        if len(player.current_room.get_exits()) == 2:
            backtracking_path[last_unknown].append(direction_facing)
            backtracking_path[player.current_room.id] = list()
            backtracking_path[player.current_room.id].append(player.current_room.id)


        # If we have gotten back to a last unknown with a backtracking length greater than 1, we have hit a "loop", so we need to backtrack to the first room
        if  (player.current_room.id == last_unknown) and (len(backtracking_path) > 1):
            next_dir = backtracking_path[last_unknown].pop()
            if next_dir == "n":
                player.travel("s")
            if next_dir == "s":
               player.travel("n")
            if next_dir == "e":
                player.travel("w")
            if next_dir == "w":
                player.travel("e")

        # If the player hits a dead-end, they backtrack to the last unknown room and continue from there
        if len(player.current_room.get_exits()) == 1:
            next_dir = backtracking_path[last_unknown].pop()
            if next_dir == "n":
                player.travel("s")
            if next_dir == "s":
                player.travel("n")
            if next_dir == "e":
                player.travel("w")
            if next_dir == "w":
                player.travel("e")
            if next_dir == last_unknown:
                player.travel("e")
        
        # Prints the room description
        player.current_room.print_room_description(player)


# Invokes the "traversing" method
traversing()


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
