# 导入相关库
'''
seg1 = jieba.cut(data, cut_all=True)
print('全模式：', ' '.join(seg1))

seg2 = jieba.cut("好好学学python，有用。", cut_all=False)
print("精确模式（也是默认模式）：", ' '.join(seg2))
seg3 = jieba.cut_for_search("好好学学python，有用。")
print("搜索引擎模式：", ' '.join(seg3))
print("\n")
'''

import os, codecs
import jieba
import csv

f = open("data.txt", "r")
datatemp = f.readlines()
counts={}
data = datatemp[0]

# 分词统计
seg_list = jieba.cut(data)
counts = {}
for word in seg_list:           
    counts[word] = counts.get(word,0) + 1
# 删除停用词
stopword=[' ']
with open("./stopword.csv",newline = '',encoding = 'utf-8')  as f:
    reader = csv.reader(f)
    for row in reader:
        for i in row:
            stopword.append(i)
for i in stopword:
    if counts.get(i, 0)!=0:
        counts.pop(i)
items = list(counts.items())
items.sort(key=lambda x:x[1], reverse=True) 
for i in items:
    print ("{0:<10}{1:>5}".format(i[0], i[1]))