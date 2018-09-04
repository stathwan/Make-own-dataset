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

for j in range(len(path_list)//2):

    im_path=path_list[1+j*2]
    img=plt.imread(im_path)
    with open(path_list[0+j*2],'r') as tsv :
        bbox = [line.strip().split('\t') for line in tsv]

    for i in range(len(bbox)):
        x1=int(bbox[i][0])
        y1=int(bbox[i][1])
        x2=int(bbox[i][2])
        y2=int(bbox[i][3])
        crop_img=img[y1:y2,x1:x2,0:3]
        plt.imsave(w_Dir+'\crop\{}{}.jpg'.format(im_path.split('\\')[-1][:-4],i),crop_img)

