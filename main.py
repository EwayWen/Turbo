from Turbojet import Turbojet
from Turboprop import Turboprop
from Turbofan import TurboFan
import Constants as C
from PeripheralHelper import PeripheralHelper
from GUI import GUI
from Controller import Controller

def main():
    gui = GUI()
    gui.init_gui()

    # Welcome
    print("Hello and welcome to the automatic Aerodynamic Cycle calculator for Turbojet, Turboprop and Turbofan\n")

    # Height Levels for all engines

    # Enter which model is being simulated

    user_input = None
    while True:
        while True:
            print("To model the Turbojet enter 1.")
            print("To model the Turboprop enter 2.")
            print("To model the Turbofan enter 3.")
            print("To exit, enter 'exit'.")
            user_input = input("Which Engine Model would you like to simulate? ").lower().strip()
            if user_input in "123" and len(user_input) == 1:
                model = int(user_input)
                break
            elif user_input == "exit":
                return
            else:
                print("Invalid input.")

        if model == 1:
            # Run Turbojet
            pass

        elif model == 2:
            pass

        elif model == 3:
            pass



if __name__ == "__main__":
    main()
