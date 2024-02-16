import cv2
from picamera2 import Picamera2

piCam = Picamera2()

#piCam.preview_configuration.main.size = (640, 360)

piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()

frame_count = 0  # Counter for frame numbering
piCam.exposure_mode = 'auto'
# Set camera parameters
piCam.resolution = (480, 360)
piCam.brightness = 3.5
piCam.contrast = 0.7
# piCam.exposure_mode = "sport"  # Commented out as this parameter is not directly supported in Picamera2
piCam.shutter_speed = 100
piCam.framerate = 60
piCam.awb_mode = "auto"
piCam.meter_mode = "centre"
piCam.saturation = 1.0
piCam.sharpness = 1.5
piCam.flush = 1

while frame_count<60:
    frame = piCam.capture_array()
    filename = "Photo_%04d.jpg" % frame_count  # Create unique filename
    cv2.imwrite(filename, frame)  # Save frame with unique filename
    frame_count += 1  # Increment frame counter
    # cv2.imshow("piCam", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
