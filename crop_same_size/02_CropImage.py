# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 16:37:15 2018

@author: 2017B221
"""



import os
import glob
import matplotlib.pyplot as plt

w_Dir=os.getcwd()
img_Dir = w_Dir+'\data'

path_list=glob.glob(img_Dir+'\*')

result = []


imgFilenames = [f for f in os.listdir(img_Dir) if f.lower().endswith(".jpg")]
for index,filename in enumerate(imgFilenames):
    CropInfoPath = os.path.join(img_Dir, filename[:-4] + ".bboxes.tsv")
    
    if os.path.exists(CropInfoPath):
        
        img=plt.imread(os.path.join(img_Dir, filename))
        with open(CropInfoPath,'r') as tsv :
            bbox = [line.strip().split('\t') for line in tsv]
    
        try:
            for i in range(len(bbox)):
                x1=int(bbox[i][0])
                y1=int(bbox[i][1])
                x2=int(bbox[i][2])
                y2=int(bbox[i][3])
                crop_img=img[y1:y2,x1:x2,0:3]
                plt.imsave(w_Dir+'\crop\{}{}.png'.format(filename[:-4],i),crop_img)
        except:
            pass
