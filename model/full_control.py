from Robot import Robot
import signal
import keyboard
import time

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

            if keyboard.is_pressed('w'):
                pitch += 1
            if keyboard.is_pressed('s'):
                pitch -= 1 
            if keyboard.is_pressed('a'):
                roll -= 1
            if keyboard.is_pressed('d'):                
                roll += 1
            if keyboard.is_pressed('q'):
                height += 1
            if keyboard.is_pressed('e'):
                height -= 1

            robot.set_tcp(roll, pitch, height, speed=500)
            print(f" | Height: {height:.1f} mm, Roll: {roll:.1f} deg, Pitch: {pitch:.1f} deg", end='\r')

            if keyboard.is_pressed('x'):
                print("Exiting...")
                break

            time.sleep(0.05)
           
    finally:
        print()
        print("Shutting down robot...")
        robot.shutdown()