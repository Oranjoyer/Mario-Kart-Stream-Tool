import cv2
import json
import fileService
import frameAverage
import referenceMatching
import sys
TEMPLATE_LOC = "./TemplateData"
WRITE_DIR = "./ReferenceData"
def prepTemplateColors(infoJson):
    if(type(infoJson)==str):
        infoJson = json.loads(infoJson)
    if("TemplateInfo" not in infoJson):
        return None
    # print(infoJson)
    refDir = infoJson.get("GAME")
    referenceResolution = infoJson.get("RefRes")
    discrete = infoJson.get("Discrete")
    refList = []
    tolerance = infoJson.get("Tolerance")
    cropPoint = infoJson.get("CropPoint")
    for template in infoJson.get("Templates"):
        # print(template)
        print(template.get("Tolerance")!=None)
        if(template.get("Tolerance")!=None):
            tolerance = template.get("Tolerance")
        queried = [f.fileData for f in fileService.loadFilesFromQueries(f"{TEMPLATE_LOC}/{refDir}/",template.get("Query"))]
        templateImg = frameAverage.getAverageFrameColor(queried)
        if(cropPoint!=None):
            templateImg = templateImg[cropPoint[0][1]:cropPoint[1][1],cropPoint[0][0]:cropPoint[1][0]]
        pixelList = []
        for pixel in template.get("Points"):
            pixelList.append(referenceMatching.Pixel(templateImg[pixel[1]][pixel[0]][2],templateImg[pixel[1]][pixel[0]][1],templateImg[pixel[1]][pixel[0]][0],pixel[0],pixel[1]))
        refTemp = referenceMatching.Reference(template.get("Name"),pixelList,tolerance,referenceResolution)
        # print(template.get("Discrete"))
        if(template.get("Discrete")==False):
            refTemp.subRes=template.get("SubRes")
            refTemp.discrete = False
            refTemp.bounds = template.get("Bounds")
        refList.append(refTemp)

    writeDir = f"{WRITE_DIR}/{refDir}/"
    for reference in refList:
        name = reference.name
        # print(reference.exportAsDict())
        dumpedRef = json.dumps(reference.exportAsDict())
        with open(f"{writeDir}{name}.json","w") as f:
            f.write(dumpedRef)
            print(f"Wrote {name}")
        
filePaths = sys.argv[1:]
# filePath = "MK8DX/placeInfo.json"     
for filePath in filePaths:
    with open(filePath) as f:
        
        prepTemplateColors(f.read())

    
