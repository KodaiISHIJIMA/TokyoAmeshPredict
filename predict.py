#!/usr/bin/env python
# -*- coding: utf-8 -*-
u'''Predict module'''

from skimage import io
import numpy as np
from matplotlib import pyplot as plt

from utils import ImageBase, Grid
from settings import Settings
from regist import RegularRegist

def _test():
    moving = ImageBase()
    moving.load_data(r'../TOKYO_AMESH_IMAGE/000/2009/200905290240.gif')

    fixed = ImageBase()
    fixed.load_data(r'../TOKYO_AMESH_IMAGE/000/2009/200905290250.gif')
    regist = RegularRegist(moving, fixed)
    regist.run()
    regist.linear_transform()
    convert_to_RGB(regist.vnext.values)

    #print regist.optimizer.vgrid.values
    #print regist.fixed.values
    #print regist.optimizer.cost

def convert_to_RGB(vmatrix):
    u'''Convert moved image to RGB image'''
    (nrow, ncol) = vmatrix.shape
    dt_stone = Settings.DATA_STONE
    dt_bound = Settings.DATA_BOUNDER
    bound_num = len(dt_bound)
    dt_max = Settings.DATA_MAX
    img = np.zeros((nrow, ncol, 3), dtype=np.uint8)
    for i in range(nrow):
        for j in range(ncol):
            value = vmatrix[i, j] * dt_max
            idx = 0
            while idx < bound_num-1 and dt_bound[idx] <= value:
                idx += 1
            img[i, j] = dt_stone[idx]
    io.imshow(img)
    plt.show()

def test_values_img():
    u'''Test value in images'''
    sample = set()
    for year in range(2009, 2010):
        folder_dir = os.path.join(Settings.DATA_DIR, str(year))
        for filepath in glob.glob(folder_dir + '/*.gif'):
            imgb = ImageBase()
            sample = sample.union(imgb.get_data(filepath))
            print filepath, sample

if __name__ == '__main__':
    _test()