
class Item:
    def __init__(self,item_name,room_name,type,player,action = None,):
        self.name = item_name
        self.room_name = room_name
        self.type = type
        self.player = player
        self.action = action


    def showItemFeature(self):

        if self.type == 'move':
            print("This is movable item.")
            print("You can take or release the item.")

        if self.type == 'stationary':
            print("This item is stationary.")
            print("You cannot take the item.")

        if self.type == 'use':
            print("This item is movable and usable.")
            print("You can take, release item or {}."\
                  .format(self.action))
