import threading
import time

# TODO uncomment imports
# from Turbojet import Turbojet
# from Turboprop import Turboprop
# from Turbofan import TurboFan
# from PeripheralHelper import PeripheralHelper


class Controller:
    jet_bool = False
    fan_bool = False

    def __init__(self, outputs):
        # self.p_helper = PeripheralHelper()
        # Store Outputs
        self.outputs = outputs
        # Thread Controls
        self.jet_thread = None
        self.fan_thread = None
        self.prop_thread = None
        # Output PWM Controls
        self.jet_or_fan = None

    def start_threads(self):
        if self.jet_thread is None:
            self.jet_thread = threading.Thread(target=self.dummy_thread, args=("jet",))
            # self.jet_thread = threading.Thread(target=self.start_jet, args=(self.outputs, self.jet_bool))
            self.jet_bool = True
            self.jet_thread.start()
        else:
            print("Jet thread already running")
        if self.fan_thread is None:
            self.fan_thread = threading.Thread(target=self.dummy_thread, args=("fan",))
            # self.fan_thread = threading.Thread(target=self.start_fan, args=(self.outputs, self.fan_bool))
            self.fan_bool = True
            self.fan_thread.start()
        else:
            print("Fan thread already running")
        if self.prop_thread is None:
            self.prop_thread = threading.Thread(target=self.dummy_thread, args=("prop",))
            # self.prop_thread = threading.Thread(target=self.start_prop, args=(self.outputs,))
            self.prop_thread.start()
        else:
            print("Prop thread already running")

    def dummy_thread(self, val):
        while True:
            print(val)
            time.sleep(1)
# TODO: Uncomment the below

#     def start_fan(self, outputs):
#         # Run Turbofan
#         print("\nThe Turbofan model is running\n")
#         while True:
#             # Input two parameters from the electronics
#             flight_level = self.p_helper.get_height()
#             fuel_level = self.p_helper.get_fuel()
#             print(f"The altitude is {str(flight_level * 500)} meters and the fuel flow is {str(fuel_level)} kg/s\n")
#             # Find other IC's
#             turbo_fan = TurboFan(flight_level, fuel_level)
#             # P_a, C_a, T_a = turbo_fan.get_conditions()
#             # print(f"The IC for Temperature is {T_a}")
#             # print(f"The IC for Speed is {C_a}")
#             # print(f"The IC for Pressure is {P_a}\n")
#             # Go throughout the engine to determine all other parameters
#             turbo_fan.engine_turbofan(outputs)
#             if not Controller.jet_bool and Controller.fan_bool:
#                 # TODO Send PWM
#                 pass
#             self.p_helper.write_lcd("")
#         pass
#
#     def start_prop(self, outputs):
#         # Run Turboprop
#         print("\nThe Turboprop model is running\n")
#         while True:
#             # Input two parameters from the electronics
#             flight_level = self.p_helper.get_height()
#             # fuel_level = float(input("What is your fuel flow rate (in kg/s) "))
#             fuel_level = self.p_helper.get_fuel()
#             print(f"The altitude is {str(flight_level * 500)} meters and the fuel flow is {str(fuel_level)} kg/s\n")
#             # Find other IC's
#             turbo_prop = Turboprop(flight_level, fuel_level)
#             # P_a, C_a, T_a = turbo_prop.get_conditions()
#             # print(f"The IC for Temperature is {T_a}")
#             # print(f"The IC for Speed is {C_a}")
#             # print(f"The IC for Pressure is {P_a}\n")
#             # Go throughout the engine to determine all other parameters
#             turbo_prop.engine_turboprop(outputs)
#
#     def start_jet(self, outputs):
#         print("\nThe Turbojet model is running\n")
#         while True:
#             # Input two parameters from the electronics
#             flight_level = self.p_helper.get_height()
#             fuel_level = self.p_helper.get_fuel()
#             print(f"The altitude is {str(flight_level * 500)} meters and the fuel flow is {str(fuel_level)} kg/s\n")
#             # Find other IC's
#             turbo_jet = Turbojet(flight_level, fuel_level)
#             # P_a, C_a, T_a = turbo_jet.get_conditions()
#             # print(f"The IC for Temperature is {T_a}")
#             # print(f"The IC for Speed is {C_a}")
#             # print(f"The IC for Pressure is {P_a}\n")
#             # Go throughout the engine to determine all other parameters
#             turbo_jet.engine_turbojet(outputs)
#             if Controller.jet_bool and not Controller.fan_bool:
#                 # TODO Send PWM
#                 pass
#             self.p_helper.write_lcd("")

