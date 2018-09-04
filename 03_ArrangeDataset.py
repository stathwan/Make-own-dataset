# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 16:04:32 2018

@author: 2017B221
"""




import os
import glob


w_Dir=os.getcwd()
img_Dir = w_Dir+'\data'

im_path=glob.glob(img_Dir+'\*')

if len(im_path)%3 != 0 :
    print("ERROR. it must be composed of JPG, bboxes and labels files")
    raise ValueError

result = []
for j in range(int(len(im_path)/3)):

    target_path=im_path[2+j*3]
    
    with open(im_path[0+j*3],'r') as tsv :
        label = [line.strip().split('\t') for line in tsv]
                 
    with open(im_path[1+j*3],'r') as tsv :
        bbox = [line.strip().split('\t') for line in tsv]
                
    for i in range(len(label)):
        tmp=[target_path]+bbox[i]+label[i]
        result.append(','.join(tmp))

with open("test.txt", "w") as f:
    for s in result:
        f.write(str(s) +"\n")
        

