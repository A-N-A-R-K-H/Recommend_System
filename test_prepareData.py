# encoding: utf-8
"""
@author: julse@qq.com
@time: 2020/3/27 15:42
@desc:
"""
from unittest import TestCase

from ItemCF0327 import prepareData


class TestPrepareData(TestCase):
    def test_createFavorite(self):
        fin = 'file/ted/testUser.csv'
        fout = 'file/ted/testFavorite.csv'
        foutTalk = 'file/ted/testTalk.csv'
        preD = prepareData()
        preD.createFavorite(fin,fout,foutTalk)