# -*- coding: utf-8 -*-
import sys;
reload(sys);
sys.setdefaultencoding('utf8');
import pynlpir
'''
测试代码
# pynlpir.open()
# s = 'NLPIR分词系统前身为2000年发布的ICTCLAS词法分析系统，从2009年开 始，为了和以前工作进行大的区隔，并推广NLPIR自然语言处理与信息检索共享平 台，调整命名为NLPIR分词系统。'
# seged = pynlpir.segment(s, pos_tagging=False)
# seged = pynlpir.segment(s, pos_names='child')
# seged2=pynlpir.get_key_words(s, weighted=True)
# print seged
# for item in seged:
#     print item
'''
#下面开始对图书书名进行分词处理。
pynlpir.open()
'''
提取关键词方法
'''
def myseg_get_keywords(filename2w,filename2seg,limitlist):
    dataMat = []; labelMat = [];
    fr = open(filename2w)
    fl=open(filename2seg, 'w')
    limits = open(limitlist)
    arrayLimits = limits.readlines()
    lengthLimits = len(arrayLimits)
    arrayOLines = fr.readlines()
    length = len(arrayOLines)
    for j in range(length):
        flag = 1
        lineArr = arrayOLines[j].strip().split(';')
        for li in range(lengthLimits):
            limitsArr = arrayLimits[li].strip().split(';')
            if str(lineArr[1]) == str(limitsArr[1]):
                flag = 0
        if flag==0:
            pass
        else:
            if len(lineArr)<3:
                pass
            else:
                seg= pynlpir.get_key_words(lineArr[1], weighted=True)
                fl.write(str(j))
                fl.write(";")
                fl.write(str(lineArr[1]))
                fl.write(";")
                fl.write(str(lineArr[2]))
                fl.write(";")
                for item in seg:
                    fl.write(str(item[0]))
                    fl.write(":")
                    fl.write(str(item[1]))
                    fl.write(",")
                fl.write(";\n")
    fl.close()
    pynlpir.close()

'''
# 这里由原  始数据，跳过限制列表的项，压入标签，并进行关键词、权重提取
# 
'''
# myseg_get_keywords('Booklist0.txt','Booklist1.txt','limitlists.txt')


def mysegment(filename2w,filename2seg,srting2strp):
    dataMat = []; labelMat = [];
    fr = open(filename2w)
    fl=open(filename2seg, 'w')
    arrayOLines = fr.readlines()
    length = len(arrayOLines)
    for j in range(length):
        lineArr = arrayOLines[j].strip().split(';')
        if len(lineArr)<3:
            pass
        else:
            fl.write(str(j))
            fl.write(";")
            fl.write(str(lineArr[1]))
            fl.write(";")
            fl.write(str(lineArr[2]))
            fl.write(";")
            seg= pynlpir.segment(lineArr[1], pos_tagging=False)
            for item in seg:
                if str(item) in srting2strp:
                    pass
                else:
                    fl.write(str(item))
                    fl.write(",")
            fl.write(";\n")
    fl.close()
    pynlpir.close()
'''
这里有原始数据，提取标签并进行简单的分类，并实现去停词
'''
srting2strp = "学-:《》#.de\" \/()·de的之,『』册·力和及与1:第2版、珍藏版最第4一Ⅲ=24第二版第三版第四版第五版"
mysegment('Booklist0.txt','Booklist2.txt',srting2strp)
