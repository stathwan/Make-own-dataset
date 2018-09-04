# Copyright (c) Microsoft. All rights reserved.

# Licensed under the MIT license. See LICENSE.md file in the project root
# for full license information.
# ==============================================================================

from builtins import chr
import os, sys
import cv2
from bbxfunctions import drawRectangles, imArrayWidthHeight, ptClip, drawCrossbar, imresizeMaxDim,\
                         scaleCropBboxes, writeTable, imread, imWidth, imHeight

####################################
# Parameters
####################################

imgDir = os.getcwd() +"\data"

# no need to change these params
drawingImgSize = 10000.0
boxlength=40 ### 중요 

####################################
# Functions
####################################

    
def event_cv2_drawRectangles(event, x, y, flags, param):
    global global_image
    global global_bboxes
    global global_leftButtonDownPoint

    # draw all previous bounding boxes, and the most recent box in a different color
    imgCopy = global_image.copy()
    drawRectangles(imgCopy, global_bboxes)
    if len(global_bboxes)>0:
        drawRectangles(imgCopy, [global_bboxes[-1]], color = (255, 0, 0))

    # handle mouse events
    if event == cv2.EVENT_LBUTTONDOWN:
        global_leftButtonDownPoint = (x, y)
        pt=global_leftButtonDownPoint
        h_blength=boxlength//2
        roi_rect=[pt[0]-h_blength]+[pt[1]-h_blength]+[pt[0]+h_blength]+[pt[1]+h_blength]
        print(roi_rect)
        global_bboxes.append(roi_rect)

    else:
        drawCrossbar(imgCopy, (x, y))
    cv2.imshow("AnnotationWindow", imgCopy)

    
####################################
# Main
####################################
imgFilenames = [f for f in os.listdir(imgDir) if f.lower().endswith(".jpg")]

# loop over each image and get annotation
for imgFilenameIndex,imgFilename in enumerate(imgFilenames):
    print (imgFilenameIndex, imgFilename)
    imgPath = os.path.join(imgDir, imgFilename)
    bBoxPath = imgPath[:-4] + ".bboxes.tsv"

    # skip image if ground truth already exists
    if os.path.exists(bBoxPath):
        print ("Skipping image {0} since ground truth already exists".format(imgFilename))
        continue
    else:
        print ("Processing image {0} of {1}: {2}".format(imgFilenameIndex, len(imgFilenames), imgPath))

    # prepare image window and callback
    global_bboxes = []
    global_image, scaleFactor = imresizeMaxDim(imread(imgPath), drawingImgSize)
    cv2.namedWindow("AnnotationWindow")
    cv2.setMouseCallback("AnnotationWindow", event_cv2_drawRectangles)
    cv2.imshow("AnnotationWindow", global_image)

    # process user input
    while True:
        key = chr(cv2.waitKey())

        # undo/remove last rectangle
        if key == "u":
            if len(global_bboxes) >= 1:
                global_bboxes = global_bboxes[:-1]
                imgCopy = global_image.copy()
                drawRectangles(imgCopy, global_bboxes)
                cv2.imshow("AnnotationWindow", imgCopy)

        # skip image
        elif key == "s":
            if os.path.exists(bBoxPath):
                print ("Skipping image hence deleting existing bbox file: " + bBoxPath)
                os.remove(bBoxPath)
            break

        # next image
        elif key == "n":
            bboxes = scaleCropBboxes(global_bboxes, scaleFactor, imWidth(imgPath), imHeight(imgPath))
            writeTable(bBoxPath, bboxes)
            break

        # quit
        elif key == "q":
            sys.exit()

cv2.destroyAllWindows()
