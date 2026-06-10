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
        robot.change_motor_mode("velocity")
        while not stop_requested:
            robot.print_motor_positions(raw=True)
            x = 0
            y = 0
            z = 0

            if keyboard.is_pressed('w'):
                y += 100
            if keyboard.is_pressed('s'):
                y -= 100
            if keyboard.is_pressed('a'):
                x -= 100
            if keyboard.is_pressed('q'):
                x += 100
            if keyboard.is_pressed('e'):
                z += 100
            if keyboard.is_pressed('d'):
                z -= 100

            robot.joystick_control(x, y, z)

            if keyboard.is_pressed('x'):
                print("Exiting...")
                break
           
    finally:
        print()
        print("Shutting down robot...")
        robot.shutdown()