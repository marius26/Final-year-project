import json
import csv

def extract_parameters(frame_number, metadata):
    exposure_time = metadata["ExposureTime"]
    frame_duration = metadata["FrameDuration"]
    difference = frame_duration - exposure_time  # Calculate the difference
    return frame_number, exposure_time, frame_duration, difference

# Open the text file containing metadata
with open('metadata.txt', 'r') as file:
    metadata = json.load(file)

# Check if metadata is a list (multiple frames) or a single dictionary (single frame)
if isinstance(metadata, list):
    # Write parameters to CSV file
    with open('metadata.csv', 'w', newline='') as csvfile:
        fieldnames = ['FrameNumber', 'ExposureTime', 'FrameDuration', 'Difference']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Iterate through each frame metadata
        for idx, frame_metadata in enumerate(metadata):
            frame_number, exposure_time, frame_duration, difference = extract_parameters(idx + 1, frame_metadata)
            writer.writerow({'FrameNumber': frame_number, 'ExposureTime': exposure_time, 
                             'FrameDuration': frame_duration, 'Difference': difference})

else:
    # Extract parameters for a single frame
    frame_number = 1
    exposure_time, frame_duration, difference = extract_parameters(frame_number, metadata)

    # Write parameters to CSV file
    with open('metadata.csv', 'w', newline='') as csvfile:
        fieldnames = ['FrameNumber', 'ExposureTime', 'FrameDuration', 'Difference']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'FrameNumber': frame_number, 'ExposureTime': exposure_time, 
                         'FrameDuration': frame_duration, 'Difference': difference})

print("CSV file generated successfully.")