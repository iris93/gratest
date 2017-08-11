# -*- coding:utf-8 -*-
# 引入分词模块
import sys;
reload(sys);
sys.setdefaultencoding('utf8');
import pynlpir
# 引入分类模块
# scikit-learn includes several variants of thisclassifier; the one most suitable for word counts is the multinomial variant:
from sklearn import datasets
from sklearn.externals import joblib

from numpy import *
from django.shortcuts import render
from django.conf import settings  
# from django.template import loader, Context,RequestContext
# Create your views here.
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response
from django.db import connection
from models import *
from django.db.models import Avg, Max, Min, Count, Q
from django.contrib.admin.models import LogEntry
from django.views.decorators.csrf import csrf_exempt
import time, datetime, re, os
from django.contrib.auth.decorators import login_required
try:
    import json
except:
    import simplejson as json  
from django.http import HttpResponse  
# from mychat import mychat
import  MySQLdb

# def home(request):
#     return render(request,'mysite.html')

#Transform python data to json data,and response to method with data for login
def response_to_app(data,method):
    response = HttpResponse(data)
    response['Access-Control-Allow-Origin']= "*"
    response['Access-Control-Allow-Methods'] = method 
    response['Access-Control-Allow-Headers'] = "x-requested-with,content-type" 
    return response

#Transform data to json and response to app request
def response_with_json(data,method):
    jsondata  = json.dumps(data,separators = (',',':'))
    response  = HttpResponse('%s' % (jsondata))
    response['Access-Control-Allow-Origin']= "*"
    response['Access-Control-Allow-Methods'] = method 
    response['Access-Control-Allow-Headers'] = "x-requested-with,content-type" 
    return response

@csrf_exempt
def testLogin(request):
    # print "============running in login============"
    if request.method == 'GET':    
        data = "It's ok!"
        response = response_to_app(data,request.method)
        return response     

    elif request.method == 'POST': 
        data = {}
        try:
            body_str = request.body
            body_dict = json.loads(body_str)
            user = body_dict['username']
            pswd = body_dict['password']
            # print user,pswd
        except:
            response  = response_to_app(data,request.method)
            return response        
        users  = User.objects.filter(username = user)
        # users  = User.objects.get_or_create(username = user)
        # print users
        if len(users) > 0:
            u = User.objects.get(username = users[0].username)
            # print u.username
            # print u.password
            # 可以在这里给新录入用户添加密码
            # u.set_password(pswd)
            # u.save()
            flag = u.check_password(pswd)
            # print flag
            if flag == True:        
                ret = "success"
                user0 = authenticate(username=user, password=pswd)  #nessary for check user
                login(request, user0)
                token = users[0].id
                message = u"欢迎登录系统！"
                user_type = users[0].username
                # print "user_type",user_type
                if user_type == 'admin':
                    usertype = 0
                else:
                    usertype = 1
            else:                
                ret = "fail"
                token = 'fail'
                message =  u"对不起，你输入的密码有错，请重新输入。。。"
        else:
            ret = "fail"
            token = ''
            message = u"对不起，你输入的用户名有错，请重新输入。。。"
        schools_name_list = []
        schools_name_dic = {}
        if ret == "success":
            users = GROUP.objects.filter(username = request.user)
            data["userschool"] = users[0].user_school
            print  "usertype",usertype
            if usertype == 1:
                schools_name_dic["name"] = users[0].user_school
                schools_name_list.append(schools_name_dic)
            else:
                users = GROUP.objects.all()
                for j in range(len(users)):
                    if users[j].user_school != 'admin':
                        schools_name_dic = {}
                        schools_name_dic["name"] = users[j].user_school
                        # print users[j].user_school
                        schools_name_list.append(schools_name_dic)
                    else:pass
            data["schools"] = schools_name_list
            # print data["schools"]
        data['token']    = token 
        data["mystatus"] = ret
        data["message"]  = message
        # print "data is:",data
        response = response_with_json(data,request.method)     
        return response
    else: 
        data = "other method"
        response  = response_to_app(data,request.method)
        return response
srting2strip = "学-:《》#.de\" \/()·de的之,，。-『』册·力和及与1:第2版、珍藏版最第4一Ⅲ=24第二版第三版第四版第五版"

def booksegment(string2split,srting2strip):
    pynlpir.open()
    length = len(string2split)
    string2cf = []
    seg= pynlpir.segment(string2split, pos_tagging=False)
    for item in seg:
        if str(item) in srting2strip:pass
        else:
            string2cf.append(str(item))
            # print item
    pynlpir.close()
    return string2cf

