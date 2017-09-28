from cabinet_utils import *

if __name__ == "__main__":

    CabinetHelper.register()

    #listen for commands
    while(True):
        newdrink = CabinetHelper.get_order()
        print(newdrink.name)