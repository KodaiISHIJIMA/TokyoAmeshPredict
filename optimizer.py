#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Optimizer class"""
import numpy as np

class RegularOptimizer(object):
    u'''Regular gradient descent optimizer'''

    def __init__(self, vgrid, deriv_grid, max_iters, base_lr):
        u'''Initialize regular optimizer'''
        # max_iters = max iterations
        # base_lr : the first learning rate
        self.iter = 0
        self.max_iters = max_iters
        self.lr = base_lr
        self.decay = 0.9
        self.vgrid = vgrid
        self.vdervgrid = deriv_grid
        self.cost = None

    def converged(self):
        u'''Check convergence condition'''
        # NEED TO IMPLEMENTATION 
        if self.iter >= self.max_iters:
            return True
        else:
            return False

    def forward(self, prev_deriv):
        u'''Forward the optimizer to the next step'''
        # Check converged condition
        
        if self.converged():
            return False
        else:
            (gysize, gxsize) = self.vgrid.size
            # Check gradient direction
            total = 0.0
            magnitude = 0.0
            for gy in range(gysize):
                for gx in range(gxsize):
                    total += np.sum(self.vdervgrid.values[gy, gx] * prev_deriv.values[gy, gx])
                    magnitude += np.sum(self.vdervgrid.values[gy, gx] * self.vdervgrid.values[gy, gx])
            
            # print 'magnitude: ', np.sqrt(magnitude),

            if total < 0.0:
                # Reduce learning rate
                self.lr *= self.decay

            # Update vgrid by vdervgrid
            for gy in range(gysize):
                for gx in range(gxsize):
                    # NEED TO IMPLEMENTATION
                    self.vgrid.values[gy, gx] -= self.lr * self.vdervgrid.values[gy, gx]

            # Increase interation step
            self.iter += 1
            return True