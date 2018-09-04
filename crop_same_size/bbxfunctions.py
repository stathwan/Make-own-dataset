import os
import cv2

from PIL import Image

### imread
def imread(imgPath, boThrowErrorIfExifRotationTagSet = True):
    if not os.path.exists(imgPath):
        print("ERROR: image path does not exist.")
        
    img = cv2.imread(imgPath)
    if img is None:
        print ("ERROR: cannot load image " + imgPath)
        
    return img

    
### resize
def imresize(img, scale, interpolation = cv2.INTER_LINEAR):
    return cv2.resize(img, (0,0), fx=scale, fy=scale, interpolation=interpolation)

def imresizeMaxDim(img, maxDim, boUpscale = False, interpolation = cv2.INTER_LINEAR):
    scale = 1.0 * maxDim / max(img.shape[:2])
    if scale < 1  or boUpscale:
        img = imresize(img, scale, interpolation)
    else:
        scale = 1.0
    return img, scale
    
def imArrayWidthHeight(input):
    width =  input.shape[1]
    height = input.shape[0]
    return width,height
    
def imWidthHeight(input):
    width, height = Image.open(input).size #this does not load the full image
    return width,height
    
def imWidth(input):
    return imWidthHeight(input)[0]

def imHeight(input):
    return imWidthHeight(input)[1]    

def writeTable(outputFile, table):
    lines = tableToList1D(table)
    writeFile(outputFile, lines)

def writeFile(outputFile, lines):
    with open(outputFile,'w') as f:
        for line in lines:
            f.write("%s\n" % line)    
    
def tableToList1D(table, delimiter='\t'):
    return [delimiter.join([str(s) for s in row]) for row in table]
            

def ptClip(pt, maxWidth, maxHeight):
    pt = list(pt)
    pt[0] = max(pt[0], 0)
    pt[1] = max(pt[1], 0)
    pt[0] = min(pt[0], maxWidth)
    pt[1] = min(pt[1], maxHeight)
    return pt
    
    
### drawRectangles
def ToIntegers(list1D):
    return [int(float(x)) for x in list1D]

def drawRectangles(img, rects, color = (0, 255, 0), thickness = 2):
    for rect in rects:
        pt1 = tuple(ToIntegers(rect[0:2]))
        pt2 = tuple(ToIntegers(rect[2:]))
        cv2.rectangle(img, pt1, pt2, color, thickness)
        
### drawCrossbar
def drawCrossbar(img, pt):
    (x,y) = pt
    cv2.rectangle(img, (0, y), (x, y), (255, 255, 0), 1)
    cv2.rectangle(img, (x, 0), (x, y), (255, 255, 0), 1)
    cv2.rectangle(img, (img.shape[1],y), (x, y), (255, 255, 0), 1)
    cv2.rectangle(img, (x, img.shape[0]), (x, y), (255, 255, 0), 1)


class Bbox:
    MAX_VALID_DIM = 100000
    left = top = right = bottom = None

    def __init__(self, left, top, right, bottom):
        self.left   = int(round(float(left)))
        self.top    = int(round(float(top)))
        self.right  = int(round(float(right)))
        self.bottom = int(round(float(bottom)))
        self.standardize()

    def __str__(self):
        return ("Bbox object: left = {0}, top = {1}, right = {2}, bottom = {3}".format(self.left, self.top, self.right, self.bottom))

    def __repr__(self):
        return str(self)

    def rect(self):
        return [self.left, self.top, self.right, self.bottom]

    def max(self):
        return max([self.left, self.top, self.right, self.bottom])

    def min(self):
        return min([self.left, self.top, self.right, self.bottom])

    def width(self):
        width  = self.right - self.left + 1
        assert(width>=0)
        return width

    def height(self):
        height = self.bottom - self.top + 1
        assert(height>=0)
        return height

    def surfaceArea(self):
        return self.width() * self.height()

    def getOverlapBbox(self, bbox):
        left1, top1, right1, bottom1 = self.rect()
        left2, top2, right2, bottom2 = bbox.rect()
        overlapLeft = max(left1, left2)
        overlapTop = max(top1, top2)
        overlapRight = min(right1, right2)
        overlapBottom = min(bottom1, bottom2)
        if (overlapLeft>overlapRight) or (overlapTop>overlapBottom):
            return None
        else:
            return Bbox(overlapLeft, overlapTop, overlapRight, overlapBottom)

    def standardize(self): #NOTE: every setter method should call standardize
        leftNew   = min(self.left, self.right)
        topNew    = min(self.top, self.bottom)
        rightNew  = max(self.left, self.right)
        bottomNew = max(self.top, self.bottom)
        self.left = leftNew
        self.top = topNew
        self.right = rightNew
        self.bottom = bottomNew

    def crop(self, maxWidth, maxHeight):
        leftNew   = min(max(self.left,   0), maxWidth)
        topNew    = min(max(self.top,    0), maxHeight)
        rightNew  = min(max(self.right,  0), maxWidth)
        bottomNew = min(max(self.bottom, 0), maxHeight)
        return Bbox(leftNew, topNew, rightNew, bottomNew)

    def isValid(self):
        if self.left>=self.right or self.top>=self.bottom:
            return False
        if min(self.rect()) < -self.MAX_VALID_DIM or max(self.rect()) > self.MAX_VALID_DIM:
            return False
        return True

        
def scaleCropBboxes(rectsIn, scaleFactor, imgWidth, imgHeight):
    if len(rectsIn) <= 0:
        return rectsIn
    else:
        rects = [ [int(round(rect[i]/scaleFactor)) for i in range(4)]
                  for rect in rectsIn]
        rects = [Bbox(*rect).crop(imgWidth, imgHeight).rect() for rect in rects]
        for rect in rects:
            assert (Bbox(*rect).isValid())
        return rects
        
        
def getFilesInDirectory(directory, postfix = ""):
    fileNames = [s for s in os.listdir(directory) if not os.path.isdir(os.path.join(directory, s))]
    if not postfix or postfix == "":
        return fileNames
    else:
        return [s for s in fileNames if s.lower().endswith(postfix)]
                
def readTable(inputFile, delimiter='\t', columnsToKeep=None):
    lines = readFile(inputFile);
    columnsToKeepIndices = None
    return splitStrings(lines, delimiter, columnsToKeepIndices)
    
def readFile(inputFile):
    #reading as binary, to avoid problems with end-of-text characters
    #note that readlines() does not remove the line ending characters
    with open(inputFile,'rb') as f:
        lines = f.readlines()
    return [removeLineEndCharacters(s) for s in lines]

def splitStrings(strings, delimiter, columnsToKeepIndices=None):
    table = [splitString(string, delimiter, columnsToKeepIndices) for string in strings]
    return table;      

def removeLineEndCharacters(line):
    if line.endswith(b'\r\n'):
        return line[:-2]
    elif line.endswith(b'\n'):
        return line[:-1]
    else:
        return line

def splitString(string, delimiter='\t', columnsToKeepIndices=None):
    if string == None:
        return None
    items = string.decode('utf-8').split(delimiter)
    return items;      

def imconvertCv2Pil(img):
    cv2_im = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    return Image.fromarray(cv2_im)
    
def writeFile(outputFile, lines):
    with open(outputFile,'w') as f:
        for line in lines:
            f.write("%s\n" % line)

