import csv
from pretreat import *
import random
import numpy as np

'''
计算两个向量的点积
'''
def vec_dot(V1,V2):
    ans=0.0
    for i in range(len(V1)):
        ans+=V1[i]*V2[i]
    return ans


'''
计算两个向量的余弦相似度
'''
def sim_cal(V1,V2):
    return vec_dot(V1,V2)/((vec_dot(V1,V1)**0.5) * (vec_dot(V2,V2)**0.5))


   
''' u_id1,u_id2为两个用户的id
    mat为user-item矩阵
    avg为user的评分平均值
'''
def user_sim(u_id1,u_id2,mat,avg):
    n_item = len(mat[0])
    V1=[]
    V2=[]
    for item in range(n_item):
        if mat[u_id1][item]!=0 and mat[u_id2][item]!=0:
            V1.append(mat[u_id1][item]-avg[u_id1])
            V2.append(mat[u_id2][item]-avg[u_id2])
    if len(V1) <=1:
        return 0.0
    print(V1,V2)
    return sim_cal(V1,V2)


'''原参数mat,avg'''
def get_sim_mat():   
    '''生成代码：写入了sim.csv文件中
    sim_file = csv.writer(open('sim.csv','w',encoding='big5',newline=""))
    n_user = 610
    sim_mat = np.zeros((n_user+1,n_user+1))
    for id1 in range(1,n_user+1):
        for id2 in range(id1+1,n_user+1):
            sim_mat[id1][id2]=sim_mat[id2][id1]=user_sim(id1,id2,mat,avg)
        sim_file.writerow(sim_mat[id1])
    '''
    sim_file = csv.reader(open('sim.csv','r',encoding='big5'))
    sim_mat = []
    for row in sim_file:
        tup = []
        for i in range(len(row)):
            tup.append((float(row[i]),i))
        sim_mat.append(tup)
    
    return sim_mat

def sort_tup():
    return


def predict(u_id,m_id,K,sim,mat,avg):
    sum = rat = 0.0
    for tup in sim:
        if K<=0 or tup[0]<=0:
            break
        id = tup[1]
        if mat[id][m_id]==0:
            continue
        sum+= tup[0]   #所有K个邻居的相似度之和
        rat+= tup[0]*(mat[id][m_id]-avg[id]) #所有K个邻居的相似度与相对评分的乘积
        K-=1
    if sum!=0:
        rat /= sum
    else:
        rat = 0.0
        
    return rat+avg[u_id]
    


if __name__ == "__main__":
    id2name,name2id = get_movie_index()
    mat = array_gen(name2id)
    avg = average_rating(mat)
    sim = get_sim_mat()  #按照相似度降序排序后的2元组(sim,id)
    for row in sim:
        row.sort()
        row.reverse()
    test_set = get_test(name2id)
    '''
    prediction = predict(133,124,4,sim[133],mat,avg)
    print(prediction)
'''
    RMSE= 0.0
    MAE = 0.0
    num = 0
    for rec in test_set:
        
        u_id = rec[0]
        m_id = name2id[rec[1]]
        ground_truth = rec[2]
        prediction = predict(u_id,m_id,6,sim[u_id],mat,avg)
       # print(ground_truth,prediction)
        RMSE += (ground_truth-prediction)**2
        MAE  += abs(ground_truth-prediction)
        #print(u_id,m_id,RMSE)
        
    RMSE/=len(test_set)
    RMSE = RMSE**0.5
    MAE /=len(test_set)
    print('RMSE:',RMSE)
    print('MAE:',MAE)
    
    
    
    
    


