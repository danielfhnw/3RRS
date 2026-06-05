from Motor import Motor
import sys
import os
import numpy as np
from dotenv import load_dotenv
current_dir = os.path.dirname(os.path.abspath(__file__))  # oop/
parent_dir = os.path.abspath(os.path.join(current_dir, "..")) 
sys.path.append(parent_dir)
from STservo_sdk import *    

class Robot:
    def __init__(self):
        load_dotenv()
        self.port_handler = PortHandler(os.getenv("COM_PORT_MOTOR"))
        self.packet_handler = sts(self.port_handler)
        
        # open port
        if self.port_handler.openPort():
            print("Succeeded to open the port")
        else:
            print("Failed to open the port")
            quit()

        # set baudrate
        if self.port_handler.setBaudRate(1000000):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate")
            quit()

        offset_servo1 = os.getenv("OFFSET_SERVO_1")
        self.motor_1 = Motor(1, int(offset_servo1) if offset_servo1 else 0, self.packet_handler)
        offset_servo2 = os.getenv("OFFSET_SERVO_2")
        self.motor_2 = Motor(2, int(offset_servo2) if offset_servo2 else 0, self.packet_handler)
        offset_servo3 = os.getenv("OFFSET_SERVO_3")
        self.motor_3 = Motor(3, int(offset_servo3) if offset_servo3 else 0, self.packet_handler)

        self.path = []

    def shutdown(self):
        self.motor_1.shutdown()
        self.motor_2.shutdown()
        self.motor_3.shutdown()
        self.port_handler.closePort()
        print("Robot shutdown")
  
    def get_motor_positions(self, raw=False):
        if raw:
            pos1 = self.motor_1.get_position_raw()
            pos2 = self.motor_2.get_position_raw()
            pos3 = self.motor_3.get_position_raw()
        else:
            pos1 = self.motor_1.get_position()
            pos2 = self.motor_2.get_position()
            pos3 = self.motor_3.get_position()
        return pos1, pos2, pos3

    def print_motor_positions(self, raw=False):
        pos1, pos2, pos3 = self.get_motor_positions(raw)
        print(f"\rMotor_1: {pos1:<6} | Motor_2: {pos2:<6} | Motor_3: {pos3:<6}", end="", flush=True)

    def change_motor_mode(self, mode):
        self.motor_1.change_mode(mode)
        self.motor_2.change_mode(mode)
        self.motor_3.change_mode(mode)

    def joystick_control(self, joystick_x, joystick_y, joystick_z):
        self.motor_1.set_speed(joystick_y * 10)
        self.motor_2.set_speed(joystick_x * 10)
        self.motor_3.set_speed(joystick_z * 10)

    def set_motor_positions(self, pos1, pos2, pos3, speed=100):
        self.motor_1.set_position(pos1, speed)
        self.motor_2.set_position(pos2, speed)
        self.motor_3.set_position(pos3, speed)