import sys
import re
from door import Door
from room import Room
from item import Item
from character import Character

class Configuration():
    """Reads a game configuration text file"""

    def __init__(self):

        input = ''
        self.allt = []
        self.rooms = []
        self.items = {}
        self.doors = {}
        self.texts = {}
        self.current_room = ''
        count = 1

        try:
            with open(sys.argv[1], 'r') as self.fh:
                for sen in self.fh:
                    sen = sen.split()
                    if sen:
                        self.allt.append([x.lower() for x in sen])

            for line in self.allt:
                if line[0] == 'room':
                    self.rooms.append(line[1])

                if line[0] == 'door':
                    # {door_1 :(dir1, dir2, status, room_1, room_2)}
                    door_name = '{}{}'.format('door',count)
                    self.doors[door_name] = (line[1][0],line[1][2],\
                                             line[2], line[3], line[4])
                    count += 1

                if line[0] == 'item':
                    # {item_name : (room, type, *action)}
                    if len(line) > 4:
                        self.items[line[1]] = (line[2], line[3], line[4])
                    else:
                        self.items[line[1]] = (line[2], line[3])

                if line[0] == 'read':
                    if line[1] == 'note':
                        self.texts['note'] = ' '.join(line[2:])
                    elif line[1] == 'book':
                        self.texts['book'] = ' '.join(line[2:])

                if line[0] == 'start':
                    self.current_room = line[1]


        except TypeError:
            print("Error: there is no such file")
            sys.exit(2)


