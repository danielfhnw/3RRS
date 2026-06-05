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
        height = 50
        while not stop_requested:
            robot.print_actuator_lengths()

            if keyboard.is_pressed('1'):
                height = 50
            if keyboard.is_pressed('2'):
                height = 75
            if keyboard.is_pressed('3'):
                height = 100
            if keyboard.is_pressed('4'):
                height = 125

            robot.set_tcp(0, 0, height, speed=100)

            if keyboard.is_pressed('x'):
                print("Exiting...")
                break
           
    finally:
        print()
        print("Shutting down robot...")
        robot.shutdown()