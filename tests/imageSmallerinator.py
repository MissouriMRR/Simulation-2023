#This program has nothing do do with balls.
## This takes an image and turns it into a number smaller images
## Overlap is half of an image
##Use imageSmallerinator to split an image into smaller photos
##Use box in photo to split into smaller photos and find new coordinates of a given ocld in the small photos. 
###Can do as many photos and odlc's as you want it to.



##########PROGRAMMED BY:##########
##########KEAN JONES##########
#*Explosion*#
#*Fireworks, etc.*#

from PIL import Image
import numpy as np
import json
from typing import TypeAlias

ODLCdetection: TypeAlias = dict[str,str|int|float]
Picture: TypeAlias = dict[str,int|ODLCdetection]


def imageSmallerinator(numRows: int = 5, numColumns: int = 5, imgPath: str = 'testBalls.jpg') -> list[list[list[float]]]:
    img: Image = Image.open(imgPath)
    width, height = img.size  #both are ints
    baseColumnWidth: float = width / (numColumns + 1)
    baseRowHeight: float = height / (numRows + 1)
    r: int = 0
    c: int = 0
    dimentions: list = np.zeros((numRows, numColumns, 4))
    for row in dimentions:
        
        for column in row:
            #minx1
            column[0] = c * baseColumnWidth
            #miny1
            column[1] = r * baseRowHeight
            #maxx2
            column[2] = (c+1) * baseColumnWidth + baseColumnWidth
            #maxy2
            column[3] = (r+1) * baseRowHeight + baseRowHeight
            
            c += 1  
        r += 1
        c = 0
    i: int = 1
    for row in dimentions:
        for column in row:
            crop: Image = img.crop(column)
            crop.save(f'cropped{i}.jpg')
            i += 1


    return dimentions



def boxInPhoto(bigImage = 'testBalls.jpg',rows = 5, columns = 5,inputFile = 'input.json', outputFile = 'output.json'):
    picturesData: list = imageSmallerinator(rows,columns, bigImage)

    with open(inputFile, 'r') as f:
        input: dict[str,list[Picture]] = json.load(f)
    i: int = -1
    output: dict[str,list[Picture]] = {'Pictures' : []}

    validPictures: list = []

    for odlc in input['Pictures'][0]['ODLCS']:
        p: int = 0
        i += 1
        boxMinX: float = input['Pictures'][0]['ODLCS'][i]['minX']
        boxMinY: float = input['Pictures'][0]['ODLCS'][i]['minY']
        boxMaxX: float = input['Pictures'][0]['ODLCS'][i]['maxX']
        boxMaxY: float = input['Pictures'][0]['ODLCS'][i]['maxY']
        for row in picturesData:
            for picture in row:
                p += 1
                try:
                   output['Pictures'][p-1]
                except IndexError:
                    output['Pictures'].append({'Picture Number': p, 'ODLC detection Count': 0, 'ODLCS' : []})
                
                
                pictureMinX: float = picture[0]
                pictureMinY: float = picture[1]
                pictureMaxX: float = picture[2]
                pictureMaxY: float = picture[3]

                clause1: bool = pictureMinX < boxMinX < pictureMaxX and pictureMinY < boxMinY < pictureMaxY
                clause2: bool = pictureMinX < boxMaxX < pictureMaxX and pictureMinY < boxMinY < pictureMaxY
                clause3: bool = pictureMinX < boxMinX < pictureMaxX and pictureMinY < boxMaxY < pictureMaxY
                clause4: bool = pictureMinX < boxMaxX < pictureMaxX and pictureMinY < boxMaxY < pictureMaxY
                clause5: bool = boxMinX < pictureMinX < boxMaxX and boxMinY < pictureMinY < boxMaxY
                clause6: bool = boxMinX < pictureMaxX < boxMaxX and boxMinY < pictureMinY < boxMaxY
                clause7: bool = boxMinX < pictureMinX < boxMaxX and boxMinY < pictureMaxY < boxMaxY
                clause8: bool = boxMinX < pictureMaxX < boxMaxX and boxMinY < pictureMaxY < boxMaxY

                if clause1 or clause5 or clause2 or clause6 or clause3 or clause7 or clause4 or clause8:
                    validPictures.append(p)
                    output['Pictures'][p-1]['ODLC detection Count'] = output['Pictures'][p-1]['ODLC detection Count'] + 1
                    newBoxMinX: float = boxMinX - pictureMinX
                    newBoxMaxX: float = boxMaxX - pictureMinX
                    newBoxMinY: float = boxMinY - pictureMinY
                    newBoxMaxY: float = boxMaxY - pictureMinY
                    output['Pictures'][p-1]['ODLCS'].append(odlc)
                    currentOdlc = output['Pictures'][p-1]['ODLCS'][output['Pictures'][p-1]['ODLC detection Count']-1]
                    currentOdlc['minX'] = newBoxMinX
                    currentOdlc['maxX'] = newBoxMaxX
                    currentOdlc['minY'] = newBoxMinY
                    currentOdlc['maxY'] = newBoxMaxY

    with open(outputFile, "w") as outfile:
        json.dump(output, outfile, indent= 3)

    

#boxInPhoto(rows = 5, columns = 5)
#print(imageSmallerinator())