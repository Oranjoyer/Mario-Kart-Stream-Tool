import cv2
import numpy as np


# Execute Edge Detection Algorithm on OpenCV image and return result
def grayscale(frame):
    if(len(frame.shape)>2):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return frame
def edgeDetect(frame):
    passF = frame - cv2.GaussianBlur(frame,(21,21),3)+127
    if(len(passF.shape)>2):
        passF = grayscale(passF)
    passF = cv2.Laplacian(passF, -1)
    return passF
def colorPass(frame):
    passF = frame
    passF = passF - cv2.GaussianBlur(passF,(21,21),3)+127
    passF = cv2.Laplacian(passF, -1)

    return passF

# # Get Average Frame but Edge Detection (Edge Detect Every Image)
# def getAverageFrame(frameList):
#     # averageFrame = np.zeros((720,1280), np.uint8)
#     # global DEBUG
#     if len(frameList) < 1:
#         return np.zeros((720,1280), np.uint8)
#     averageFrame = edgeDetect(frameList[0])
#     for i in range(len(frameList)-1):
#         averageFrame = cv2.addWeighted(averageFrame, 1-getWeight(i), edgeDetect(frameList[i+1]), getWeight(i),0.0)
#     return cv2.normalize(averageFrame, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

# Get Average Frame but Edge Detection (Edge Detect Only final Stacked Image)
def getAverageFrame(frameList):
    # averageFrame = np.zeros((720,1280), np.uint8)
    # global DEBUG
    if len(frameList) < 1:
        return np.zeros((720,1280), np.uint8)
    averageFrame = grayscale(frameList[0])
    for i in range(len(frameList)-1):
        averageFrame = cv2.addWeighted(averageFrame, 1-getWeight(i), grayscale(frameList[i+1]), getWeight(i),0.0)
    return edgeDetect(cv2.normalize(averageFrame, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U))

# Function to get the weight of a new element added to an average
def getWeight(iterations):
    base = 1/(iterations+2)
    return base


# Average Frames but Keep full color
def getAverageFrameColor(frameList):
    if len(frameList) < 1:
        return np.zeros((720,1280), np.uint8)
    averageFrame = frameList[0]
    for i in range(len(frameList)-1):
        averageFrame = cv2.addWeighted(averageFrame, 1-getWeight(i), frameList[i+1], getWeight(i),0.0)
            # cv2.destroyWindow("Debug")
    return cv2.normalize(averageFrame, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    # return averageFrame

