from Robot import Robot
import signal
import keyboard

stop_requested = False

def handle_sigint(sig, frame):
    global stop_requested
    print("\nSIGINT received, stopping...")
    stop_requested = True

if __name__ == "__main__":
    robot = Robot()

    signal.signal(signal.SIGINT, handle_sigint)

    try:
        height = 75
        roll = 0
        pitch = 0
        while not stop_requested:
            robot.print_actuator_lengths()

            if keyboard.is_pressed('1'):
                height = 50
                roll = 0
                pitch = 0
            if keyboard.is_pressed('2'):
                height = 75
                pitch = 10
                roll = 0
            if keyboard.is_pressed('3'):
                height = 100
                roll = 10
                pitch = 0
            if keyboard.is_pressed('4'):
                height = 125.
                roll = 0
                pitch = 0
            if keyboard.is_pressed('5'):
                height = 100
                roll = -10
                pitch = 0

            robot.set_tcp(roll, pitch, height, speed=500)

            if keyboard.is_pressed('x'):
                print("Exiting...")
                break
           
    finally:
        print()
        print("Shutting down robot...")
        robot.shutdown()