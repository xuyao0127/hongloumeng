# -*- coding: utf-8 -*-

import tools
import codecs
import shutil
import numpy as np
from sklearn import feature_extraction  
from sklearn.feature_extraction.text import TfidfTransformer  
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering

def SKLearn(Text):
    #print()
    #将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
    vectorizer = CountVectorizer()

    #该类会统计每个词语的tf-idf权值
    transformer = TfidfTransformer()

    #第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵
    tfidf = transformer.fit_transform(vectorizer.fit_transform(Text))
    print(tfidf)

    #获取词袋模型中的所有词语  
    word = vectorizer.get_feature_names()
    #print(type(word))
    print(word[:10])

    #将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重
    weight = tfidf.toarray()
    print(len(weight),len(weight[0]))
    
    print(len(word))
    print(weight)
    #print(set(weight.tolist()))
    temp=weight.tolist()
    count=0
    for i in range(10):
        for j in range(100):
            if temp[i][j]!=0:
                count=count+1
                print(word[j])
                #print(temp[i][j])
    print(count)
    
    print('Start Kmeans:')
    clf = KMeans(n_clusters=2)
    s = clf.fit(weight)
    print(s)

    #10个中心点
    print(clf.cluster_centers_)
    print(len(clf.cluster_centers_),len(clf.cluster_centers_[0]))
    
    #每个样本所属的簇
    print(clf.labels_)
    i = 1
    F_Result=[0,0,0,0]
    while i <= len(clf.labels_):
        if i<=80:
            if clf.labels_[i-1]==0:
                F_Result[0]=F_Result[0]+1
            else:
                F_Result[1]=F_Result[1]+1
        else:
            if clf.labels_[i-1]==0:
                F_Result[2]=F_Result[2]+1
            else:
                F_Result[3]=F_Result[3]+1
                
        print(i, clf.labels_[i-1])
        i = i + 1
    
    print("Chapter 1-80: "+str(F_Result[0]/80.0)+"Probability in Class 0, "+str(F_Result[1]/80.0)+"Probability in Class 1")
    print("Chapter 80-120: "+str(F_Result[2]/40.0)+"Probability in Class 0, "+str(F_Result[3]/40.0)+"Probability in Class 1")
    
    #用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数
    print(clf.inertia_)
    
    #Hierach
    ward = AgglomerativeClustering(n_clusters=2, linkage='average').fit(weight)
    label = ward.labels_
    print(len(label))
    i = 1
    F_Result=[0,0,0,0]
    while i <= len(label):
        if i<=80:
            if label[i-1]==0:
                F_Result[0]=F_Result[0]+1
            else:
                F_Result[1]=F_Result[1]+1
        else:
            if label[i-1]==0:
                F_Result[2]=F_Result[2]+1
            else:
                F_Result[3]=F_Result[3]+1
                
        print(i, label[i-1])
        i = i + 1
    
    print("Chapter 1-80: "+str(F_Result[0]/80.0)+"Probability in Class 0, "+str(F_Result[1]/80.0)+"Probability in Class 1")
    print("Chapter 80-120: "+str(F_Result[2]/40.0)+"Probability in Class 0, "+str(F_Result[3]/40.0)+"Probability in Class 1")
    
    
    
if __name__ == '__main__':
    n = tools.Novel('hongloumeng.txt')
    #print('Number of chapters: ', n.num_chapters)
    first_80 = [' '.join(chapter.word_bracket) for chapter in n.chapters[:80]]
    allChapter = [' '.join(chapter.word_bracket) for chapter in n.chapters]
    #print(first_80[0])
    '''
    print('Content of first chapter')
    print(c.text)
    print('Number of unique words in first chapter: ', c.num_words)
    print('words braket', c.word_bracket)
    '''
    SKLearn(allChapter)