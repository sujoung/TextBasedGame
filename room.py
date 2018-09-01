class Room:
    def __init__(self,room_name,door_list,player,item_list): # add item object later
        self.room_name = room_name
        self.door_list = door_list # list of object(s)
        self.dir_list = [] # list of name of door direction
        self.door_info = {}
        # {door1: N, open, Hall, Bedroom}
        self.item_list = item_list
        self.item_info = {}
        self.it_list = [] # list of name of door direction
        self.player = player
        self.current_room = self.player.current_room
        self.true_sight = self.player.true_sight

        if self.door_list:

            for door in self.door_list:

                if self.room_name == door.room_1:
                    self.door_info[door.name] = [door.direction_1, door.status,
                                            door.room_1, door.room_2]

                elif self.room_name == door.room_2:
                    self.door_info[door.name] = [door.direction_2,door.status,
                                                 door.room_2, door.room_1]

        for i in self.door_info:
            self.dir_list.append(self.door_info[i][0])

        #self.item_list = {room name : [item objects]}
        if self.item_list:
            for item in self.item_list:
                self.item_info[item.name] = [item.name, item.room_name,
                                             item.type, item.action]

        for i in self.item_info:
            if not self.player.true_sight:
                self.it_list.append(self.item_info[i][0])

        if 'key' in self.it_list and not self.player.true_sight:
            self.it_list.remove('key')





    def showRoom(self):
        print("You are in the {}.".format(self.room_name))

        if len(self.dir_list) == 1:
            print("There is a door towards",self.dir_list[0].upper()+".")

        elif len(self.dir_list) >= 2:
            print("There are doors towards", end='')
            for i in self.dir_list:
                print(" " + i.upper() + ".", end= '')
            print("")

        if self.it_list:

            if self.player.true_sight:
                print("In this room, there are following items: ")
                print(','.join([' '.join(x.split('_')) \
                                for x in self.it_list])+ ".")

            if not self.player.true_sight:
                temp = ','.join([' '.join(x.split('_')) \
                        for x in self.it_list if x != 'key'])
                if temp:
                    print("In this room, there are following items: ")
                    print(temp+".")


        elif not self.it_list:
            print("There are no items in this room.")

        else:
            print("There is no door.")



    def moveRoom(self,command,direction,door_obj,room_objects):

        if command == 'go':

            if door_obj.status == 'open':
                door_obj.passOpenedDoor()

                if self.player.current_room.room_name == door_obj.room_1:
                    self.player.changeRoom(room_objects[door_obj.room_2])

                elif self.player.current_room.room_name == door_obj.room_2:
                    self.player.changeRoom(room_objects[door_obj.room_1])

                self.player.current_room.showRoom()

            elif door_obj.status == 'closed':
                door_obj.closedDoor()

            elif door_obj.status == 'locked':
                door_obj.lockedDoor()

        if command == 'open':

            if door_obj.status == 'open':
                print("The door is already opened, please go through this door.")

            elif door_obj.status == 'closed':
                door_obj.openTheDoor()

            elif door_obj.status == 'locked':
               print("The door is locked. Unlock the door first.")

        if command == 'unlock':

            if door_obj.status == 'open':
                print("The door is already opened, please go through this door.")

            elif door_obj.status == 'closed':
                print("The door is aready unlocked, please open the door.")

            elif door_obj.status == 'locked':
               door_obj.unlockTheDoor(self.player)


    def clairvoyance(self):
        self.it_list = []
        if self.player.true_sight:
            for i in self.item_info:
                self.it_list.append(self.item_info[i][0])




