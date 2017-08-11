## -*- coding: utf-8 -*-
from numpy import *
def choice2frequency(n):
    m = 0
    if n == 1:m=0
    elif n==2:m=0.5
    elif n ==3: m =1
    elif n ==4: m = 2
    elif n ==5: m = 4
    else:pass
    return m
def load4Model(filename):
    dataMat = []
    labelMat = []
    fr = open(filename)
    arrayOLines = fr.readlines()
    length = len(arrayOLines)
    for i in range(length):
        lineArr = arrayOLines[i].strip().split(';')
        labelMat.append(float(lineArr[0]))
        dataMat.append([int(lineArr[1]),int(lineArr[2]),int(lineArr[3]),choice2frequency(int(lineArr[4])),choice2frequency(int(lineArr[5])),choice2frequency(int(lineArr[6])),choice2frequency(int(lineArr[7])),choice2frequency(int(lineArr[8]))])
    return dataMat,labelMat

'''
# 测试加载函数
dataMat,labelMat = load4Model('questionnaire.txt')
print dataMat[0],labelMat[0]
'''
from sklearn.externals import joblib
from sklearn import datasets
from sklearn.linear_model import LinearRegression
from sklearn.linear_model.logistic import LogisticRegression
def regressiontest(list0Posts, listClasses):
    digits = datasets.load_digits()
    digits.data = list0Posts
    digits.target = listClasses
    length = len(digits.data)
    # 多元线性回归
    # model = LinearRegression()
    model = LogisticRegression()
    model.fit(digits.data,digits.target)
    joblib.dump(model, 'models/regressiontest/regressiontest.pkl')
    model_load = joblib.load('models/regressiontest/regressiontest.pkl')
    testInput = digits.data
    testResult=model_load.predict(testInput)
    realResult = digits.target
    testLen = len(testResult)
    errorCount = 0
    totalError = 0
    for i in range(len(testResult)):
        if fabs(testResult[i] - realResult[i]) > 10:
            errorCount +=1
            # print i+2
    totalError += float(errorCount)/testLen
    totalRight = 1 - totalError
    print "number of training:",length,"errorCount :",errorCount,"total error rate",totalError,"total right rate",totalRight
    print "R-squared:",model.score(testInput,testResult)

# '''
list0Posts, listClasses= load4Model('questionnaire.txt') 
# print list0Posts[0]
regressiontest(list0Posts, listClasses)
# '''
def regressionrating(list0Posts):
    digits = datasets.load_digits()
    digits.data = list0Posts
    model_load = joblib.load('models/regressiontest/regressiontest.pkl')
    ratingResult=model_load.predict(digits.data)
    return ratingResult
result = regressionrating(list0Posts)
# print result
