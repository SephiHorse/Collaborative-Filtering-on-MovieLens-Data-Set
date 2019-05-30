import csv
import numpy as np

'''
被评分的电影id并不连续，故将之看作电影名，
再按照顺序生成id2name以及name2id的映射表
'''
def get_movie_index():  
    file = csv.reader(open('Dataset/rawdata_sort_by_movieid.csv','r',encoding='big5'))
    nrow = 0
    cur  = 0
    name2id   =[0]*194000
    id2name =[0]*9800

    for row in file:
        if nrow !=0:
            movie = int(row[1])
            if name2id[movie] == 0:
                cur+=1
                name2id[movie]=cur
                id2name[cur]=movie
        nrow+=1
    return id2name,name2id


'''
生成user-item矩阵
'''

def array_gen(name2id):
    n_user = 610    #原始数据共有610个用户
    n_item = 9724   #共评分过9724部电影
    mat = np.zeros((n_user+1,n_item+1))
    train_set = csv.reader(open('Dataset/train.csv','r',encoding='big5'))
    for row in train_set:
        userid  = int(row[0])
        movieid = name2id[int(row[1])]
        mat[userid][movieid]=float(row[2])

    return mat


def get_test(name2id):
    test_set = csv.reader(open('Dataset/test.csv','r',encoding='big5'))
    ret = []
    for row in test_set:
        userid  = int(row[0])
        movieid = name2id[int(row[1])]
        ret.append((userid,movieid,float(row[2])))
    return ret

#得到每个用户的评分平均值
def average_rating(mat):
    ratings = []
    for row in mat:
        sum = 0.0
        cnt = 0
        for rat in row:
            if float(rat)!=0:
                sum+=float(rat)
                cnt+=1
        if sum == 0.0:
            ratings.append(0.0)
        else :
            ratings.append(sum/cnt)
    return ratings

if __name__ == "__main__":
    id2name,name2id = get_movie_index()
    test = get_test(name2id)
    print(test)
    
    

    