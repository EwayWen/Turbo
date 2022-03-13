import threading
import tkinter as tk
from Controller import Controller
from tkinter.scrolledtext import ScrolledText


class GUI:

    def __init__(self):
        # GUI Thread
        self.thread = None
        # Controller
        self.outputs = {}
        self.controller = Controller(self.outputs)
        # self.controller = None
        # self.controller.start_threads()
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
        # Texts
        self.jet_text = ScrolledText(master=self.jet_frame, height=20, width=50)
        self.fan_text = ScrolledText(master=self.fan_frame, height=20, width=50)
        self.prop_text = ScrolledText(master=self.prop_frame, height=20, width=50)
        # Buttons
        self.jet_button = tk.Button(text="Switch", master=self.jet_frame, width=10)
        # self.prop_button = tk.Button(text="Turboprop", master=self.prop_frame, width=10)
        self.fan_button = tk.Button(text="Switch", master=self.fan_frame, width=10)
        self.exit_button = tk.Button(text="Exit", master=self.output_frame, width=10)

    def init_gui(self):
        # Jet Frame
        self.jet_label.pack()
        self.jet_button.pack()
        self.jet_button.bind("<Button-1>", self.jet_button_press)
        self.jet_text.pack(side=tk.LEFT)
        # Prop Frame
        self.prop_label.pack()
        self.prop_text.pack(side=tk.LEFT)
        # Fan Frame
        self.fan_label.pack()
        self.fan_button.pack()
        self.fan_button.bind("<Button-1>", self.fan_button_press)
        self.fan_text.pack(side=tk.LEFT)
        # Output Frame
        self.height_label.pack()
        self.pressure_label.pack()
        self.speed_label.pack()
        self.temperature_label.pack()
        self.fuel_label.pack()
        self.exit_button.pack()
        self.exit_button.bind("<Button-1>", self.exit_button_press)
        # Grid
        self.prop_frame.grid(row=0, column=0)
        self.fan_frame.grid(row=0, column=2)
        self.jet_frame.grid(row=0, column=1)
        self.output_frame.grid(row=0, column=3)
        # Start TK
        tk.mainloop()
        # Start GUI thread
        self.thread = threading.Thread(target=self.set_outputs, args=(self.outputs,))


    def jet_button_press(self, event):
        print("jet")
        Controller.jet_bool = True
        Controller.fan_bool = False
        pass


    def fan_button_press(self, event):
        print("fan")
        Controller.jet_bool = False
        Controller.fan_bool = True
        pass

    def exit_button_press(self, event):
        print("exit")
        Controller.jet_bool = False
        Controller.fan_bool = False
        pass

    def set_outputs(self, outputs):
        conditions = outputs['conditions']
        self.height_label['text'] = f"Height: {conditions['height']}"
        self.speed_label['text'] = f"Speed: {conditions['speed']}"
        self.temperature_label['temperature'] = f"Temperature: {conditions['temperature']}"
        self.pressure_label['pressure'] = f"Pressure: {conditions['pressure']}"
        self.jet_text.insert(tk.END, outputs['turbojet'])
        self.fan_text.insert(tk.END, outputs['turbofan'])
        self.prop_text.insert(tk.END, outputs['turboprop'])
