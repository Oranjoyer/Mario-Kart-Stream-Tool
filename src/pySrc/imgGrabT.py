from fileService import loadFilesFromQueries
from frameAverage import getAverageFrameColor
import cv2
quer = ["Race","Online","12P","1st","Rankings"]
def test():
    cv2.imshow("test",getAverageFrameColor([f.fileData for f in loadFilesFromQueries("TemplateData/MK8DX/",quer)]))
    cv2.waitKey(0)
test()