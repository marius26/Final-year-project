from picamera2 import Picamera2, Preview
import sys,os,glob, subprocess, time, keyboard
  

    
    
def run_libcamera_command():
    command = [
        "libcamera-vid",
        "-n",
        "--codec", "mjpeg",
        "-t", "1000",
        "--segment", "1",
        "-o", "/home/pi/Final-year-project/Python Scripts/PhotoApp/Test/NoForceRes-SensorSet_1456x1088-%03d.jpg",
        #"--width", "640",
        #"--height", "480",
        "--brightness", "0.0",
        "--contrast", "0.7",
        #"--exposure", "sport",
        "--shutter","16566",
        "--framerate", "60",
        "--gain", "0",
        "--awb", "auto",
        "--metering", "centre",
        "--saturation", "1.0",
        "--sharpness", "1.5",
        "--flush","1",
        "--denoise", "cdn_off",
        "--info-text", "#%frame %fps(fps)  Exposure %exp",
        "--save-pts","timestampPerFrame.txt",
        "--metadata", "metadata.txt"
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print("Error running libcamera-vid command:", e)
    except FileNotFoundError:
        print("libcamera-vid command not found. Make sure it is installed and accessible in your system.")



    
if __name__ == "__main__":
     run_libcamera_command()
     #     preBuffered_libcamera_command()