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
        a = 0.5
        while not stop_requested:
            robot.print_motor_positions(raw=False)

            if keyboard.is_pressed('1'):
                a = 0.5
            if keyboard.is_pressed('2'):
                a = 1.0
            if keyboard.is_pressed('3'):
                a = 1.5
            if keyboard.is_pressed('4'):
                a = 2.0
            if keyboard.is_pressed('5'):
                a = 2.5

            robot.set_motor_positions(a, a, a, speed=500)

            if keyboard.is_pressed('x'):
                print("Exiting...")
                break
           
    finally:
        print()
        print("Shutting down robot...")
        robot.shutdown()