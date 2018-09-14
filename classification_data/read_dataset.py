


import glob
import cv2
import numpy as np

    



def import_data(path, suffle=False, one_hot_encoding = False, split = False):
    
    data=[img_path.replace('\\','/') for img_path in glob.glob(path+'/*/*')  
    if img_path.lower().endswith(".png" or ".jpg")]
    
    length=len(data)
    
    im_shape=cv2.imread(data[0]).shape
    data_x=np.empty([length,*im_shape])
    data_y=np.empty([length,1],dtype='U16')
    
    for idx, img_path in enumerate(data):
        label=img_path.split('/')[2]
        img=cv2.imread(img_path)/255.
        data_x[idx] = img
        data_y[idx] = label
    
    if suffle == True :
        permutation = np.random.permutation(length)
        data_x = data_x[permutation]
        data_y = data_y[permutation]
        
    if one_hot_encoding == True:
        label_name=np.unique(data_y)
        one_hot_length = label_name.shape[0]
        one_hot_label=np.identity(one_hot_length)
        one_hot_data=np.zeros((length,one_hot_length))
        
        
        for name, dummy in zip(label_name,one_hot_label):
            label_bool=(data_y==name).reshape(-1)
            one_hot_data[label_bool]=dummy
        
        data_y=one_hot_data
    
        
    if split == True :
        
        ratio = 0.8
        th=int(length*ratio)
        
        permutation = np.random.permutation(length)
        train_idx=permutation[:th]
        val_idx=permutation[th:]  

        train_x = data_x[train_idx]
        train_y = data_y[train_idx]
        val_x = data_x[val_idx]
        val_y = data_y[val_idx]

        return (train_x, train_y, val_x, val_y)
        
        
    return (data_x, data_y)
#
#path='./own_dataset'    
#x, y=import_data(path, suffle=True, one_hot_encoding=True, split=False)
#








