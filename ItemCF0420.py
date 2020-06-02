# encoding: utf-8
"""
@author: julse@qq.com
@time: 2020/1/7 17:02
UCF for algebra_2005_2006
1. Andreas, T. & Jahrer, M. Collaborative Filtering Applied to Educational Data Mining. 1–11 (2010).
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

    def createFavorite(self,fin,outFavorite,foutMapping_user,foutMapping_steps):
        """
            user.csv -> favorite.csv

            row user correct
            int str int=1
        :param fin:
        :param fout:
        :return:
        """
        # fin = 'file/ted/testUser.csv'
        # fout = 'file/ted/testFavorite.csv'
        data = pd.read_table(fin)
        favorite = pd.DataFrame()
        user = data['Anon Student Id'].drop_duplicates()
        user.to_csv(foutMapping_user)
        steps = data['Step Name'].drop_duplicates()
        steps.to_csv(foutMapping_steps)

        favorite['Anon Student Id'] = data['Anon Student Id'].replace(user.values,user.index )
        favorite['Step Name'] = data['Step Name'].replace(steps.values,steps.index )
        favorite['Correct First Attempt'] = data['Correct First Attempt']
        favorite['Row'] = data['Row']

        favorite = favorite[favorite['Correct First Attempt']==1]
        favorite.to_csv(outFavorite, index=False, header=False)

class Recommend(object):
    def __init__(self,fin,in_dir=''):
        self.userItems = dict()  # 用户到物品的倒排表
        self.C = defaultdict(defaultdict)  # 用户与用户共同喜欢物品的个数
        self.N = defaultdict(defaultdict)  # 用户个数
        self.W = defaultdict(defaultdict)  # 相似度矩阵
        self.K = 5  # 选取前k个最相似的物品计算预测相似度
        self.fin = fin
        self.in_dir = in_dir
        self.favorite = []
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
        f = open(os.path.join(self.in_dir,'matrixW.txt'), 'wb')
        pickle.dump(self.W, f)
        f.close()

    def load_matrix_w(self):  # 载入大概需要7.96s
        fW = os.path.join(os.path.join(self.in_dir,'matrixW.txt'))
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
        if len(self.favorite) ==0:
            data = np.loadtxt(self.fin, delimiter=',',dtype=int)  # for test
            self.favorite = data
        else:
            data = self.favorite
        ru = data[data[:, 0] == UserID]  # 用户数据，表示某物品及其兴趣度
        for r in ru:# i表示用户已评价的电影id，pi表示其兴趣度（评分）
            i = r[1]
            pi = r[2]
            # j表示相似度为前K个物品的id，wj表示物品i和物品j的相似度
            numb = -1
            for j, wj in sorted(self.W[str(i)].items(), key=itemgetter(1), reverse=True):
                numb = numb + 1
                if numb==self.K:
                    break
                if int(j) in ru[:,1]:  # 如果用户已经有了物品j，则不再推荐
                    continue
                # rank = dict()
                if j not in rank.keys():
                    rank[j] = 0
                rank[j] += pi * wj
        return rank

class dataPath:
    in_dir = 'file/algebra_2005_2006/test_matrics'
    fin_train = 'file/algebra_2005_2006/algebra_2005_2006_train.txt'

    fin_test = 'file/algebra_2005_2006/algebra_2005_2006_test.txt'  # missing values
    fin_master = 'file/algebra_2005_2006/algebra_2005_2006_master.txt' # validate
    fin_row = 'file/algebra_2005_2006/algebra_2005_2006.txt' # row

    outFavorite = '%s/favorite.csv' % in_dir    # item_user table
    foutMapping_user = '%s/students.csv' % in_dir   # mappping user:str to user:int
    foutMapping_items = '%s/steps.csv' % in_dir # mappping item:str to item:int

    simple_test = '%s/algebra_2005_2006_test_simple.txt'% in_dir
    simple__master = '%s/algebra_2005_2006_master_simple.txt' %in_dir
    simple__train = '%s/algebra_2005_2006_train_simple.txt'%in_dir

    f_src_list = [fin_test,fin_master]
    f_simple_list = [simple_test,simple__master]


def RMSE():
    pass
def doTrain(in_dir,fin, outFavorite, foutMapping_user, foutMapping_items):
    '''
    generate matrix_W
    :return:
    '''
    preD = prepareData()
    preD.createFavorite(fin, outFavorite, foutMapping_user, foutMapping_items)
    recommend = Recommend(outFavorite, in_dir=in_dir)
    recommend.cal_matrix_W()
def train():
    doTrain(dataPath.in_dir, dataPath.fin_train, dataPath.outFavorite, dataPath.foutMapping_user, dataPath.foutMapping_items)
    # simplify()
#     user in test may not in train
def smplifyData(fin,fout):
    # fin = dataPath.fin_master
    data = pd.read_table(fin)
    user = pd.read_csv(dataPath.foutMapping_user, index_col=0, header=None)
    item = pd.read_csv(dataPath.foutMapping_items, index_col=0, header=None)

    for x in data['Step Name']:
        if x not in user.values:
            user.add(x)
    result_data = pd.DataFrame()
    result_data['studentID'] = data['Anon Student Id'].replace(user.values, user.index)
    result_data['stepName'] = data['Step Name'].replace(item.values, item.index)
    result_data['realCis'] = data['Correct First Attempt']
    result_data['predictCis'] = [0] * len(data)

    result_data.to_csv(fout,sep='\t',index=False,header='info')
def simplify():
    for idx in range(len(dataPath.f_src_list)):
        smplifyData(dataPath.f_src_list[idx], dataPath.f_simple_list[idx])
def evaluate():
    pass
def precision(train, test, W, N,rank):
    hit = 0                              # hit is the number of tu & ru
    all = 0                              # all is the number of ru
    for user in train.keys():
        if user not in test:
            continue
        tu = test[user].keys()
        for item, pui in rank.items():
            if item in tu:
                hit += 1
        all += len(rank)
        return hit / (all * 1.0)
def predict():
    recommend = Recommend(dataPath.outFavorite, in_dir=dataPath.in_dir)
    data = pd.read_table(dataPath.simple__master)
    user = data['studentID'].drop_duplicates()
    mylist = []
    for x in user.values:
        rank = recommend.recommend(x)
        mylist.append(rank)
    print(mylist)
    with open(os.path.join(dataPath.in_dir,'ranks.dict'),'w') as fo:
        fo.write(str(mylist))
        fo.flush()

if __name__ == '__main__':
    # in_dir = 'file/ted/'
    # fin = '%s/user.csv'%in_dir
    '''
    test
    '''
    # in_dir = 'file/algebra_2005_2006/test_matrics'
    # fin = 'file/algebra_2005_2006/algebra_2005_2006_master.txt'
    # fin_row = 'file/algebra_2005_2006/algebra_2005_2006.txt'
    # outFavorite = '%s/favorite.csv'%in_dir
    # foutMapping_user = '%s/students.csv'%in_dir
    # foutMapping_steps = '%s/steps.csv'%in_dir
    # if not os.path.exists(in_dir):os.mkdir(in_dir)
    # preD = prepareData()
    # preD.createFavorite(fin,outFavorite,foutMapping_user,foutMapping_steps)
    # recommend = Recommend(outFavorite,in_dir=in_dir)
    # recommend.cal_matrix_W()
    # rank = recommend.recommend(3)
    #
    # recommend = Recommend(outFavorite,in_dir=in_dir)
    # rank = recommend.recommend(3)

    print('training...')
    train()
    print('evaluating')
    evaluate()
    print('predict...')
    # predict()
    print('all down!')
    # print('all down!',rank)
    print()
