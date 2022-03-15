import threading
import time
from asyncio import Semaphore
# TODO uncomment imports
from Turbojet import Turbojet
from Turboprop import Turboprop
from Turbofan import TurboFan
from PeripheralHelper import PeripheralHelper


class Controller:
    # Output PWN controls
    jet_bool = False
    fan_bool = False

    def __init__(self, jet_output, prop_output, fan_output, conditions):
        self.p_helper = PeripheralHelper()
        # Store Outputs
        self.jet_output = jet_output
        self.prop_output = prop_output
        self.fan_output = fan_output
        self.conditions = conditions
        # Thread Controls
        self.jet_thread = None
        self.fan_thread = None
        self.prop_thread = None
        self.jet_thread_bool = True
        self.fan_thread_bool = True
        self.prop_thread_bool = True

    def start_threads(self):
        if self.jet_thread is None:
            self.jet_thread = threading.Thread(target=self.start_jet, args=(self.jet_output,))
            self.jet_thread_bool = True
            self.jet_thread.start()
        else:
            print("Jet thread already running")
        if self.fan_thread is None:
            self.fan_thread = threading.Thread(target=self.start_fan, args=(self.fan_output,))
            self.fan_thread_bool = True
            self.fan_thread.start()
        else:
            print("Fan thread already running")
        if self.prop_thread is None:
            self.prop_thread = threading.Thread(target=self.start_prop, args=(self.prop_output, self.conditions))
            self.prop_thread_bool = True
            self.prop_thread.start()
        else:
            print("Prop thread already running")

    def start_fan(self, outputs):
        # Run Turbofan
        print("\nThe Turbofan model is running\n")
        while self.fan_thread_bool:
            # Input two parameters from the electronics
            flight_level = self.p_helper.get_height()
            fuel_level = self.p_helper.get_fuel()
            print(f"The altitude is {str(flight_level * 500)} meters and the fuel flow is {str(fuel_level)} kg/s\n")
            # Init Turbo
            turbo_fan = TurboFan(flight_level, fuel_level)
            turbo_fan.engine_turbofan(outputs)
            if not Controller.jet_bool and Controller.fan_bool:
                self.p_helper.write_PWM(fuel_level)
            time.sleep(1)

#
    def start_prop(self, outputs, conditions):
        # Run Turboprop
        print("\nThe Turboprop model is running\n")
        time.sleep(0.6)
        while self.prop_thread_bool:
            # Input two parameters from the electronics
            flight_level = self.p_helper.get_height()
            fuel_level = self.p_helper.get_fuel()
            print(f"The altitude is {str(flight_level * 500)} meters and the fuel flow is {str(fuel_level)} kg/s\n")
            # Init Turbo
            turbo_prop = Turboprop(flight_level, fuel_level)
            conditions.update({'fuel': fuel_level})
            turbo_prop.engine_turboprop(outputs, conditions)
            time.sleep(1)
            
    def start_jet(self, outputs):
        print("\nThe Turbojet model is running\n")
        time.sleep(0.3)
        while self.jet_thread_bool:
            # Input two parameters from the electronics
            flight_level = self.p_helper.get_height()
            fuel_level = self.p_helper.get_fuel()
            print(f"The altitude is {str(flight_level * 500)} meters and the fuel flow is {str(fuel_level)} kg/s\n")
            # Init Turbo
            turbo_jet = Turbojet(flight_level, fuel_level)
            turbo_jet.engine_turbojet(outputs)
            if Controller.jet_bool and not Controller.fan_bool:
                self.p_helper.write_PWM(fuel_level)
            time.sleep(1)
            

