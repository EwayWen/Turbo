import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
import math
from adafruit_mcp3xxx.analog_in import AnalogIn
import pwmio
from adafruit_motor import servo
import RPi.GPIO as GPIO


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
        try:
            GPIO.setup(12, GPIO.OUT)
            self.not_prop = GPIO.PWM(12, 50)
            self.not_prop.start(0.0)
            GPIO.setup(20, GPIO.OUT)
            GPIO.output(20, GPIO.HIGH)
            GPIO.setup(26, GPIO.OUT)
            GPIO.output(26, GPIO.LOW)
            # TODO: fill in prop pins
            GPIO.setup(13, GPIO.OUT)
            self.prop = GPIO.PWM(13, 50)
            self.prop.start(0.0)
            GPIO.setup(5, GPIO.OUT)
            GPIO.output(5, GPIO.HIGH)
            GPIO.setup(6, GPIO.OUT)
            GPIO.output(6, GPIO.LOW)
#           self.pin_high_b 
#           self.pin_low_a 
        except Exception as e:
            print(f"PWM Exception occurred, closing: {e}")


    def get_height(self):
        raw_height = self.channel_height.value
        normalized = self.new_normalize(raw_height, 40)
        # if raw_height > 0:
        #     normalized = (raw_height)/64500 * 40
        # else:
        #     normalized = 0
        # if normalized > 40:
        #     normalized = 40
        # if normalized < 0:
        #     normalized = 0
        return int(normalized)

    def get_fuel(self):
        raw_fuel = self.channel_fuel.value
        normalized = self.new_normalize(raw_fuel, 0.26)
        # if raw_fuel > 0:
        #     normalized = (raw_fuel)/64500 * 0.26
        # else:
        #     normalized = 0
        # if normalized > 0.26:
        #     normalized = 0.26
        # if normalized < 0:
        #     normalized = 0
        return normalized

    def new_normalize(self, input, range):
        return (range+1)**(input/64500)-1

    def write_PWM(self, pwm_in):
        pwm_out = pwm_in/0.26 * 30
        print(f"pwm write: {pwm_out}")
        self.not_prop.ChangeDutyCycle(pwm_out)
        self.prop.ChangeDutyCycle(pwm_out)
