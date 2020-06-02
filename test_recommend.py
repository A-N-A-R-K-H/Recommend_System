# encoding: utf-8
"""
@author: julse@qq.com
@time: 2020/1/7 17:02
@desc:
"""
from collections import defaultdict
from unittest import TestCase

from loadDat import loadData



class TestRecommend(TestCase):
    def test__build_inver_table(self):
        self.userItems = dict()  # 用户到物品的倒排表
        self.C = defaultdict(defaultdict)  # 用户与用户共同喜欢物品的个数
        self.N = defaultdict(defaultdict)  # 用户个数
        self.W = defaultdict(defaultdict)  # 相似度矩阵
        self.k = 20  # 选取前k个最相似的物品计算预测相似度
        doc = loadData('file/ratings.dat')
        # UserID::MovieID::Rating::Timestamp
        count = 0
        for d in doc:
            print(count)
            count += 1
            UserID = d[0]
            if UserID not in self.userItems:
                self.userItems[UserID] = set()
            MovieID = d[1]
            Rating = d[2]
            self.userItems[UserID].add((MovieID, Rating))
            #         todo 此处添加的是元祖，后续处理需要记住
            if count> 20:break
        for u, items in self.userItems.items():
            for i in items:
                i = i[0]
                if i not in self.N.keys():  # 如果一维字典中没有该键，初始化值为0
                    self.N[i] = 0
                self.N[i] += 1
                for j in items:
                    j=j[0]
                    if i == j:
                        continue
                    if j not in self.C[i].keys():  # 如果二维字典中没有该键，初始化值为0
                        self.C[i][j] = 0
                    self.C[i][j] += 1
        # for u, items in self.userItems.items():
        #     for i in items:
        #         if i[0] not in self.N.keys():  # 如果一维字典中没有该键，初始化值为0
        #             self.N[i[0]] = 0
        #         self.N[i[0]] += 1
        #         for j in items:
        #             if i[0] == j[0]:
        #                 continue
        #             if j[0] not in self.C[i[0]].keys():  # 如果二维字典中没有该键，初始化值为0
        #                 self.C[i[0]][j[0]] = 0
        #             self.C[i[0]][j[0]] += 1
        print('end')

