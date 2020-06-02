# encoding: utf-8
"""
@author: julse@qq.com
@time: 2020/1/7 17:02
推荐系统ted
"""

# coding=utf-8
import math, pickle, time
from collections import defaultdict  # 可以直接使用下标访问二维字典不存在的元素
import sys, operator
from operator import itemgetter
from time import sleep
import numpy as np
import os
from loadData import loadData, searchByID
import pandas as pd
class prepareData():
    def createFavorite(self,fin,fout,foutTalk):
        """
            user.csv -> favorite.csv
        :param fin:
        :param fout:
        :return:
        """
        # fin = 'file/ted/testUser.csv'
        # fout = 'file/ted/testFavorite.csv'
        user = pd.read_table(fin)
        talk = user['talk'].drop_duplicates()
        talk.to_csv(foutTalk)
        favorite = pd.DataFrame()
        favorite['userID'] = user['user']
        favorite['talkID'] = user['talk'].replace(talk.values,talk.index )
        favorite['rating'] = [1 for x in range(len(favorite))]
        favorite.to_csv(fout, index=False, header=False)

class Recommend(object):
    def __init__(self,fin,in_dir=''):
        self.userItems = dict()  # 用户到物品的倒排表
        self.C = defaultdict(defaultdict)  # 用户与用户共同喜欢物品的个数
        self.N = defaultdict(defaultdict)  # 用户个数
        self.W = defaultdict(defaultdict)  # 相似度矩阵
        self.K = 20  # 选取前k个最相似的物品计算预测相似度
        self.fin = fin
        self.in_dir = in_dir
        self.load_matrix_w()

    def _build_inver_table(self):
        """
        倒排表
        :return:
        """
        doc = loadData(self.fin,sep=',')
        count = 0
        for d in doc:
            print(count)
            count += 1
            UserID = d[0]
            if UserID not in self.userItems:
                self.userItems[UserID] = set()
            MovieID = d[1]
            self.userItems[UserID].add(MovieID)
    def _cal_corated_users(self):
        """
        共现矩阵
        :return:
        """
        for u, items in self.userItems.items():
            for i in items:
                # i = i[0]
                if i not in self.N.keys():  # 如果一维字典中没有该键，初始化值为0
                    self.N[i] = 0
                self.N[i] = self.N[i] + 1
                for j in items:
                    # j = j[0]
                    if i == j:
                        continue
                    if j not in self.C[i].keys():  # 如果二维字典中没有该键，初始化值为0
                        self.C[i][j] = 0
                    self.C[i][j] += 1

    def _cal_matrix_W(self):
        """
        计算余弦相似度矩阵
        :return:
        """
        for i, related_items in self.C.items():
            for j, cij in related_items.items():
                self.W[i][j] = cij / math.sqrt(self.N[i] * self.N[j])  # 余弦相似度

    def _save_matrix_w(self):
        """
        保存矩阵
        :return:
        """
        f = open(self.in_dir+'matrixW.txt', 'wb')
        pickle.dump(self.W, f)
        f.close()

    def load_matrix_w(self):  # 载入大概需要7.96s
        fW = self.in_dir+'matrixW.txt'
        if os.access(fW, os.F_OK):
            f = open(fW,'rb')
            try:
                self.W = pickle.load(f)
            except:
                print('wrong in matrixW.txt')
            f.close()
    def cal_matrix_W(self):
        self.W.clear()
        print(len(self.W))
        sleep(3)
        print('build inver table...')
        self._build_inver_table()
        print('cal corated users...')
        self._cal_corated_users()
        print('save matrix...')
        self._cal_matrix_W()
        print('save matrix...')
        self._save_matrix_w()

    def recommend(self, UserID):
        rank = dict()
        data = np.loadtxt(self.fin, delimiter=',',dtype=int)  # for test
        ru = data[data[:, 0] == UserID]  # 用户数据，表示某物品及其兴趣度
        for r in ru:# i表示用户已评价的电影id，pi表示其兴趣度（评分）
            i = r[1]
            pi = r[2]
            # j表示相似度为前K个物品的id，wj表示物品i和物品j的相似度
            for j, wj in sorted(self.W[str(i)].items(), key=itemgetter(1), reverse=True)[0:self.K]:
                if int(j) in ru[:,1]:  # 如果用户已经有了物品j，则不再推荐
                    continue
                # rank = dict()
                if j not in rank.keys():
                    rank[j] = 0
                rank[j] += pi * wj
        return rank



if __name__ == '__main__':
    # in_dir = 'file/ted/test'
    in_dir = 'file/ted/'
    fin = '%s/user.csv'%in_dir
    outFavorite = '%s/favorite.csv'%in_dir
    foutTalk = '%s/talk.csv'%in_dir
    preD = prepareData()
    preD.createFavorite(fin, outFavorite, foutTalk)
    recommend = Recommend(outFavorite,in_dir=in_dir)
    recommend.cal_matrix_W()
    rank = recommend.recommend(1)
    print('all down!',rank)
    print()
