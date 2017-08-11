# -*- coding: utf-8 -*-
import bayes
import numpy
from numpy import*
from sklearn import datasets
from sklearn.cross_validation import train_test_split
from sklearn.externals import joblib
import pickle
from sklearn import svm
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.neighbors import KNeighborsClassifier
def loadDataSet(fileName,isGetKey,length):
    dataMat = []; labelMat = []
    # fileName = 'book-cf/'+fileName
    fr = open(fileName)
    arrayOLines = fr.readlines()
    if isGetKey ==0:
        for i in range(length):
            lineArr = arrayOLines[i].strip().split(';')
            lineArr[3] = lineArr[3].strip().split(',')
            dataMat.append(lineArr[3][:-1])
            # 这里是挑出漏注释的选项
            if lineArr[2]=='':
                print i
            else:lineArr[2] = int(lineArr[2])
            labelMat.append(lineArr[2])
    else:
        for i in range(length):
            lineArr = arrayOLines[i].strip().split(';')
            lineArr[3] = lineArr[3].strip().split(',')
            arr=[]
            num = len(lineArr[3])
            for j in range(num-1):
                lineArr[3][j] = lineArr[3][j].strip().split(':')
                arr.append(lineArr[3][j][0])
            dataMat.append(arr)
            # 这里是挑出漏注释的选项
            if lineArr[2]=='':
                print i
            else:lineArr[2] = int(lineArr[2])
            labelMat.append(lineArr[2])
    return dataMat,labelMat,length
def setOfWords2Vec(vocabList, inputSet):
    words2Vec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            words2Vec[vocabList.index(word)] = 1
        else: pass
    return words2Vec


def createVocabList(dataset):
    vocabList = set([])   #提取list中元素唯一值到vocab中
    for item in dataset:
        vocabList = vocabList | set(item)    #创建两个集合的并集
    return list(vocabList)

def loadDataSetT():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,2,1,0,1]    #1 is abusive, 0 not
    return postingList,classVec
def testMyNB0():
    list0Posts, listClasses = loadDataSetT()
    myVocabList = createVocabList(list0Posts)
    print myVocabList
    trainMat = []
    for postinDoc in list0Posts:
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
    targetArr = array([0,1,2])
    print trainMat[0]
    pV, pAb= bayes.mytrainNB0(trainMat,listClasses,targetArr)
    print pAb
    print "\n"
    print pV
    testEntry = ['stupid', 'garbage']
    # testEntry = ['love', 'my', 'dalmation']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print testEntry,'classified as: ',bayes.myclassifyNB(thisDoc,pV,pAb,targetArr)

# testMyNB0()

# 对Booklist2进行训练并交叉验证分类准确率
def mybayesBookClassify():
    list0Posts, listClasses, length= loadDataSet('Booklist2.txt',0,5500)    
    # list0Posts, listClasses, length= loadDataSet('Booklist1.txt',1,2500)
    myVocabList = createVocabList(list0Posts)
    trainMat = []
    for postinDoc in list0Posts:
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
    targetArr = array([0,1,2,3,4])
    digits = datasets.load_digits()
    digits.data,digits.target = trainMat,listClasses
    length = len(digits.data)
    nsplit = int(length/5)
    train_data,test_data,train_target,test_target = train_test_split(digits.data, digits.target)
    pV, pAb= bayes.mytrainNB0(train_data,train_target,targetArr)
    # print pAb
    # print "\n"
    # print pV
    testEntry = test_data
    testLen = len(testEntry)
    testResult = zeros(testLen)
    realResult = test_target
    errorCount = 0
    totalError = 0
    for i in range(testLen):
        # thisDoc = array(setOfWords2Vec(myVocabList, testEntry[i]))
        testResult[i] = bayes.myclassifyNB(testEntry[i],pV,pAb,targetArr)
        if testResult[i] != realResult[i]:
            errorCount +=1
    totalError += float(errorCount)/testLen
    totalRight = 1 - totalError
    print "number of testing:",length,"errorCount :",errorCount,"total right rate",totalRight
# '''
# mybayesBookClassify()
# '''

# scikit-learn includes several variants of thisclassifier; the one most suitable for word counts is the multinomial variant:

def dumpTree(tree, filename):
    with open(filename,'wb') as fp:
        pickle.dump(tree, fp)       

def loadTree(filename):
    with open(filename,'rb') as fp:
        return pickle.load(fp)
def classifytest(list0Posts, listClasses, length):
    digits = datasets.load_digits()
    myVocabList = createVocabList(list0Posts)
    trainMat = []
    for postinDoc in list0Posts:
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
    digits.data,digits.target = trainMat,listClasses
    train_data,test_data,train_target,test_target = train_test_split(digits.data, digits.target)
    # '''
    # bayes方法实现分类
    # clf = MultinomialNB().fit(train_data,train_target)
    # clf = BernoulliNB().fit(train_data,train_target)
    #  
    clf = MultinomialNB().fit(digits.data,digits.target)

    # 实现svm分类
    # clf = svm.SVC(gamma=0.001, C=100.)    #建立预测器
    # clf.fit(train_data,train_target)

    joblib.dump(clf, 'modelpersitence/boocf_model.pkl')
    clf_load = joblib.load('modelpersitence/boocf_model.pkl')
    # '''

    '''
    #knn分类
    clf=KNeighborsClassifier(n_neighbors=3)
    clf.fit(train_data,train_target)
    dumpTree(clf, 'knntest_booklist2.pkl')
    clf_load = loadTree('knntest_booklist2.pkl')
    # '''
    testResult=clf_load.predict(test_data)
    realResult = test_target
    testLen = len(testResult)
    errorCount = 0
    totalError = 0
    for i in range(len(testResult)):
        if testResult[i] != realResult[i]:
            errorCount +=1
    totalError += float(errorCount)/testLen
    totalRight = 1 - totalError
    print "number of training:",testLen,"errorCount :",errorCount,"total right rate",totalRight

# 测试分类器
list0Posts, listClasses, length= loadDataSet('Booklist2.txt',0,5500)
classifytest(list0Posts, listClasses, length)