from picamera2 import Picamera2, Preview
from libcamera import controls #import controls for the camera
import time

picam2 = Picamera2()
picam2.camera_properties



picam2.start_preview(Preview.QTGL)
picam2.title_fields = ["ExposureTime","fps"]
picam2.start()

metadata = picam2.capture_metadata()
print(metadata["ExposureTime"], metadata["AnalogueGain"])


picam2.set_controls({
        #"AfMode": controls.AfModeEnum.Continuous, No autofocus 
        "AwbEnable":0,
        "Contrast":1,
        "ExposureTime":10000,
        "FrameDurationLimits":(66666,66666),
        "NoiseReductionMode": controls.draft.NoiseReductionModeEnum.HighQuality, # Off Fast HighQuality
        #"ScalerCrop": (0,0,640,480) #used to crop the image recieved by the sensor -> show only that part usually used to pan and zoom
        "Saturation":1, #0.0 to 32, 1 is normal
         
    })


