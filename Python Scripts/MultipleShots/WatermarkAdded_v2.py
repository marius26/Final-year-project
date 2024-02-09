import time
from picamera2 import Picamera2
from datetime import datetime

picam2 = Picamera2()
picam2.start()

def capture_photos(num_photos, delay):
    with picam2 as camera:
        for i in range(num_photos):
            # Generate a filename with current time (including seconds and milliseconds)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = f"photo_{timestamp}.jpg"

            # Capture and save the photo
            picam2.start_and_capture_file(filename)# a single photo

            # Print feedback to the user
            print(f"Photo {i + 1}/{num_photos} taken: {filename}")

            # Wait for the specified delay before capturing the next photo
            time.sleep(delay)

if __name__ == "__main__":
    try:
        # Get user input for the number of photos and delay
        num_photos = int(input("Enter the number of photos to capture: "))
        delay = float(input("Enter the delay between photos (in seconds): "))

        # Capture photos
        capture_photos(num_photos, delay)

    except ValueError as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nCapture interrupted by user.")
    finally:
        print("Exiting the program.")