def loadDataSet(fileName,isGetKey,length):
    dataMat = []; labelMat = []
    fileName = 'book-cf/'+fileName
    fr = open(fileName)
    arrayOLines = fr.readlines()
    if isGetKey ==0:
        for i in range(length):
            lineArr = arrayOLines[i].strip().split(';')
            lineArr[3] = lineArr[3].strip().split(',')
            dataMat.append(lineArr[3][:-1])
            # 这里是挑出漏注释的选项
            if lineArr[2]=='':
                pass
                # print i
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
                pass
                # print i
            else:lineArr[2] = int(lineArr[2])
            labelMat.append(lineArr[2])
    return dataMat,labelMat,length
# 创建不重复词集
def createVocabList(dataset):
    vocabList = set([])   #提取list中元素唯一值到vocab中
    for item in dataset:
        vocabList = vocabList | set(item)    #创建两个集合的并集
    return list(vocabList)
# 将书籍名称转化为向量
def setOfWords2Vec(vocabList, inputSet):
    words2Vec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            words2Vec[vocabList.index(word)] = 1
        else: pass
    return words2Vec


def bookclassify(testData):
    digits = datasets.load_digits()
    # 加载词集以便构建不重复词列表
    list0Posts, listClasses, length= loadDataSet('Booklist2.txt',0,5500)
    myVocabList = createVocabList(list0Posts)
# bayes模型加载
    clf_load = joblib.load('book-cf/modelpersitence/boocf_model.pkl')
    # '''
    testMat = []
    testMat.append(setOfWords2Vec(myVocabList, testData))
    digits.data = testMat
    testResult=clf_load.predict(digits.data)
    return testResult
def checkstudent(student_id):
    lendbooks=LEND_INFO.objects.filter(STU_ID = student_id)
    bookcount = len(lendbooks)
    stuinfo_lendbooks = []
    stuinfo_bookscount = [[0,0,0,0,0]]
    # print bookcount
    if len(lendbooks) > 0 :
        # data_dty = 2016
        # print data_dty
        # data_dtm = (data_dty-2015)*12+1-6
        # print data_dtm
        for i in range(bookcount):
            lend_year = int(lendbooks[i].LEND_DATE[0:4])
            # print lend_year
            # print int(lendbooks[i].LEND_DATE[5:7])
            # lend_month = (lend_year-2015)*12+int(lendbooks[i].LEND_DATE[5:7])
            if lend_year >2014:
                if len(lendbooks[i].M_TITLE) > 0 :
                    # if lendbooks[i].M_CLASS == None:
                    if 1==1:
                        lendbooksseg = booksegment(lendbooks[i].M_TITLE,srting2strip)
                        bookclass = bookclassify(lendbooksseg)
                        # print stuinfo_bookscount
                        lendbooks[i].M_CLASS = bookclass[0]
                        lendbooks[i].save()
                        # print lendbooks[i].M_TITLE
                        stuinfo_lendbooks.append([lendbooks[i].M_TITLE,bookclass[0]])
                    else:
                        # print lendbooks[i].M_CLASS
                        stuinfo_lendbooks.append([lendbooks[i].M_TITLE,lendbooks[i].M_CLASS])
                else:pass
                if lendbooks[i].M_CLASS == 0:stuinfo_bookscount[0][0] +=1
                elif lendbooks[i].M_CLASS == 1:stuinfo_bookscount[0][1] +=1
                elif lendbooks[i].M_CLASS == 2:stuinfo_bookscount[0][2] +=1
                elif lendbooks[i].M_CLASS == 3:stuinfo_bookscount[0][3] +=1
                elif lendbooks[i].M_CLASS == 4:stuinfo_bookscount[0][4] +=1
                else:pass
            else:pass
    else :pass
    return stuinfo_lendbooks,stuinfo_bookscount

def regressionrating(ratingvector):
    digits = datasets.load_digits()
    digits.data = ratingvector
    model_load = joblib.load('ratingmodel/models/regressiontest/regressiontest.pkl')
    ratingResult=model_load.predict(digits.data)
    return ratingResult[0]+4

# 通过学生的学号以及读书信息给学生产生ratingvector并调用regressionrating函数进行打分
def rating(stu_id,stuinfo_bookscount):
    student = STU_INFO.objects.get(STU_ID=stu_id)
    ratingvector = []
    if student.score ==None:
    # if 1 ==1:
        if student.STU_TYPE == '本科':
            stugrade =16 - int(str(stu_id)[0:2])
        elif student.STU_TYPE == '硕士':
            stugrade =16 - int(str(stu_id)[0:2]) + 5
        # print stugrade
        if student.STU_SEX == '男':
            stusex = 1
        else:stusex = 2
        if student.INST_CH =='艺术与传媒学院':
            majortype = 0
        else :majortype = 1;
        # print stusex
        ratingvector.append([stusex,stugrade,majortype,stuinfo_bookscount[0][0],stuinfo_bookscount[0][1],stuinfo_bookscount[0][2],stuinfo_bookscount[0][3],stuinfo_bookscount[0][4]])
        student.score = regressionrating(ratingvector)
        student.save()
    else:pass
    # print student.score
    if int(str(student.score)[0:2])>72:
        student_level = '重度抑郁'
    elif int(str(student.score)[0:2])>62:
        student_level = '中度抑郁'
    elif int(str(student.score)[0:2])>50:
        student_level = '轻度抑郁'
    else:
        student_level = '无抑郁'
    return student.score,student_level

