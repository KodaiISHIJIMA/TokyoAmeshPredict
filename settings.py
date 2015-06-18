#!/usr/bin/env python
# -*- coding: utf-8 -*-

u'''Setting for environment'''

class Settings:
    def __init__(self):
        u'''Init'''
        pass

    DATA_DIR = r'../TOKYO_AMESH_IMAGE/000'
    DATA_MAX = 80.0
    DATA_MIN = 0.0
    DATA_BOUNDER = [0, 4, 10, 20, 30, 40, 50, 80, 80]
    DATA_STONE = [(0, 0, 0), (204, 255, 255), (102, 153, 255), \
        (51, 51, 255), (0, 255, 0), (255, 255, 0), (255, 153, 0), \
        (255, 0, 255), (255, 0, 0)]

    DATA = {}
    DATA[(0, 0, 0)] = 0 # 雨が降ってない
    DATA[(0, 0, 1)] = 0 # 雨が降ってない
    DATA[(204, 255, 255)] = 2 # 弱い雨 1->3 mm/h
    DATA[(102, 153, 255)] = 7 # 並の雨 4->9 mm/h
    DATA[(51, 51, 255)] = 15  # やや強い雨 10->19 mm/h
    DATA[(0, 255, 0)] = 25    # 強い雨 20->29 mm/h
    DATA[(255, 255, 0)] = 35  # やや激しい雨 30->39 mm/h
    DATA[(255, 153, 0)] = 45  # 激しい雨 40->49 mm/h
    DATA[(255, 0, 255)] = 65  # 非常に激しい雨 50->80 mm/h
    DATA[(255, 0, 0)] = 80    # 猛烈雨 80 mm/h ~