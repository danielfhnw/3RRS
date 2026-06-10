import serial
import os
from dotenv import load_dotenv

class IMU:
    def __init__(self):
        load_dotenv()
        self.com_port_nano = os.getenv("COM_PORT_IMU")
        self.ser = serial.Serial(self.com_port_nano, 115200, timeout=1)   

    def shutdown(self):
        self.ser.close()
  
    def get_imu_raw(self):
        return self.ser.readline().decode("utf-8").strip()

    def get_position(self):
        line = self.ser.readline().decode("utf-8").strip()

        if not line:
            return None, None

        pitch_imu, roll_imu = line.split(",")
        pitch_imu = float(pitch_imu)
        roll_imu = float(roll_imu)

        return pitch_imu, roll_imu