class GameManager(Configuration):

    def __init__(self):
        super().__init__()
        self.door_in_room = {} # dict of door objects
        self.item_in_room = {} # dict of item objects
        self.comm = [] # List of available commands

        # ==== ASSIGN PLAYER USING CHARACTER CLASS ====#
        true_sight = False
        self.player = Character(self.current_room, true_sight)

        #============= ASSIGN DOOR CLASS OBJECTS ===============#

        self.door_objects = {}
        for k,v in self.doors.items():
            self.door_objects[k] = Door(k,v[0],v[1],v[2],v[3],v[4])

        #============= ASSIGN ITEM  CLASS OBJECTS =================#

        self.item_objects = {}

        for k,v in self.items.items():
            if len(v)==3:
                self.item_objects[k] = Item(k,v[0],v[1],self.player,v[2])
                self.comm.append(v[2])
            else:
                self.item_objects[k] = Item(k,v[0],v[1],self.player)

        #============= Items in room, Doors in room ===============#

        # Make dictionary of available doors in each room#
        for room in self.rooms:
            # door_in_room = {room_name : door_1, door_2}
            for k,v in self.door_objects.items():
                if v.room_2 == room:
                    if room not in self.door_in_room:
                        self.door_in_room[room] = [v]
                    else:
                        self.door_in_room[room] += [v]
                elif v.room_1 == room:
                    if room not in self.door_in_room:
                        self.door_in_room[room] = [v]
                    else:
                        self.door_in_room[room] += [v]

            if room not in self.door_in_room:
                self.door_in_room[room] = []

        # Make dictionary of available items in each room#
        for room in self.rooms:
            # item_in_room = {room_name : item_1, item_2}
            for k,v in self.item_objects.items():
                if v.room_name == room:
                    if room not in self.item_in_room:
                        self.item_in_room[room] = [v]
                    else:
                        self.item_in_room[room] += [v]
            if room not in self.item_in_room:
                self.item_in_room[room] = []

        # ==== ASSIGN ROOM CLASS OBJECTS USING DOORS AND ITEMS====== #
        self.room_objects = {}
        for room in self.rooms:
            self.room_objects[room]=(Room(room,self.door_in_room[room],\
                                          self.player,self.item_in_room[room]))

        #==========Set current room, overwrites the str==========#
        self.current_room = self.room_objects[self.current_room]
        self.player.current_room = self.current_room



    def exit(self):
        sys.exit(2)

    def userInput(self):

        user_input = self.getInput()

        command, *content = user_input.split(' ')

        # ==================== CONDITION  ========================#
        self.start_game = ['1', '2', 'start', 'exit']
        # ==================== ALLOCATION  ========================#
        if command == 'show':
            self.player.current_room.showRoom()

        elif command == 'commands':
            print("+ go Dir: Let’s the player move to the room in direction DIR,\n\
                   if there is an open door in that direction.")

            print("+ take ITEM: Let’s the player take the item ITEM \n\
                    if it is in the same room as the player, and \n\
                    ITEM is not a STATIONARY item. The item should \n\
                    then be held by the player, and no longer\n\
                    available in the room.")

            print("+ release ITEM: Let’s the player release item ITEM, \n\
                   if he holds it. The item will then be in the room the player\n\
                   is in, and should no longer be held by the player.")

            print("+ open DIR: Opens the door in direction DIR in the current room, \n\
                   if there is such a door, and if that door is closed.")

            print("+ show: Describes the room the player is currently \n\
                in, i.e. gives its name, lists the doors, and the \n\
                available items, if any.")

            print("+ commands: Lists all available commands in the game.")

            print("+ holding: Lists all the items the player is currently holding.")

            print("+ quit: Ends the game.")

            print("+ examine ITEM : shows the type of item and command for use")

            print(" ... and there are additional commands: ", end ='')

            print(', '.join(set(self.comm)))

        elif command == 'quit':
            print("Thank you for playing this game")
            self.exit()

        elif command == 'holding':
            self.player.showInventory()

        elif command == 'take': #Item related
            self.current_room = self.player.current_room
            if len(content) == 1 and content[0] \
                in self.current_room.it_list:
                x = self.item_objects[content[0]]
                self.player.takeItem(x)

            elif len(content) >= 2 and self.slicing(content) \
                    in self.current_room.it_list:
                x = self.item_objects[self.slicing(content)]
                self.player.takeItem(x)

            elif not content:
                print("What do you mean?")
                return

            else:
                print("There is no such item.")
                return

        elif command == 'release': #Item related
            self.current_room = self.player.current_room
            if len(content) == 1 and content[0] \
                    in self.player.inventory:
                y = self.item_objects[content[0]]
                self.player.releaseItem(y)

            elif len(content) >= 2 and self.slicing(content) \
                     in self.player.inventory:
                y = self.item_objects[self.slicing(content)]
                self.player.releaseItem(y)

            elif not content:
                print("What do you mean?")
                return

            else:
                print("You don't have such item.")
                return

        elif command in self.comm: # unlock, read, sleep
            self.current_room = self.player.current_room

            if len(content) == 1 and content:

                if content[0] not in ['n','e','w','s']\
                    and (content[0] in self.current_room.it_list\
                    or content[0] in self.player.inventory):
                    w = self.item_objects[content[0]]
                    self.player.useItem(command, w,self.texts)

                elif (content[0] not in self.current_room.it_list\
                    or content[0] in self.player.inventory)\
                    and command != 'unlock':
                    print("There is no such item")

                elif content[0] in ['n','e','w','s'] and\
                    command == 'unlock':
                    for door_obj in self.current_room.door_list:
                        if door_obj.direction_1 == content[0]:
                            self.current_room.moveRoom\
                                (command, content[0], door_obj,
                                 self.room_objects)
                        if door_obj.direction_2 == content[0]:
                            self.current_room.moveRoom\
                                (command, content[0], door_obj,
                                 self.room_objects)

                        elif content[0] not in self.current_room.dir_list:
                            print("There is no door.")
                            return

                elif content[0] not in ['n','e','w','s']\
                    and command == 'unlock':
                    print("This is not a direction.")
                    return

                elif content[0] in ['n','e','w','s']\
                    and command != 'unlock':
                    print("This is not an item, this is a direction.")
                    return

            elif len(content) >= 2 and self.slicing(content) \
                in self.item_objects:
                w = self.slicing(content)
                w = self.item_objects[w]
                self.player.useItem(command,w,self.texts)

            elif not content:
                print("What do you mean?")
                return

            else:
                print("There is no such item.")
                return

        elif command == 'examine': #Item related
            self.current_room = self.player.current_room

            if len(content) == 1 and (content[0] \
                    in self.player.inventory or\
                    content[0] in self.current_room.it_list):
                z = self.item_objects[content[0]]

            elif len(content) >= 2 and (self.slicing(content) \
                in self.player.inventory or self.slicing(content)\
                in self.current_room.it_list):
                z = self.item_objects[self.slicing(content)]

            elif not content:
                print("What do you mean?")
                return

            else:
                print("You don't have such item.")
                return

            z.showItemFeature()

        elif command in ['go','open']:


            self.current_room = self.player.current_room

            if content:
                content = content[0]



            elif not content:
                print("please type either go or open and direction")
                return

            if content not in ['n','e','w','s']:
                print("This is not a direction.")
                return

            if content in ['n','e','w','s'] and\
                content not in self.current_room.dir_list:
                print("There is no door in that direction")
                return

            for door_obj in self.current_room.door_list:

                if content == door_obj.direction_1 and\
                self.current_room.room_name == door_obj.room_1:

                    self.current_room.moveRoom(command,content,door_obj,\
                                               self.room_objects)

                if content == door_obj.direction_2 and\
                self.current_room.room_name == door_obj.room_2:

                    self.current_room.moveRoom(command,content,door_obj,\
                                               self.room_objects)


        else:
            print("This is not a valid command, Try again!")

    def main(self):
        self.welcome()
        self.mainInfo(self.player)
        while True:
            self.userInput()

    def getInput(self):
        return input("--> ").lower()

    def slicing(self,content):
        return '_'.join([content[0], content[1]])


    def welcome(self):
        print()
        print("WELCOME TO OUR MYSTERIOUS HOUSE GAME!")
        print("If you want to see commands, type 'commands'\n")
        print("Here are your options:")
        print("\n1. START")
        print("2. EXIT\n")

        while True:
            user_input = self.getInput()
            if user_input in ("1","start"):
                return
            elif user_input in ("2","exit"):
                print("See you next time!")
                self.exit()
            else:
                print("Please choose an option. (1.START, 2.EXIT)")


    def mainInfo(self,player):
        self.current_room = self.player.current_room
        self.current_room.showRoom()
        return

def main():
    x = Configuration()

if __name__ == "__main__":
    main()


play = GameManager()
play.main()