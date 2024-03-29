import subprocess
import threading
import os
import sys
import RPi.GPIO as GPIO
from time import sleep

# Script 1: libcamera-vid

def run_libcamera_command():
    #full resolution: 1456x1088
    command = [
        "libcamera-vid",
        "-n",
        "--codec", "mjpeg",
        "-t", "1000",
        "--segment", "1",
        "--width","640",
        "--height","480",
        "-o", "/home/pi/Desktop/Final-year-project/Python Scripts/PWM LED/Photos/640x480-%03d.jpg",
        #"--brightness", "0.1",
        #"--contrast", "0.5",
        "--framerate", "60",
        "--shutter","14000",
        #"--exposure","sport",
        #"--gain", "0.5",
        #"--awb", "fluorescent",
        #"--metering", "centre",
        #"--saturation", "1.0",
        #"--sharpness", "1.5",
        "--flush", "1",
        "--denoise", "cdn_off",
        "--info-text", "#%frame %fps(fps)  Exposure %exp",
        "--save-pts", "timestampPerFrame.txt",
        "--metadata", "metadata.txt"
    ]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print("Error running libcamera-vid command:", e)
    except FileNotFoundError:
        print("libcamera-vid command not found. Make sure it is installed and accessible in your system.")

# Script 2: LED PWM

def run_pwm():
    ledpin = 35  # PWM pin connected to LED
    GPIO.setmode(GPIO.BOARD)  # set pin numbering system
    GPIO.setup(ledpin, GPIO.OUT)

    pi_pwm = GPIO.PWM(ledpin, 5000)  # create PWM instance with frequency
    pi_pwm.start(0)  # start PWM of required Duty Cycle 

    while True:
        on_time_ms = 1
        
        pi_pwm.ChangeDutyCycle(100)
        sleep(on_time_ms/1e3)
        pi_pwm.ChangeDutyCycle(0)
        sleep((1/30)-(on_time_ms/1e3))
        
        

if __name__ == "__main__":
    # Initialize GPIO
    GPIO.setwarnings(False)  # disable warnings
    #GPIO.setmode(GPIO.BOARD)  # set pin numbering system

    # Create threads for each script and start them
    libcamera_thread = threading.Thread(target=run_libcamera_command)
    pwm_thread = threading.Thread(target=run_pwm)
    
    pwm_thread.start()
    libcamera_thread.start()
    

    # Wait for both threads to finish
    pwm_thread.join()
    libcamera_thread.join()
    

    # Cleanup GPIO
    GPIO.cleanup()
