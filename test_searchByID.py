# encoding: utf-8
"""
@author: julse@qq.com
@time: 2020/1/7 17:02
@desc:
"""
from unittest import TestCase
import numpy as np

class TestSearchByID(TestCase):
    def test_searchByID(self):
        fin = 'file/ratings.dat'
        ID = 25
        data = np.loadtxt(fin, delimiter='::',skiprows=1000000) # 36.725s
        data = data[data[:, 1] == ID]
        print('end')

