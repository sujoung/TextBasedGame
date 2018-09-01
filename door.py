class Door:
    def __init__(self,name,direction_1,direction_2,status,room_1,room_2):
        self.name = name
        self.direction_1 = direction_1
        self.direction_2 = direction_2
        self.status = status
        self.room_1 = room_1
        self.room_2 = room_2

    def passOpenedDoor(self):
        print("You just passed the door.")

    def closedDoor(self):
        print("The door is closed. Please open the door.")

    def openTheDoor(self):
        #change the door status to 'open' and pass the door
        self.status = 'open'
        print("You opened the door to the next room.")

    def lockedDoor(self):
        if self.status == 'locked':
            print("The door is locked. You need a key.")
            print("If you have a key, please unlock it.")

    def unlockTheDoor(self,player):
        self.player = player
        if 'key' in self.player.inventory:
            self.status = 'open'
            print("You unlocked the door.")
            print("Please go through the door")
        else:
            print("You don't have the key.")


