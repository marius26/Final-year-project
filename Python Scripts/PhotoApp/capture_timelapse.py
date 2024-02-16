import time

from picamera2 import Picamera2

picam2 = Picamera2()
capture_config = picam2.create_still_configuration()
picam2.configure(picam2.create_preview_configuration())
picam2.start()


def capture_photos(num_photos):
         for i in range(10):
            picam2.start_and_capture_file(f'photo_{i}.jpg')
            print(f'Captured photo {i+1}/{num_photos}')
            time.sleep(0)  # No delay between captures

if __name__ == "__main__":
    #num_photos = int(input("Enter the number of photos to capture: "))
    capture_photos(10)
