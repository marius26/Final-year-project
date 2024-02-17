#! /usr/bin/env python3
import time
import os
import subprocess
import signal
import datetime
import glob
import sys
import shutil
import keyboard  # Import the keyboard module
import os
import sys



# Constants and variables
width = 640  # frame width 
height = 480   # frame height
framerate = 60    # fps
pre_frames = 10    # Number of PRE Frames
cap_length = 1000  # in mS
ram_limit = 150   # in MB, stops if RAM below this

# setup directories
#pic_dir = "/home/{}/Pictures/".format(os.getlogin())

pic_dir = "/home/pi/Desktop/Final-year-project/Python Scripts/PhotoApp".format(os.getlogin())
# clear ram
print("Clearing RAM...")
frames = glob.glob('/run/shm/*.jpg')
for frame in frames:
    os.remove(frame)

# start camera with subprocess
print("Starting Camera...")
command = "libcamera-vid -n -t 0 --codec mjpeg --segment 1 --framerate {} -o /run/shm/temp_%06d.jpg --width {} --height {}".format(
    framerate, width, height)
s = subprocess.Popen(command, shell=True, preexec_fn=os.setsid) #line of code to run the command in subprocess using poppen class
#creates a subprocess object and atributes it to s
s.poll() #checks if the subrocess is finished
while s.poll() is not None:
    print("waiting...")
    time.sleep(1)

print("Capturing Pre-Frames...")
while len(glob.glob('/run/shm/temp*.jpg')) < pre_frames:
    time.sleep(1)
print("Pre-Frames captured...")
print("Ready for Trigger.....")

# Main loop
while True:
    # Check for trigger key press
    print("Press 't' to trigger camera...")
    keyboard.wait('t')
    print("Triggered...")
    
    # Your camera capture logic goes here
    now = datetime.datetime.now()
    timestamp = now.strftime("%y%m%d_%H%M%S_%f")
    
    # Your capture duration logic goes here
    # Stop camera subprocess
    os.killpg(s.pid, signal.SIGTERM)

    # Get date parameters
    yr, mh, dy = timestamp[:2], timestamp[2:4], timestamp[4:6]
    hr, mn, sc, ms = map(int, [timestamp[7:9], timestamp[9:11], timestamp[11:13], timestamp[14:21]])
    dz = timestamp[:6]

    # Get frames list
    frames = glob.glob('/run/shm/temp*.jpg')
    frames.reverse()
    
    # Calculate times for file name
    for x in range(len(frames)):
        mc = ms + ((x - pre_frames) * int(1000000/framerate))
        sc2, mn2, hr2 = sc, mn, hr
        while mc > 999999:
            sc2 += 1
            mc -= 1000000
            if sc2 > 59:
                sc2 = 0
                mn2 += 1
                if mn2 > 59:
                    hr2 += 1
                    mn2 = 0
                    if hr2 > 23:
                        hr2 = 0
        while mc < 0:
            sc2 -= 1
            mc += 1000000
            if sc2 < 0:
                sc2 = 59
                mn2 -= 1
                if mn2 < 0:
                    hr2 -= 1
                    mn2 = 59
                    if hr2 < 0:
                        hr2 = 23
        md = "00000" + str(mc)
        mo = str(mn2).zfill(2)
        sd = str(sc2).zfill(2)
        hs = str(hr2).zfill(2)
        timestamp = hs + mo + sd + "_" + str(md)[-6:]
        if x == pre_frames:
            trig = timestamp
        # Rename file to HHMMSS-mmmmmm.jpg
        if os.path.exists(frames[x]):
            os.rename(frames[x], frames[x][0:9] + timestamp + '.jpg')

    # Clear ram of temp files
    print("Clearing temp files from RAM...")
    for frame in frames:
        os.remove(frame)
    
    # Move RAM Files to SD card
    print("Moving files to SD card (/Pictures/DATE)...")
    if not os.path.exists(pic_dir + dz):
        os.mkdir(pic_dir + dz)
    vframes = glob.glob('/run/shm/*.jpg')
    for frame in vframes:
        if not os.path.exists(pic_dir + frame[9:]) and frame[:4] != "temp":
            shutil.move(frame, pic_dir + dz)
