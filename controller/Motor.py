import numpy as np

class Motor:
    def __init__(self, id, offset, packet_handler):
        self.id = id
        self.offset = offset
        # initial offset based on position the model is in when the tool is as low as possible
        self.a = 50
        self.b = 78.868
        self.c = 40
        self.angle_offset = np.arccos((self.a*self.a + self.b*self.b - self.c*self.c) / (2*self.a*self.b))
        self.packet_handler = packet_handler
        self.mode = "position"

        self.packet_handler.ServoMode(self.id)
        self.packet_handler.change_hold(self.id, 0)
        self.packet_handler.set_max_angle(self.id, 0)
        self.packet_handler.set_min_angle(self.id, 0)
        self.packet_handler.set_multiturn(self.id)
        

    def shutdown(self):
        self.packet_handler.change_hold(self.id, 0)
        print(f"Motor {self.id} shutdown")

    def get_position_raw(self):
        position, _, _, _ = self.packet_handler.ReadPosSpeed(self.id)
        return position - self.offset
    
    def get_position(self):
        position_raw = self.get_position_raw()
        return position_raw * 2 * 3.141592653589793 / 4096 + self.angle_offset
    
    def get_actuator_length(self):
        angle = self.get_position()
        c = np.sqrt(self.a*self.a + self.b*self.b - 2*self.a*self.b*np.cos(angle))
        return c

    def get_speed(self):
        _, speed, _, _ = self.packet_handler.ReadPosSpeed(self.id)
        return speed
    
    def set_actuator_length(self, length, speed=100):
        if length < abs(self.a - self.b) or length > self.a + self.b:
            raise ValueError("Length is out of range for the given arm configuration.")
        angle = np.arccos((self.a*self.a + self.b*self.b - length*length) / (2*self.a*self.b))
        if angle < self.angle_offset or angle > (np.pi - 0.3):
            raise ValueError("Calculated angle is out of range. Check the input length.")
        self.set_position(angle, speed)

    def get_theoretical_angle(self, length):
        if length < abs(self.a - self.b) or length > self.a + self.b:
            raise ValueError("Length is out of range for the given arm configuration.")
        angle = np.arccos((self.a*self.a + self.b*self.b - length*length) / (2*self.a*self.b))
        return angle

    def set_position(self, position, speed=100):
        position_raw = int((position-self.angle_offset) * 4096 / (2 * 3.141592653589793) + self.offset)
        self.set_position_raw(position_raw, speed)

    def set_position_raw(self, position, speed=100):
        self.packet_handler.WritePosEx(self.id, position, int(speed), 0)

    def change_mode(self, mode):
        if mode == "position":
            self.packet_handler.ServoMode(self.id)
        elif mode == "velocity":
            self.packet_handler.WheelMode(self.id)
        else:
            raise ValueError("Invalid mode. Use 'position' or 'velocity'.")
        self.mode = mode

    def set_speed(self, speed):
        if self.mode != "velocity":
            raise ValueError("Motor is not in velocity mode. Call change_mode('velocity') first.")
        self.packet_handler.WriteSpec(self.id, int(speed), 0)