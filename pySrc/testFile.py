import cv2
import subprocess
import numpy as np
import time

wid = 1920
height = 1080
framerate = 60

pipe = subprocess.Popen(["ffmpeg","-video_size",f"{wid}x{height}","-framerate",f"{framerate}","-i","/dev/video0","-vcodec","libx264","-f","mpegts","udp://localhost:21623","-vcodec","rawvideo","-an","-sn","-pix_fmt","bgr24","-f","image2pipe","-"],stdout=subprocess.PIPE,bufsize=10)

while True:
    start = time.time()
    raw = pipe.stdout.read(wid*height*3)
    image = np.frombuffer(raw,dtype='uint8')
    image = image.reshape((height,wid,3))
    print(1/(time.time()-start))
    cv2.imshow("vid",image)
    cv2.waitKey(1)
