import subprocess
from picamera2 import Picamera2, Preview



def run_libcamera_command():
    command = [
        "libcamera-vid",
        "-n",
        "--codec", "mjpeg",
        "-t", "1000",
        "--segment", "2",
        "-o", "/home/pi/Final-year-project/Python Scripts/PhotoApp/Shutter-200_%03d.jpg",
        "--width", "640",
        "--height", "480",
        #"--brightness", "0.0",
        #"--contrast", "0.7",
       # "--exposure", "sport",
        "--shutter","200",
        "--framerate", "60",
       # "--gain", "0",
       # "--awb", "auto",
        #"--metering", "centre",
        #"--saturation", "1.0",
        #"--sharpness", "1.5",
        #"--denoise", "off",
        "--info-text", "#%frame (%fps fps) Exposure %exp"
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print("Error running libcamera-vid command:", e)
    except FileNotFoundError:
        print("libcamera-vid command not found. Make sure it is installed and accessible in your system.")



    
if __name__ == "__main__":
    run_libcamera_command()
