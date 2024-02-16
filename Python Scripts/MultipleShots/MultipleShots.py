from picamera2 import Picamera2, Preview
from libcamera import controls #import controls for the camera
from picamera2.controls import Controls
import time

picam2 = Picamera2()

picam2.start_preview(Preview.QTGL)
picam2.title_fields = ["ExposureTime","fps"]

preview_config = picam2.create_preview_configuration()
picam2.configure(preview_config)


picam2.preview_configuration.size = (1090, 1080)
picam2.preview_configuration.format = "XBGR8888"
picam2.still_configuration.size = (1600, 1200)
picam2.still_configuration.size = (1600, 1200)

with picam2.controls as ctrl:
    ctrl.AnalogueGain = 6.0
    ctrl.ExposureTime = 60000

ctrls = Controls(picam2)
ctrls.AnalogueGain = 1.0
ctrls.ExposureTime = 10000
picam2.set_controls(ctrls)
#picam2.set_controls({"ExposureTime":10000, "FrameRate":60})#keep it 10k

#JPEG quality level, where 0 is the worst quality and 95 is best. (default = 90)
#compress_level 1 PNG compression level, where 0 gives no compression, 1 is the fastest that actually does any compression, and 9 is the slowest.

#quality is for jpeg/jpg  95 gives a photo of about 256kb (fast)
picam2.options["quality"] = 20
#compress level is for png - 9 gives 1.3Mb (reaaaaly slow)
picam2.options["compress_level"] = 1

#a second delay, just before photos (to stabilize the camera)
#time.sleep(1)

# configure the camera, this is used if you want to switch the mode. create_still_configuration is for photos ; i don't think anything like this will be needed
#capture_config = picam2.create_still_configuration()


time.sleep(1)

#start_and_capture_file("filename") is used to capture a single photo
#check page 44 (6.6.1 of picamera2 library
#picam2.start_and_capture_file("StartAndCapture.jpg")# a single photo
picam2.start_and_capture_files("{:d}.jpg",initial_delay=5,delay=0, num_files=10) #10 photos at 0s delay each with a 2 s initial delay
#picam2.start_and_capture_files("StartAndCaptureFiles{:d}.png",initial_delay=0,delay=0, num_files=10)


# timestampe watermark


