# encoding: utf-8
"""
@author: julse@qq.com
@time: 2020/1/7 17:02
@desc:
"""
import numpy as np
def loadData(fin,sep='::',title=False):
    with open(fin,'r') as fo:
        if title:fo.readline()
        line = fo.readline()[:-1]
        while(line):
            yield line.split(sep)
            line = fo.readline()
def searchByID(fin,ID):
    # data = np.loadtxt(fin,delimiter='::') # 36.725s
    data = np.loadtxt(fin, delimiter='::',skiprows=1000000)  # for test
    data = data[data[:, 1] == ID]

