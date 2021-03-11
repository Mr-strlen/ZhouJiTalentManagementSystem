# 导入相关库
import jieba
f = open("data.txt", "r")
datatemp = f.readlines()
f.close()
data = datatemp[0]

seg1 = jieba.cut(data, cut_all=True)
print('全模式：', ' '.join(seg1))
'''
seg2 = jieba.cut("好好学学python，有用。", cut_all=False)
print("精确模式（也是默认模式）：", ' '.join(seg2))
seg3 = jieba.cut_for_search("好好学学python，有用。")
print("搜索引擎模式：", ' '.join(seg3))
print("\n")
'''