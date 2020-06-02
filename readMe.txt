## 基于物品的协同推荐算法 userItem

ItemCF0315.py
    for group len
    example:
        recommend = Recommend()
        # recommend.cal_matrix_W()
        rank = recommend.recommend(1)
ItemCF0327.py
    for ted
    example:
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
loadData.py
    supprot file