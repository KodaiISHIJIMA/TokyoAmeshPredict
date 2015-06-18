#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import os
import sys
import numpy as np
from matplotlib import pyplot as plt
#from skimage.feature import hog
#from skimage import data, color, exposure
from skimage import io
from datetime import datetime, date, time, timedelta

DATA_DIR = r'../TOKYO_AMESH_IMAGE/000'

def display(timestr, num_prev = 9, row = 3):
    u'''Display previous images before time string'''
    u'''Example: display(200905290250)'''
    year = int(timestr[0:4])
    month = int(timestr[4:6])
    day = int(timestr[6:8])
    hour = int(timestr[8:10])
    mins = int(timestr[10:12])

    d = date(year, month, day)
    t = time(hour, mins)
    dt = datetime.combine(d, t)
    # Time interval
    diff = timedelta(minutes=10)

    # Get the paths of images
    show_files = []
    for i in range(num_prev):
        dt = dt - diff
        print dt
        filename = str(dt.year).zfill(4) + str(dt.month).zfill(2) + \
            str(dt.day).zfill(2) + str(dt.hour).zfill(2) + str(dt.minute).zfill(2) + '.gif'
        folder_dir = os.path.join(DATA_DIR, str(dt.year))
        filepath = os.path.join(folder_dir, filename)
        if os.path.exists(filepath):
            show_files.append(filepath)

    col = len(show_files) / row
    fig, axes = plt.subplots(row, col)
    for i in range(row):
        for j in range(col):
            # Load images
            file_path = show_files[i*col+j]
            img_file = io.imread(file_path)
            
            #image = color.rgb2gray(img_file)
            #fd, hog_image = hog(image, orientations=8, pixels_per_cell=(16, 16), 
            #    cells_per_block=(1, 1), visualise=True)
            #hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 0.02))

            axes[i, j].imshow(img_file, cmap='gray')
            axes[i, j].set_title('%s' % (file_path[(-16):(-4)]))
            
            plt.setp(axes[i, j].get_xticklines(), visible=False)
            plt.setp(axes[i, j].get_xticklabels(), visible=False)

            plt.setp(axes[i, j].get_yticklines(), visible=False)
            plt.setp(axes[i, j].get_yticklabels(), visible=False)

    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.1, hspace=0.1)
    fig.suptitle('Time string %s.' % timestr)
    plt.show()
    return True

if __name__ == '__main__':
    display('200905290310', 4, 2)