def get_student_info(request):
    # print "============running in get_locat============"  
    if request.method == 'GET': 
        # for key in request.GET:
        #     print key,request.GET[key]
        # user_flag = check_user(request)
        # if user_flag == False:
        #     return response_to_app([],request.method)
        
        try:        
            schoolname = request.GET.get("schoolname") 
            # print schoolname
        except:
            response = response_with_json({},request.method)
            return response #response nothing but without any server bug
        data = {}           #response data
        grade= request.GET.get("subgrade") 
        studenttype = request.GET.get("studenttype") 
        number = request.GET.get("number") 
        # print number
        # print studenttype
        # 这一段提取学生年级
        '''
        stusetgra=[]
        stusetgra = STU_INFO.objects.all()
        setgralength = len(stusetgra)
        for i in range(setgralength):
            gra = str(stusetgra[i].STU_ID)[0:2]
            stusetgra[i].STU_GRA=gra
            stusetgra[i].STU_ID=stusetgra[i].STU_ID*911
            stusetgra[i].save()
            print 'stu_id',stusetgra[i].STU_ID,stusetgra[i].STU_GRA
        stusetid=[]
        stusetid = LEND_INFO.objects.all()
        for j in range(len(stusetid)):
            stusetid[j].STU_ID = stusetid[j].STU_ID*911
            stusetid[j].save()
            print 'stu_id',stusetid[j].STU_ID
            # '''
        stu = []
        stu = STU_INFO.objects.filter(INST_CH=schoolname).filter(STU_TYPE=studenttype).filter(STU_GRA=grade)
        stuinfo_list = []
        stu_length = len(stu)
        N = 11
        number = int(number)
        start_index = number*N
        end_index = (number+1)*N
        if end_index<stu_length:
            stu = stu[start_index:end_index]
        elif end_index<(stu_length)+N:
            stu = stu[start_index:]
        else:
            stu = []
        # print stu[0].STU_TYPE
        for i in range(len(stu)):
            stuinfo_dic = {}
            stuinfo_dic["student_id"] =stu[i].STU_ID
            stuinfo_lendbooks,stuinfo_bookscount= checkstudent(stu[i].STU_ID)
            # print  stuinfo_bookscount
            stuinfo_dic["student_lendbooks"] = stuinfo_lendbooks
            stuinfo_dic["student_bookscount"] = stuinfo_bookscount
            student_score,student_level = rating(stu[i].STU_ID,stuinfo_bookscount)
            stuinfo_dic["student_score"] = student_score
            stuinfo_dic["student_level"] = student_level
            stuinfo_list.append(stuinfo_dic)
        data["students"] = stuinfo_list
        response = response_with_json(data,request.method)
        # print data
        return response
    elif request.method == 'POST': 
        data = "post method"       
        response    = response_with_json(data,request.method)
        return response
    else:
        data = "other method"
        response    = response_with_json(data,request.method)
        return response

def search(request):
    # print "============running in get_locat============"  
    if request.method == 'GET': 
        # for key in request.GET:
        #     print key,request.GET[key]
        # user_flag = check_user(request)
        # if user_flag == False:
        #     return response_to_app([],request.method)
        try:        
            stu_id = request.GET.get("student_id") 
            # print stu_id
        except:
            response = response_with_json({},request.method)
            return response #response nothing but without any server bug
        data = {}           #response data
        stu = STU_INFO.objects.filter(STU_ID=stu_id)
        stuinfo_list = []
        # print len(stu)
        if len(stu)>0:
            stuinfo_dic = {}
            stuinfo_dic["student_id"] =stu[0].STU_ID
            stuinfo_lendbooks,stuinfo_bookscount= checkstudent(stu[0].STU_ID)
            # print stuinfo_bookscount
            stuinfo_dic["student_lendbooks"] = stuinfo_lendbooks
            stuinfo_dic["student_bookscount"] = stuinfo_bookscount
            student_score,student_level = rating(stu[0].STU_ID,stuinfo_bookscount)
            stuinfo_dic["student_score"] = student_score
            stuinfo_dic["student_level"] = student_level
            stuinfo_list.append(stuinfo_dic)
            data["students"] = stuinfo_list
        else:data["students"] = []
        response = response_with_json(data,request.method)
        # print data
        return response
    elif request.method == 'POST': 
        data = "post method"       
        response    = response_with_json(data,request.method)
        return response
    else:
        data = "other method"
        response    = response_with_json(data,request.method)
        return response
