import threading
import tkinter as tk
from Controller import Controller
from tkinter.scrolledtext import ScrolledText
import time


class GUI:

    def __init__(self):
        # GUI Thread
        self.thread = None
        self.thread_bool = True
        # Controller
        self.jet_output = {}
        self.prop_output = {}
        self.fan_output = {}
        self.conditions = {}
        self.controller = Controller(self.jet_output, self.prop_output, self.fan_output, self.conditions)
        # self.controller = None
        self.controller.start_threads()
        # TK start
        self.window = tk.Tk()
        # Frames
        self.prop_frame = tk.Frame(master=self.window)
        self.jet_frame = tk.Frame(master=self.window)
        self.fan_frame = tk.Frame(master=self.window)
        self.output_frame = tk.Frame(master=self.window)
        # Labels
        self.height_label = tk.Label(text="Height: ", master=self.output_frame, width=30, justify="left", anchor="nw")
        self.pressure_label = tk.Label(text="Pressure: ", master=self.output_frame, width=30, justify="left", anchor="nw")
        self.speed_label = tk.Label(text="Speed: ", master=self.output_frame, width=30, justify="left", anchor="nw")
        self.temperature_label = tk.Label(text="Temperature: ", master=self.output_frame, width=30, justify="left", anchor="nw")
        self.fuel_label = tk.Label(text="Fuel: ", master=self.output_frame, width=30, justify="left", anchor="nw")
        self.fan_label = tk.Label(text="Turbofan", master=self.fan_frame)
        self.prop_label = tk.Label(text="Turboprop", master=self.prop_frame, anchor="n")
        self.jet_label = tk.Label(text="Turbojet", master=self.jet_frame)
        self.mode_label = tk.Label(text="Mode: None; use buttons.", master=self.output_frame)
        # Texts
        self.jet_text = ScrolledText(master=self.jet_frame, height=20, width=40)
        self.fan_text = ScrolledText(master=self.fan_frame, height=20, width=40)
        self.prop_text = ScrolledText(master=self.prop_frame, height=20, width=40)
        # Buttons
        self.jet_button = tk.Button(text="Switch", master=self.jet_frame, width=10)
        self.prop_button = tk.Button(text="", master=self.prop_frame, width=10)
        self.fan_button = tk.Button(text="Switch", master=self.fan_frame, width=10)
        self.clear_button = tk.Button(text="Clear Mode", master=self.output_frame, width=10) 
        self.exit_button = tk.Button(text="Exit", master=self.output_frame, width=10)

    def init_gui(self):
        # Jet Frame
        self.jet_label.pack()
        self.jet_button.pack()
        self.jet_button.bind("<Button-1>", self.jet_button_press)
        self.jet_text.pack(side=tk.LEFT)
        # Prop Frame
        self.prop_label.pack()
        self.prop_button.pack()
        self.prop_button.bind("<Double-1>", self.prop_button_press)
        self.prop_text.pack(side=tk.LEFT)
        # Fan Frame
        self.fan_label.pack()
        self.fan_button.pack()
        self.fan_button.bind("<Button-1>", self.fan_button_press)
        self.fan_text.pack(side=tk.LEFT)
        # Output Frame
        self.mode_label.pack()
        self.height_label.pack()
        self.pressure_label.pack()
        self.speed_label.pack()
        self.temperature_label.pack()
        self.fuel_label.pack()
        self.clear_button.pack()
        self.clear_button.bind("<Button-1>", self.clear_button_press)
        self.exit_button.pack()
        self.exit_button.bind("<Button-1>", self.exit_button_press)
        # Grid
        self.prop_frame.grid(row=0, column=0)
        self.fan_frame.grid(row=0, column=2)
        self.jet_frame.grid(row=0, column=1)
        self.output_frame.grid(row=0, column=3)
        # Start GUI thread
        self.thread = threading.Thread(target=self.set_outputs)
        self.thread.start()
        # Start TK
        tk.mainloop()

    def jet_button_press(self, event):
        print("jet")
        Controller.jet_bool = True
        Controller.fan_bool = False
        self.mode_label['text'] = "Mode: Turbojet"

    def fan_button_press(self, event):
        print("fan")
        Controller.jet_bool = False
        Controller.fan_bool = True
        self.mode_label['text'] = "Mode: Turbofan"


    def clear_button_press(self, event):
        print("exit")
        Controller.jet_bool = False
        Controller.fan_bool = False
        self.controller.p_helper.write_PWM(0.0)
        self.mode_label['text'] = "Mode: None; use buttons."
        
    def exit_button_press(self, event):
        self.controller.p_helper.write_PWM(0.0)
        self.controller.fan_thread_bool = False
        self.controller.jet_thread_bool = False
        self.controller.prop_thread_bool = False
        self.thread_bool = False
        self.window.destroy()
        
    def prop_button_press(self, event):
        self.prop_button['text'] = ":)"

    # Updates the text in the GUI
    def set_outputs(self):
        while self.thread_bool:
            conditions = self.conditions
            if conditions is not None:
                
                self.height_label['text'] = f"Height: {conditions.get('height', None)}"
                self.speed_label['text'] = f"Speed: {conditions.get('speed', None)}"
                self.temperature_label['text'] = f"Temperature: {conditions.get('temperature', None)}"
                self.pressure_label['text'] = f"Pressure: {conditions.get('pressure', None)}"
                self.fuel_label['text'] = f"Fuel: {conditions.get('fuel', None)}"
                self.jet_text.delete(1.0, 'end')
                self.jet_text.insert(1.0, self.jet_output.get('out', ""))
                self.fan_text.delete(1.0, 'end')
                self.fan_text.insert(1.0, self.fan_output.get('out', ""))
                self.prop_text.delete(1.0, 'end')
                self.prop_text.insert(1.0, self.prop_output.get('out', ""))
            # Wait 1 second between updates
            time.sleep(1)
