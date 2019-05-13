import csv
import random

raw  = open('Dataset/rawdata.csv','r',encoding='big5')
train = open('Dataset/train.csv','w',encoding='big5',newline="")
test = open('Dataset/test.csv','w',encoding='big5',newline="")

file = csv.reader(raw)
train_file = csv.writer(train)
test_file=csv.writer(test)

nrow = 0
for row in file:
    if row != 0:
        rand = random.randint(1,10)
        if rand <= 8:
            train_file.writerow(row)
        else:
            test_file.writerow(row)
    nrow+=1

