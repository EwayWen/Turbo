import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn


class PeripheralHelper:

    def __init__(self):
        try:
            # MCP Initialization
            MCP_PIN_HEIGHT = MCP.P0
            MCP_PIN_FUEL = MCP.P1
            # # create the spi bus
            spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
            # # create the cs (chip select)
            cs = digitalio.DigitalInOut(board.D22)
            # # create the mcp object
            mcp = MCP.MCP3008(spi, cs)
            # # create an analog input channel on pin height/speed
            self.channel_height = AnalogIn(mcp, MCP_PIN_HEIGHT)
            self.channel_fuel = AnalogIn(mcp, MCP_PIN_FUEL)
        except Exception as e:
            print(f"MCP Exception occurred, closing: {e}")
            return
        try:
            # TODO PWM connection
            pass
        except Exception as e:
            print(f"PWM Exception occurred, closing: {e}")


    def get_height(self):
        # TODO: normalize
        # Input range from min to max
        # normalized_value = (input - min)/(max-min) * desired_range
        # normalized_value = (input - min)/(max-min) * 21
        # if (input >= max) input = max
        # if (input <= min) input = min
        return self.channel_height.value()

    def get_fuel(self):
        # TODO: normalize
        # Input range from min to max
        # normalized_value = (input - min)/(max-min) * desired_range
        # normalized_value = (input - min)/(max-min) * 21
        # if (input >= max) input = max
        # if (input <= min) input = min
        return self.channel_fuel.value()

    def write_PWM(self, PWM_out):
        # TODO: output
        pass
