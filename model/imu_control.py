from Robot import Robot
from IMU import IMU
import signal
import keyboard


stop_requested = False
roll = 0.0
pitch = 0.0
roll_offset = 0.0
pitch_offset = 0.0
height = 75


def handle_sigint(sig, frame):
    global stop_requested
    print("\nSIGINT received, stopping...")
    stop_requested = True


if __name__ == "__main__":
    robot = Robot()
    imu = IMU()


    signal.signal(signal.SIGINT, handle_sigint)

    try:
        while not stop_requested:

            robot.print_actuator_lengths()

            if keyboard.is_pressed('w'):
                pitch_offset += 0.1
            if keyboard.is_pressed('s'):
                pitch_offset -= 0.1
            if keyboard.is_pressed('a'):
                roll_offset -= 0.1
            if keyboard.is_pressed('d'):                
                roll_offset += 0.1
            if keyboard.is_pressed('q'):
                height += 0.1
            if keyboard.is_pressed('e'):
                height -= 0.1
            if keyboard.is_pressed('x'):
                print("Exiting...")
                break


            pitch_imu, roll_imu = imu.get_position()

            if not pitch_imu or not roll_imu:
                continue

            pitch = -pitch_imu + pitch_offset
            roll = -roll_imu + roll_offset

            height = max(40, min(150, height))
            pitch = max(-20, min(20, pitch))
            roll = max(-20, min(20, roll))

            robot.set_tcp(roll, pitch, height, speed=2000)

            print(
                f" | Height: {height:.1f} mm "
                f"| Roll: {roll:.2f} deg "
                f"| Pitch: {pitch:.2f} deg",
                end="\r"
            )

    finally:
        print()
        print("Shutting down robot...")
        stop_requested = True
        robot.shutdown()
        imu.shutdown()