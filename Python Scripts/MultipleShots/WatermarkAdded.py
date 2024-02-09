from picamera2 import Picamera2
from PIL import Image, ImageDraw, ImageFont
import time

# Create a Picamera2 instance
picam2 = Picamera2()
picam2.start(show_preview=True)
config["main"]
{'format':'XBGR8888','size':(808,606)}
picam2.align_configuration(config)

# Set exposure time
picam2.set_controls({"ExposureTime": 10000})

# Set image quality and compression level
picam2.options["quality"] = 90
picam2.options["compress_level"] = 2

# Wait for the camera to stabilize
time.sleep(1)

# Capture multiple photos with timestamp
num_files = 10  # 10 photos
initial_delay = 0  # 2 seconds
delay = 0 # 5 seconds between photos

# Start the for loop for the num_files (number of photos)
prev_timestamp_ns = time.time_ns()

for i in range(num_files):
    # introduce initial delay before capturing the first photo (this is more for "stabilization")
    if i == 0:  # this being the first run
        time.sleep(initial_delay)  # "sleep" for initial_delay seconds

    # Capture a single photo with timestamp watermark
    timestamped_filename = f"Photo{i:02d}.jpg"  # Simply name the file
    timestamp_ns = time.time_ns()
    picam2.start_and_capture_file(timestamped_filename)  # call this function to take a single photo

    # Open captured image using Pillow - adding timestamp to the photo
    image = Image.open(timestamped_filename)
    draw = ImageDraw.Draw(image)

    # Add timestamp watermark with nanoseconds
    font_size = 30
    font_path = "/usr/share/fonts/truetype/freefont/FreeMono.ttf"
    font = ImageFont.truetype(font_path, font_size)  # font size 36

    formatted_timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp_ns // 1e9))
    # Add watermark at the bottom right corner of the photo
    draw.text((image.width - 800, image.height - 800), formatted_timestamp, (255, 255, 255), font=font)

    # Calculate time elapsed since the previous photo
    time_elapsed = (timestamp_ns - prev_timestamp_ns) / 1e9  # convert to seconds
    prev_timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(prev_timestamp_ns // 1e9))
    time_elapsed_str = f"From previous photo {time_elapsed:.4f} seconds"

    # Add it underneath timestamp
    draw.text((image.width - 800, image.height - 750), time_elapsed_str, (255, 255, 255), font=font)

    # Save the image
    image.save(timestamped_filename)  # Save the file with the name

    # Add the delay between the photos
    time.sleep(delay)

    # Update the previous timestamp for the next iteration
    prev_timestamp_ns = timestamp_ns
    sum = timestamp_ns + prev_timestamp_ns

# Close the Picamera instance
picam2.close()
print((sum/num_files)/1e-9)