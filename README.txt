README

Usage instructions
1. Open terminal
2. Navigate to “Documents/Turbo/”
2.1 The command to change directory is “cd”, e.g. “cd Documents/Turbo/” or “cd Documents/”
3. Type “python main.py” and hit enter

Class Summary

GUI.py
- uses a default python library to implement a simple GUI for the user.

Controller.py
- Starts the Turbo threads

PeripheralHelper.py
- Handles digital input from the ADC (MCP)
- Handles PWM to the motor drivers (L298)

Turbofan/prop/jet.py
- Performs calculations for display on the GUI

main.py
- Starts the program

Constants.py
- Contains constants used by the program

Class Details

GUI.py
The GUI class uses the default python library tkinter to generate a GUI. In addition to the tkinter mainloop, an additional thread (self.thread) is started to update GUI elements with data from the Turbo threads (set_outputs). The data from the Turbo threads is stored in dictionaries (self.jet_output, self.prop_output, self.fan_output, self.conditions). Buttons in the GUI enable, switch, or disable the turbofan or turbojet.

Controller.py
The Controller class is used to start or stop the Turbo threads. Output dictionaries are passed to the Controller class from the GUI class. These dictionaries are then passed to the start_turbo function threads. In the Turbo threads, input to the Turbo classes is obtained via a PeripheralHelper object. Output to GPIO is also done via a PeripheralHelper object. The output is controlled by Controller class booleans, which are set by the buttons in the GUI class.

PeripheralHelper.py

The PeripheralHelper class initializes controls digital input from the ADC (MCP) and PWM output from the Raspberry Pi's GPIO pins to the motor driver (L298). The PeripheralHelper class uses Adafruit’s circuitpython blinka suite of libraries in addition to Ben Croston’s RPi.GPIO library. PeripheralHelper’s get_height and get_fuel functions perform a linearization and normalization of the potentiometer’s output.

Normalization

Since the input from the potentiometer is logarithmic, we must perform a linearization on the input: 
input = ln(x)
⇒ e**(input) = x

Since we do not want to raise e to the power of 65k, we first perform a normalization on the input:
	input / 65k = normalized_1

Normalized_1 is guaranteed to be in [0, 1] since the maximum value of the input is 65k. We proceed with the linearization:
	e**(normalized_1) = x

e**(normalized_1) is guaranteed in the range of [1, e].

Since we want the input to be in the range of [0, 40], we perform a second normalization:
	(e**(normalized_1) - 1) / (e - 1)

Note: Shift e**(normalized_1) to 0 by doing (e**(normalized_1) - 1) and divide by the range of values (e - 1). The value is guaranteed to be in the range [0, 1]. 

Scale to [0, 40]:
	(e**(normalized_1) - 1) / (e - 1) * 40 = normalized_2

We can save a step by realizing that (e**(normalized_1) - 1) is in the range of [1, e]. If we instead raise 41 to normalized_1, we obtain a value in the range of [1, 41]. Shift to the range of [0, 40] by doing (41**(normalized_1) - 1):
	41**(input/65k) - 1

Turbofan/prop/jet.py

The turbo classes perform the calculations for the simulated inputs. The results of the calculations are written to each class’ output dictionary (see: Controller.py, GUI.py). Constants used by the Turbo classes are obtained from Constants.py or hardcoded in the simulation code. 

main.py

The main class is used to start the program. If main.py is directly run, it will instantiate a GUI class object. Otherwise, nothing will happen.

Constants.py

Constants.py is a static variable class that holds four lists of 41 values each. For a given input height in [0, 40], the corresponding value in each list is used as input to the Turbo classes.
