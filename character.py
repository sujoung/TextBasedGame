import sys
import time

class Character:
    def __init__(self,current_room,true_sight):
        self.current_room = current_room
        self.true_sight = true_sight
        self.inventory = []

    def changeRoom(self,room_to):
        self.current_room = room_to # room_to is object

    def showInventory(self):
        if self.inventory:
            print("You have", ','.join([x.replace('_',' ') \
                                        for x in self.inventory]))
        else:
            print("You don't have any items now.")

    def takeItem(self,item_obj):

        if item_obj.type == 'stationary':
            print("You cannot take this item.")

        elif item_obj.type in ['use','move']:
            self.inventory.append(item_obj.name)

            self.current_room.item_list.remove(item_obj)
            del self.current_room.item_info[item_obj.name]
            self.current_room.it_list.remove(item_obj.name)
            print("You took the item : {}."\
                  .format(item_obj.name.replace('_',' ')))

    def releaseItem(self,item_obj):


        self.inventory.remove(item_obj.name)

        self.current_room.item_list.append(item_obj)
        self.current_room.item_info[item_obj.name] = [item_obj.name,
                                                      item_obj.room_name,
                                                      item_obj.type,
                                                      item_obj.action]
        self.current_room.it_list.append(item_obj.name)

        print("You released the item : {}."\
              .format(item_obj.name.replace('_',' ')))

        #====== GAME ENDING =====#
        if self.current_room.room_name == 'bathroom' and\
                item_obj.name == 'rubber_duck':
            time.sleep(1.5)
            print("Wait...!")
            self.gameEnding()



    def useItem(self,command,content,text):
        self.texts = text

        if command == 'read' and content.action == 'read':
            print(self.texts[content.name])

        elif command == 'sleep' and content.action == 'sleep':
            time.sleep(1)
            print("You slept very well, Your tiredness is gone")
            print("...")
            time.sleep(2)
            self.true_sight = True
            print("You acquired the true sight!")
            self.current_room.clairvoyance()

        else:
            print("You cannot use item in that way.")



    def gameEnding(self):
        time.sleep(1.5)
        print("...")
        time.sleep(2)
        print("Mr. Rubber duck: Thank you. I can finally swim in the bath tub")
        time.sleep(2)
        print("...")
        time.sleep(1.5)
        print("GAME END")
        sys.exit(2)