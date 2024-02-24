#!/usr/bin/env python3
import time
import os, subprocess
import signal
import datetime
import glob
import sys
from gpiozero import Button
import numpy as np
import shutil
import pygame
from pygame.locals import *

#v0.02

# setup
width      = 640  # frame width 
height     = 480   # frame height
framerate  = 60    # fps
pre_frames = 5   # Number of PRE Frames
cap_length = 1000  # in mS
ram_limit  = 150   # in MB, stops if RAM below this

# specify trigger button
trigger    = Button(21)

# setup directories
Home_Files  = []
Home_Files.append(os.getlogin())
pic_dir = "/home/" + Home_Files[0]+ "/Pictures/"

# screen setup
pygame.init()
width2 = 400
height2 = 200
windowSurfaceObj = pygame.display.set_mode((width2, height2), pygame.NOFRAME, 24)
capture = 0

def text(msg,row,color):
   global width2,height2
   fontObj = pygame.font.Font(None,30)
   msgSurfaceObj = fontObj.render(msg, False, color)
   msgRectobj = msgSurfaceObj.get_rect()
   pygame.draw.rect(windowSurfaceObj,(0,0,0),Rect(0,row*30,width2,30))
   msgRectobj.topleft = (0,row * 30)
   windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)
   pygame.display.update()

# clear ram
text("Clearing RAM...",0,(128,128,128))
frames = glob.glob('/run/shm/*.jpg')
for tt in range(0,len(frames)):
    os.remove(frames[tt])
   
# start camera with subprocess
text("Starting Camera...",1,(128,128,128))
command = "libcamera-vid -n -t 0 --codec mjpeg --segment 1 --framerate " + str(framerate) + " -o /run/shm/temp_%06d.jpg --width " + str(width) + " --height " + str(height)
s = subprocess.Popen(command, shell=True, preexec_fn=os.setsid)
poll = s.poll()
while poll != None:
    text("waiting...")
    poll = s.poll()

text("Capturing Pre-Frames...",2,(128,128,128))
while len(frames) < pre_frames:
    frames = glob.glob('/run/shm/temp*.jpg')
text("Pre-Frames captured...",3,(128,128,128))
text("Ready...Press t to capture, ESC to EXIT",4,(0,128,0))

# check ram
st = os.statvfs("/run/shm/")
freeram = (st.f_bavail * st.f_frsize)/1100000

stop = 0

# loop
while freeram > ram_limit:
    
    # check ram and stop if full
    st = os.statvfs("/run/shm/")
    freeram = (st.f_bavail * st.f_frsize)/1100000
        
    # read temp files
    frames = glob.glob('/run/shm/temp*.jpg')
    # DELETE old frames from buffer
    for tt in range(pre_frames,len(frames)-1):
        os.remove(frames[tt])
    
    # trigger capture
    if capture == 1:
        capture = 0
        now = datetime.datetime.now()
        timestamp = now.strftime("%y%m%d_%H%M%S_%f")
        w = len(frames)
        text("Triggered...",5,(128,128,128))
        text(timestamp,6,(128,128,128))
       
        # capture for cap_length
        start = time.monotonic()
        st = os.statvfs("/run/shm/")
        freeram = (st.f_bavail * st.f_frsize)/1100000
        while time.monotonic() - start < cap_length/1000 and freeram > ram_limit:
            st = os.statvfs("/run/shm/")
            freeram = (st.f_bavail * st.f_frsize)/1100000
        
        # stop camera subprocess
        print (s.pid)
        print(signal.SIGTERM)
        os.killpg(s.pid, signal.SIGTERM)
        
        # get date parameters 
        yr = timestamp[0:2]
        mh = timestamp[2:4]
        dy = timestamp[4:6]
        hr = int(timestamp[7:9])
        mn = int(timestamp[9:11])
        sc = int(timestamp[11:13])
        ms = int(timestamp[14:21])
        dz = timestamp[0:6]

        # get frames list
        frames = glob.glob('/run/shm/temp*.jpg')
        frames.reverse()
       
        # calculate times for file name
        for x in range(0,len(frames)):
            mc = ms + ((x - w) * int(1000000/framerate))
            sc2 = sc
            mn2 = mn
            hr2 = hr
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
            mo = str(mn2)
            if len(mo) < 2:
                mo = "0" + mo
            sd = str(sc2)
            if len(sd) < 2:
                sd = "0" + sd
            hs = str(hr2)
            if len(hs) < 2:
                hs = "0" + hs
            timestamp = hs + mo + sd + "_" + str(md)[-6:]
            if x == w:
                trig = timestamp
            # rename file to HHMMSS-mmmmmm.jpg
            if os.path.exists(frames[x]):
                os.rename(frames[x],frames[x][0:9] + timestamp + '.jpg')
               #os.rename(frames[x], pic_dir + "Photo_" + str(x+1) + '.jpg')


       
        # clear ram of temp files
        text("Clearing temp files from RAM...",0,(128,128,128))
        frames = glob.glob('/run/shm/temp*.jpg')
        for tt in range(0,len(frames)):
            os.remove(frames[tt])
        
        # move RAM Files to SD card
        text("Moving files to SD card (/Pictures/DATE)...",1,(128,128,128))
        if not os.path.exists(pic_dir + dz) :
            os.system('mkdir ' + pic_dir + dz)
        vframes = glob.glob('/run/shm/*.jpg')
        for xx in range(0,len(vframes)):
            if not os.path.exists(pic_dir + vframes[xx][9:]) and vframes[xx][0:4] != "temp":
                shutil.move(vframes[xx],pic_dir + dz)

        for d in range(1,7):
            text(" ",d,(0,0,0))
        # restart camera with subprocess
        text("Starting Camera...",1,(128,128,128))
        command = "libcamera-vid -n -t 0 --codec mjpeg --segment 1 --framerate " + str(framerate) + " -o /run/shm/temp_%06d.jpg --width " + str(width) + " --height " + str(height)
        s = subprocess.Popen(command, shell=True, preexec_fn=os.setsid)
        print(preexec_fn)
        poll = s.poll()
        while poll != None:
            text("waiting...")
            poll = s.poll()

        text("Capturing Pre-Frames...",2,(128,128,128))
        while len(frames) < pre_frames:
            frames = glob.glob('/run/shm/temp*.jpg')
        text("Pre-Frames captured...",3,(128,128,128))
        text("Ready...Press t to capture, ESC to EXIT",4,(0,128,0))

    # check for key presses
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            key = event.key
            if key == K_t:
                capture = 1
            if key == K_ESCAPE:
                # stop camera subprocess if running
                poll = s.poll()
                if poll == None:
                    os.killpg(s.pid, signal.SIGTERM)
                pygame.display.quit()
                pygame.quit()
                sys.exit
              
# stop if ram full
poll = s.poll()
if poll == None:
   os.killpg(s.pid, signal.SIGTERM)
pygame.display.quit()
pygame.quit()
sys.exit              