#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Util functions"""

import numpy as np
import os
import glob
from skimage import io
from settings import Settings

class ImageBase(object):
    u'''Image base class for loading image'''

    def __init__(self, size=None):
        u'''Init function'''
        self.filepath = None
        self.size = size
        if size:
            self.values = np.zeros(size, dtype=np.float32)
        else:
            self.values = None

    def load_data(self, filepath):
        u'''Load data from filepath'''
        if os.path.exists(filepath):
            dt = Settings.DATA
            dt_max = Settings.DATA_MAX

            self.filepath = filepath
            img = io.imread(filepath)
            (nrow, ncol) = (img.shape[0], img.shape[1])
            self.size = (nrow, ncol) 
            # Initialize values for image
            self.values = np.zeros((nrow, ncol), dtype=np.float32)
            # Convert RBG 3 channels to float32 value in range [0, 1]
            for i in range(nrow):
                for j in range(ncol):
                    tpr = (img[i, j, 0], img[i, j, 1], img[i, j, 2])
                    if tpr in dt:
                        self.values[i, j] = dt[tpr] / dt_max
                    else:
                        self.values[i, j] = 0

    def get_data_pattern(self, filepath):
        u'''Get patterns of data'''
        if os.path.exists(filepath):
            self.filepath = filepath
            img = io.imread(filepath)
            (nrow, ncol) = (img.shape[0], img.shape[1])
            sample = set()
            for i in range(nrow):
                for j in range(ncol):
                    #tmp = np.int32(img[i, j, 0] << 8) | np.int32(img[i, j, 1])
                    #tmp = np.int32(tmp << 8) | np.int32(img[i, j, 2])
                    sample.add((img[i, j, 0], img[i, j, 1], img[i, j, 2]))
            return sample

class ImageGrad(object):
    u'''Image grad base class'''
    def __init__(self, nsize):
        u'''Init function'''
        self.size = nsize
        self.values = np.zeros((nsize[0], nsize[1], 2))


class Grid(object):
    u'''Control grids'''

    def __init__(self, nsize, spacing):
        u'''Init function'''
        self.origin = (-0*spacing[0], -0*spacing[1])
        srow = int( (nsize[0] - 1 - self.origin[1]) / spacing[1] ) + 2
        scol = int( (nsize[1] - 1 - self.origin[0]) / spacing[0] ) + 2
        self.size = (srow, scol)
        self.spacing = spacing
        self.values = np.zeros((srow, scol, 2))

def linear_interpolator(vol, coord):
    u'''Linear interpolator'''
    (ysize, xsize) = vol.size
    cx = coord[0]
    cy = coord[1]
    xmax = xsize - 1
    ymax = ysize - 1
    if cx >= 0 and cx < xsize and \
        cy >= 0 and cy < ysize:
        # Linear interpolator inside
        px = int(cx)
        py = int(cy)
        dx = float(cx) - float(px)
        dy = float(cy) - float(py)
        px1 = min(px+1, xmax)
        py1 = min(py+1, ymax)
        g00 = vol.values[py , px]
        g10 = vol.values[py1, px]
        g01 = vol.values[py , px1]
        g11 = vol.values[py1, px1]
        g0  = dx * g01 + (1.0 - dx) * g00
        g1  = dx * g11 + (1.0 - dx) * g10
        g   = dy * g1 + (1 - dy) * g0
    else:
        # Nearest interpolator outside
        px = int(cx)
        px = max(px, 0)
        px = min(px, xmax)
        py = int(cy)
        py = max(py, 0)
        py = min(py, ymax)
        g = vol.values[py, px]
    return g





