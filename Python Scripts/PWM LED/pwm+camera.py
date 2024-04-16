import subprocess
import threading
import os
import sys
import RPi.GPIO as GPIO
from time import sleep

# Script 1: libcamera-vid

def run_libcamera_command():
    #full resolution: 1456x1088
    command = [        "libcamera-vid",        "-n",        "--codec", "mjpeg",        "-t", "1000",        "--segment", "1",        "--width","1080",        "--height","640",
        "-o", "/home/pi/Desktop/Final-year-project/Python Scripts/PWM LED/Photos/1080x640-%03d.bmp",        "-v","1",        "--framerate", "60",        "--shutter","14000", #exposure time in microseconds
        #"--exposure","sport",        #"--gain", "0.5",        #"--metering","average",        #"--awb", "auto",   #"--saturation", "1.0",       #"--sharpness", "1.5",        #"--buffer-count","10",        #"--flush", "1",        #"--denoise", "cdn_off",
        "--info-text", "#%frame %fps(fps)  Exposure %exp",        "--save-pts", "timestampPerFrame.txt",        "--metadata", "metadata.txt"
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

    pi_pwm = GPIO.PWM(ledpin, 1000)  # create PWM instance with frequency (Hz)
    pi_pwm.start(0)  # start PWM of required Duty Cycle 
    while True:
        on_time_ms = 1 #store on time in ms for LED         
        pi_pwm.ChangeDutyCycle(100) #max brightness
        sleep(on_time_ms/1e3) #hold ON time
        pi_pwm.ChangeDutyCycle(0) # LED off
        sleep((1/60)-(on_time_ms/1e3)) #hold OFF time to maintain 60fps
        
        

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
