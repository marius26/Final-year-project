from picamera2 import Picamera2
import time

picam2 = Picamera2()
picam2.start(show_preview=True)

picam2.set_controls({"ExposureTime":10000})

#JPEG quality level, where 0 is the worst quality and 95 is best. (default = 90)
#compress_level 1 PNG compression level, where 0 gives no compression, 1 is the fastest that actually does any compression, and 9 is the slowest.

#quality is for jpeg/jpg  95 gives a photo of about 256kb (fast)
picam2.options["quality"] = 95
#compress level is for png - 9 gives 1.3Mb (reaaaaly slow)
picam2.options["compress_level"] = 1

#a second delay, just before photos (to stabilize the camera)
#time.sleep(1)

# configure the camera, this is used if you want to switch the mode. create_still_configuration is for photos ; i don't think anything like this will be needed
#capture_config = picam2.create_still_configuration()


time.sleep(1)

#start_and_capture_file("filename") is used to capture a single photo
#check page 44 (6.6.1 of picamera2 library
picam2.start_and_capture_file("StartAndCapture.jpg")# a single photo
picam2.start_and_capture_files("StartAndCaptureFiles{:d}.jpg",initial_delay=2,delay=0, num_files=10) #10 photos at 0s delay each with a 2 s initial delay
#picam2.start_and_capture_files("StartAndCaptureFiles{:d}.png",initial_delay=0,delay=0, num_files=10)


# timestampe watermark


