#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Regist params namespace"""
import numpy as np

from optimizer import RegularOptimizer
from utils import Grid, ImageGrad, ImageBase, linear_interpolator
from settings import Settings

def CalMAD(moving, fixed):
    # NEED TO IMPLEMENTATION
    pass

def CalMADByGrid(moving, fixed, vgrid, skip):
    # NEED TO IMPLEMENTATION
    u'''calculate Mean Absolute Difference'''
    assert(moving.size == fixed.size)

    (ysize,xsize) = moving.size
    (orgy, orgx) = vgrid.origin
    spacing = vgrid.spacing

    xmax = xsize - 1
    ymax = ysize - 1
    Ed = 0.0

    for y in range(0, ysize, skip):
        gy = ( (y - orgy) / spacing[1])
        ry = float(y % spacing[1]) / float(spacing[1])
        for x in range(0, xsize, skip):
            gx = ( (x - orgx) // spacing[0])
            rx = float(x % spacing[0]) / float(spacing[0])

            v00 = vgrid.values[gy  , gx  ]
            v01 = vgrid.values[gy  , gx+1]
            v10 = vgrid.values[gy+1, gx  ]
            v11 = vgrid.values[gy+1, gx+1]

            v0 = (1 - rx) * v00 + rx * v01 
            v1 = (1 - rx) * v11 + rx * v10
            v  = (1 - ry) * v1  + ry * v0

            coord = np.array([x, y]) + v

            # Find value in fixed
            g = linear_interpolator(moving, coord)
            
            # For out of bound
            if g < 0.0:
                g = 0.0
            if g > 1.0:
                g = 1.0

            Ed += np.abs(fixed.values[y, x] - g)

    Ed /= (xsize * ysize / (skip**2))
    return Ed

def CalImageGrad(moving):
    u'''Calculate image gradient'''
    vgrad = ImageGrad(moving.size)
    (ysize, xsize) = moving.size
    for y in range(ysize):
        ynext = min(y+1, ysize-1)
        yprev = max(y-1, 0)    
        for x in range(xsize):
            xnext = min(x+1, xsize-1)
            xprev = max(x-1, 0)

            vgrad.values[y, x, 0] = (moving.values[y, xnext] - moving.values[y, xprev]) / 2.0
            vgrad.values[y, x, 1] = (moving.values[ynext, x] - moving.values[yprev, x]) / 2.0

    return vgrad

def CalLinearDeriv(moving, fixed, vgrad, vgrid, skip):
    # NEED TO IMPLEMENTATION
    assert(moving.size == fixed.size)

    (gysize, gxsize) = vgrid.size
    (ysize, xsize) = fixed.size

    spacing = vgrid.spacing
    origin = vgrid.origin
    deriv = Grid(moving.size, spacing)

    for gy in range(gysize - 1):
        py =  spacing[1] * gy + origin[1]
        ymin = max(py, 0)
        ymax = min(py + spacing[1], ysize)
        for gx in range(gxsize - 1):
            px = spacing[0] * gx + origin[0]
            xmin = max(px, 0)
            xmax = min(px + spacing[0], xsize)

            # Add to deriv grid (gx,gy), (gx,gy+1), (gx+1,gy), (gx+1,gy+1)
            a00, a01 = np.array([0.0, 0.0]), np.array([0.0, 0.0])
            a10, a11 = np.array([0.0, 0.0]), np.array([0.0, 0.0])

            v00 = vgrid.values[gy  , gx  ]
            v01 = vgrid.values[gy  , gx+1]
            v10 = vgrid.values[gy+1, gx  ]
            v11 = vgrid.values[gy+1, gx+1]

            for y in range(ymin, ymax, skip):
                ry = (y - py) / float(spacing[1])
                for x in range(xmin, xmax, skip):
                    rx = (x - px) / float(spacing[0])
                    v0 = (1 - rx) * v00 + rx * v01 
                    v1 = (1 - rx) * v11 + rx * v10
                    v  = (1 - ry) * v1  + ry * v0
                    coord = np.array([x, y]) + v

                    # Find value in fixed
                    g = linear_interpolator(moving, coord)
                    
                    # For out of bound
                    if g < 0.0:
                        g = 0.0
                    if g > 1.0:
                        g = 1.0

                    flag = np.sign(g - fixed.values[y, x])
                    # Find value in vgrad
                    tmp_grad = linear_interpolator(vgrad, coord) * flag

                    a00 += (1 - rx) * (1 - ry) * tmp_grad
                    a01 += (rx    ) * (1 - ry) * tmp_grad
                    a10 += (1 - rx) * (ry    ) * tmp_grad
                    a11 += (rx    ) * (ry    ) * tmp_grad

                    # print g, rx, ry, 1-rx, 1-ry, flag, tmp_grad, a00, a01, a10, a11

            deriv.values[gy  , gx  ] += a00
            deriv.values[gy  , gx+1] += a01
            deriv.values[gy+1, gx  ] += a10
            deriv.values[gy+1, gx+1] += a11

    deriv.values = deriv.values / (xsize * ysize / (skip**2))
    return deriv

def CalLinearDerivAndMAD(moving, fixed, vgrad, vgrid, skip):
    # NEED TO IMPLEMENTATION
    assert(moving.size == fixed.size)

    (gysize, gxsize) = vgrid.size
    (ysize, xsize) = fixed.size

    spacing = vgrid.spacing
    origin = vgrid.origin
    deriv = Grid(moving.size, spacing)
    mad = 0.0

    for gy in range(gysize - 1):
        py =  spacing[1] * gy + origin[1]
        ymin = max(py, 0)
        ymax = min(py + spacing[1], ysize)
        for gx in range(gxsize - 1):
            px = spacing[0] * gx + origin[0]
            xmin = max(px, 0)
            xmax = min(px + spacing[0], xsize)

            # Add to deriv grid (gx,gy), (gx,gy+1), (gx+1,gy), (gx+1,gy+1)
            a00, a01 = np.array([0.0, 0.0]), np.array([0.0, 0.0])
            a10, a11 = np.array([0.0, 0.0]), np.array([0.0, 0.0])

            v00 = vgrid.values[gy  , gx  ]
            v01 = vgrid.values[gy  , gx+1]
            v10 = vgrid.values[gy+1, gx  ]
            v11 = vgrid.values[gy+1, gx+1]

            for y in range(ymin, ymax, skip):
                ry = (y - py) / float(spacing[1])
                for x in range(xmin, xmax, skip):
                    rx = (x - px) / float(spacing[0])
                    v0 = (1 - rx) * v00 + rx * v01 
                    v1 = (1 - rx) * v11 + rx * v10
                    v  = (1 - ry) * v1  + ry * v0
                    coord = np.array([x, y]) + v

                    # Find value in fixed
                    g = linear_interpolator(moving, coord)
                    
                    # For out of bound
                    if g < 0.0:
                        g = 0.0
                    if g > 1.0:
                        g = 1.0

                    flag = np.sign(g - fixed.values[y, x])
                    mad += np.abs(g - fixed.values[y, x])

                    # Find value in vgrad
                    tmp_grad = linear_interpolator(vgrad, coord) * flag

                    a00 += (1 - rx) * (1 - ry) * tmp_grad
                    a01 += (rx    ) * (1 - ry) * tmp_grad
                    a10 += (1 - rx) * (ry    ) * tmp_grad
                    a11 += (rx    ) * (ry    ) * tmp_grad

                    # print g, rx, ry, 1-rx, 1-ry, flag, tmp_grad, a00, a01, a10, a11

            deriv.values[gy  , gx  ] += a00
            deriv.values[gy  , gx+1] += a01
            deriv.values[gy+1, gx  ] += a10
            deriv.values[gy+1, gx+1] += a11

    Nsize = xsize * ysize / (skip**2)
    deriv.values = deriv.values / Nsize
    mad /= Nsize
    return deriv, mad
               
def CalCubicDeriv(moving, fixed, vgrad, vgrid):
    # NEED TO IMPLEMENTATION
    pass

def CalCubicDerivAndMAD(moving, fixed, vgrad, vgrid):
    # NEED TO IMPLEMENTATION
    pass

class RegularRegist(object):
    u'''Registration class'''

    def __init__(self, moving, fixed, skip = 4, spacing=(32, 32), max_iters=50, base_lr=100):
        u'''Init regist class with two images'''
        assert(moving.size == fixed.size)

        self.moving = moving
        self.fixed = fixed
        self.skip = skip
        self.movgrad = CalImageGrad(moving)
        self.vnext = None
        self.vgrid = Grid(moving.size, spacing)
        # Initialize optimizer with vgrid and dervgrid
        self.optimizer = RegularOptimizer(self.vgrid, Grid(moving.size, spacing), \
                max_iters=max_iters, base_lr=base_lr)

    def run(self):
        u'''Run to find vgrid'''
        
        self.optimizer.vdervgrid = CalLinearDeriv(self.moving, self.fixed, self.movgrad, \
            self.optimizer.vgrid, self.skip)
        prev_deriv = Grid(self.moving.size, self.vgrid.spacing)

        #print self.optimizer.vdervgrid.values
        #print self.movgrad.values

        while self.optimizer.forward(prev_deriv):
            prev_deriv = self.optimizer.vdervgrid

            # self.optimizer.vdervgrid = CalLinearDeriv(self.moving, self.fixed, self.movgrad, \
            #     self.optimizer.vgrid, self.skip)
            # self.optimizer.cost = CalMADByGrid(self.moving, self.fixed, \
            #     self.optimizer.vgrid, self.skip)

            # Or can call
            self.optimizer.vdervgrid, self.optimizer.cost = \
              CalLinearDerivAndMAD(self.moving, self.fixed, self.movgrad, \
                  self.optimizer.vgrid, self.skip)
            print ' iter ', self.optimizer.iter, ' cost ', self.optimizer.cost, ' learning rate ', self.optimizer.lr

        self.vgrid = self.optimizer.vgrid

    def linear_transform(self):
        u'''Linear transform fixed image to next image'''
        # NEED TO IMPLEMENTATION
        (ysize, xsize) = self.fixed.size
        self.vnext = ImageBase(size=(ysize, xsize))

        (orgy, orgx) = self.vgrid.origin
        spacing = self.vgrid.spacing

        xmax = xsize - 1
        ymax = ysize - 1
        Ed = 0.0

        for y in range(ysize):
            gy = ( (y - orgy) / spacing[1])
            ry = float(y % spacing[1]) / float(spacing[1])
            for x in range(xsize):
                gx = ( (x - orgx) // spacing[0])
                rx = float(x % spacing[0]) / float(spacing[0])

                v00 = self.vgrid.values[gy  , gx  ]
                v01 = self.vgrid.values[gy  , gx+1]
                v10 = self.vgrid.values[gy+1, gx  ]
                v11 = self.vgrid.values[gy+1, gx+1]

                v0 = (1 - rx) * v00 + rx * v01 
                v1 = (1 - rx) * v11 + rx * v10
                v  = (1 - ry) * v1  + ry * v0

                coord = np.array([x, y]) + v

                # Find value in fixed
                g = linear_interpolator(self.fixed, coord)
                # For out of bound
                if g < 0.0:
                    g = 0.0
                if g > 1.0:
                    g = 1.0

                self.vnext.values[y, x] = g

    def cubic_transform(self):
        u'''Linear transform moving image by vgrid'''
        # NEED TO IMPLEMENTATION
        pass
