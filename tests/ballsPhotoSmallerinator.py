#This program has nothing do do with balls.
## This takes an image and turns it into a number smaller images
## Overlap is half of an image
##Use imageSmallerinator to split an image into smaller photos
##Use box in photo to split into smaller photos and find new coordinates of a given ocld in the small photos. 
###Can do as many photos and odlc's as you want it to.

from PIL import Image
import numpy as np
import json

def imageSmallerinator(numRows = 5, numColumns = 5, imgPath = 'testBalls.jpg'):
    img = Image.open(imgPath)
    width, height = img.size
    baseColumnWidth = width / (numColumns + 1)
    baseRowHeight = height / (numRows + 1)
    r = 0
    c = 0
    dimentions = np.zeros((numRows, numColumns, 4))
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
    i = 1
    for row in dimentions:
        for column in row:
            crop = img.crop(column)
            crop.save(f'cropped{i}.jpg')
            i += 1


    return dimentions



def boxInPhoto(bigImage = 'testBalls.jpg',rows = 5, columns = 5,inputFile = 'input.json', outputFile = 'output.json'):
    picturesData = imageSmallerinator(rows,columns, bigImage)

    with open(inputFile, 'r') as f:
        input = json.load(f)
    i = -1
    output = {'Pictures' : []}

    validPictures = []

    for odlc in input['Pictures'][0]['ODLCS']:
        p = 0
        i += 1
        boxMinX = input['Pictures'][0]['ODLCS'][i]['minX']
        boxMinY = input['Pictures'][0]['ODLCS'][i]['minY']
        boxMaxX = input['Pictures'][0]['ODLCS'][i]['maxX']
        boxMaxY = input['Pictures'][0]['ODLCS'][i]['maxY']
        for row in picturesData:
            for picture in row:
                p += 1
                try:
                   output['Pictures'][p-1]
                except IndexError:
                     output['Pictures'].append({'Picture Number': p, 'ODLC detection Count': 0, 'ODLCS' : []})
                
                
                pictureMinX = picture[0]
                pictureMinY = picture[1]
                pictureMaxX = picture[2]
                pictureMaxY = picture[3]

                clause1 = pictureMinX < boxMinX < pictureMaxX and pictureMinY < boxMinY < pictureMaxY
                clause2 = pictureMinX < boxMaxX < pictureMaxX and pictureMinY < boxMinY < pictureMaxY
                clause3 = pictureMinX < boxMinX < pictureMaxX and pictureMinY < boxMaxY < pictureMaxY
                clause4 = pictureMinX < boxMaxX < pictureMaxX and pictureMinY < boxMaxY < pictureMaxY
                clause5 = boxMinX < pictureMinX < boxMaxX and boxMinY < pictureMinY < boxMaxY
                clause6 = boxMinX < pictureMaxX < boxMaxX and boxMinY < pictureMinY < boxMaxY
                clause7 = boxMinX < pictureMinX < boxMaxX and boxMinY < pictureMaxY < boxMaxY
                clause8 = boxMinX < pictureMaxX < boxMaxX and boxMinY < pictureMaxY < boxMaxY

                if clause1 or clause5 or clause2 or clause6 or clause3 or clause7 or clause4 or clause8:
                    validPictures.append(p)
                    output['Pictures'][p-1]['ODLC detection Count'] = output['Pictures'][p-1]['ODLC detection Count'] + 1
                    newBoxMinX = boxMinX - pictureMinX
                    newBoxMaxX = boxMaxX - pictureMinX
                    newBoxMinY = boxMinY - pictureMinY
                    newBoxMaxY = boxMaxY - pictureMinY
                    output['Pictures'][p-1]['ODLCS'].append(odlc)
                    output['Pictures'][p-1]['ODLCS'][output['Pictures'][p-1]['ODLC detection Count']-1]['minX'] = newBoxMinX
                    output['Pictures'][p-1]['ODLCS'][output['Pictures'][p-1]['ODLC detection Count']-1]['maxX'] = newBoxMaxX
                    output['Pictures'][p-1]['ODLCS'][output['Pictures'][p-1]['ODLC detection Count']-1]['minY'] = newBoxMinY
                    output['Pictures'][p-1]['ODLCS'][output['Pictures'][p-1]['ODLC detection Count']-1]['maxY'] = newBoxMaxY

    with open(outputFile, "w") as outfile:
        json.dump(output, outfile, indent= 3)
    validPictures.sort()               

    

boxInPhoto(rows = 69, columns = 12)
#print(imageSmallerinator())