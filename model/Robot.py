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

    def print_actuator_lengths(self):
        length1 = self.motor_1.get_actuator_length()
        length2 = self.motor_2.get_actuator_length()
        length3 = self.motor_3.get_actuator_length()
        print(f"\rMotor_1: {length1:<6} | Motor_2: {length2:<6} | Motor_3: {length3:<6}", end="", flush=True)

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

    def set_tcp(self, roll, pitch, height, speed=100):
        roll = np.deg2rad(roll)
        pitch = np.deg2rad(pitch)
        height = height - 12.5 # compensate for the distance of the anchor point to the plates

        scale = 0.75
        base_size = 100/np.cos(np.deg2rad(30))

        # Base plate coordinates (homogeneous)
        P = np.array([
            [0,  np.sqrt(3)/2, -np.sqrt(3)/2],
            [1, -0.5,          -0.5],
            [0,  0,             0],
            [1,  1,             1]
        ], dtype=float)

        T_base_size = np.array([
            [base_size, 0,         0,        0],
            [0,         base_size, 0,        0],
            [0,         0,         base_size, 0],
            [0,         0,         0,        1]
        ], dtype=float)

        P = T_base_size @ P

        # Rotation matrices
        T_roll = np.array([
            [np.cos(roll), 0, np.sin(roll), 0],
            [0,            1, 0,            0],
            [-np.sin(roll),0, np.cos(roll), 0],
            [0,            0, 0,            1]
        ], dtype=float)

        T_pitch = np.array([
            [1, 0,            0,             0],
            [0, np.cos(pitch), -np.sin(pitch), 0],
            [0, np.sin(pitch),  np.cos(pitch), 0],
            [0, 0,            0,             1]
        ], dtype=float)

        T_height = np.array([
            [scale, 0,     0,     0],
            [0,     scale, 0,     0],
            [0,     0,     scale, height],
            [0,     0,     0,     1]
        ], dtype=float)

        P_rot = T_height @ T_pitch @ T_roll @ P

        # Alignment angle
        phi = np.arctan2(-np.sin(pitch) * np.sin(roll),
                        np.cos(pitch) + np.cos(roll))

        # Shift and rotate in XY plane
        P_xy = np.vstack([
            P_rot[0, :],
            P_rot[1, :] - P_rot[1, 0]
        ])

        R = np.array([
            [np.cos(phi), -np.sin(phi)],
            [np.sin(phi),  np.cos(phi)]
        ])

        P_xy_rot = R @ P_xy

        # Re-center left/right plane
        y_off = P_xy_rot[1, 1] + P_xy_rot[0, 1] / np.sqrt(3)
        final_position = P_xy_rot - np.array([[0], [y_off]])

        # Add Z back
        P_result = np.vstack([
            final_position,
            P_rot[2, :]
        ])

        # Leg lengths (front, right, left)
        base_xyz = P[0:3, :]

        length_front = np.linalg.norm(P_result[:, 0] - base_xyz[:, 0])
        length_right = np.linalg.norm(P_result[:, 1] - base_xyz[:, 1])
        length_left  = np.linalg.norm(P_result[:, 2] - base_xyz[:, 2])

        angle_front = self.motor_1.get_theoretical_angle(length_front)
        angle_right = self.motor_2.get_theoretical_angle(length_right)
        angle_left  = self.motor_3.get_theoretical_angle(length_left)

        diff_front = angle_front - self.motor_1.get_position()
        diff_right = angle_right - self.motor_2.get_position()
        diff_left  = angle_left  - self.motor_3.get_position()

        diffs = np.array([diff_front, diff_right, diff_left], dtype=float)

        max_diff = np.max(np.abs(diffs))

        # avoid division by zero
        if max_diff < 1e-9:
            return

        # base speed (your chosen max speed)
        base_speed = speed

        speed_front = base_speed * (abs(diff_front) / max_diff)
        speed_right = base_speed * (abs(diff_right) / max_diff)
        speed_left  = base_speed * (abs(diff_left)  / max_diff)

        self.motor_1.set_actuator_length(length_front, speed_front)
        self.motor_2.set_actuator_length(length_right, speed_right)
        self.motor_3.set_actuator_length(length_left, speed_left)

        return length_front, length_right, length_left
