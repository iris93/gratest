# -*- coding: utf-8 -*-
from numpy import *


# 这里我进行一点修改,增加目标值lists来告诉训练器需要分为几类.如此看来还是svm简单一点.
# 但是svm需要解决如何输入的问题.
targetArr = array([0,1,2,3,4,5,6,7])
targetArr = array([0,1])

def mytrainNB0(trainMatrix,trainCategory,targetArr):
    numTrainDocs = len(trainMatrix)
    # print numTrainDocs
    numWords = len(trainMatrix[0])
    # print numWords
    numTargets = len(targetArr)
    # print numTargets
    nAbusive = zeros(numTargets)   #生成包含numTargets个元素的array
    # print nAbusive
    for item in trainCategory:
        nAbusive[targetArr.tolist().index(item)] +=1     #对各个类别分别统计出现的次数
    pAbusive = nAbusive/float(numTrainDocs)   #对于各个类别类别在所有文档中的概率.
    # print pAbusive
    pNum = ones((numTargets,numWords))      #change to ones() 
    pVect = zeros((numTargets,numWords))
    pDenom = 1.0*numTargets*ones(numTargets)                     #change to 2.0
    for i in range(numTrainDocs):
        for j in range(numTargets):
            if trainCategory[i] == targetArr[j]:
                pNum[j] += trainMatrix[i]                #对每个类别分别统计每个词向量出现的次数
                pDenom[j] += sum(trainMatrix[i])      #总的词向量出现的次数
    # print pNum,pDenom
    for k in range(numTargets):
        pVect[k] = log(pNum[k]/pDenom[k])          #一个类别*词向量的array,存放每个类别每个词的词频
    return pVect,pAbusive
# 经过测试,ok
def myclassifyNB(vec2Classify, pVec, pAbusive,targetArr):
    numTargets = len(targetArr)
    p = zeros(numTargets)
    for i in range(numTargets):
        p[i] = p[i] + sum(vec2Classify * pVec[i]) + log(pAbusive[i])
    pmax = max(p)
    return targetArr[p.tolist().index(pmax)]

def textParse(bigString):    #input is big string, #output is word list
    import re
    listOfTokens = re.split(r'\W*', bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) > 2] 
    
def spamTest():
    docList=[]; classList = []; fullText =[]
    for i in range(1,26):
        wordList = textParse(open('email/spam/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(open('email/ham/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)#create vocabulary
    trainingSet = range(50); testSet=[]           #create test set
    for i in range(10):
        randIndex = int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])  
    trainMat=[]; trainClasses = []
    for docIndex in trainingSet:#train the classifier (get probs) trainNB0
        trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
    errorCount = 0
    for docIndex in testSet:        #classify the remaining items
        wordVector = bagOfWords2VecMN(vocabList, docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
            errorCount += 1
            print "classification error",docList[docIndex]
    print 'the error rate is: ',float(errorCount)/len(testSet)
    #return vocabList,fullText

def calcMostFreq(vocabList,fullText):
    import operator
    freqDict = {}
    for token in vocabList:
        freqDict[token]=fullText.count(token)
    sortedFreq = sorted(freqDict.iteritems(), key=operator.itemgetter(1), reverse=True) 
    return sortedFreq[:30]       

def localWords(feed1,feed0):
    import feedparser
    docList=[]; classList = []; fullText =[]
    minLen = min(len(feed1['entries']),len(feed0['entries']))
    for i in range(minLen):
        wordList = textParse(feed1['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1) #NY is class 1
        wordList = textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)#create vocabulary
    top30Words = calcMostFreq(vocabList,fullText)   #remove top 30 words
    for pairW in top30Words:
        if pairW[0] in vocabList: vocabList.remove(pairW[0])
    trainingSet = range(2*minLen); testSet=[]           #create test set
    for i in range(20):
        randIndex = int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])  
    trainMat=[]; trainClasses = []
    for docIndex in trainingSet:#train the classifier (get probs) trainNB0
        trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
    errorCount = 0
    for docIndex in testSet:        #classify the remaining items
        wordVector = bagOfWords2VecMN(vocabList, docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
            errorCount += 1
    print 'the error rate is: ',float(errorCount)/len(testSet)
    return vocabList,p0V,p1V

def getTopWords(ny,sf):
    import operator
    vocabList,p0V,p1V=localWords(ny,sf)
    topNY=[]; topSF=[]
    for i in range(len(p0V)):
        if p0V[i] > -6.0 : topSF.append((vocabList[i],p0V[i]))
        if p1V[i] > -6.0 : topNY.append((vocabList[i],p1V[i]))
    sortedSF = sorted(topSF, key=lambda pair: pair[1], reverse=True)
    print "SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**"
    for item in sortedSF:
        print item[0]
    sortedNY = sorted(topNY, key=lambda pair: pair[1], reverse=True)
    print "NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**"
    for item in sortedNY:
        print item[0]
