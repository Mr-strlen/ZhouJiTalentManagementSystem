from flask import Flask,url_for,render_template,redirect,request,session,abort,flash
from flask_sqlalchemy import SQLAlchemy
import random, datetime
import time
import jieba
import csv,math

app = Flask(__name__)

# orm初始化
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://ZhouJiAdmin:ZhouJi123#@47.102.195.43:3306/ZhouJiTalentMS?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

# 企业公司表
class Company(db.Model):
    # 定义表名 ZJTMS_Company
    __tablename__ = "ZJTMS_Company"
    # 定义字段
    Company_Name = db.Column(db.String(20), nullable=False)
    Boss_Id = db.Column(db.String(20), nullable=False, primary_key=True)
    Boss_Name = db.Column(db.String(30), nullable=True)

    def __init__(self, name, boss_id, boss_name):
        self.Company_Name = name
        self.Boss_Id = boss_id
        self.Boss_Name = boss_name

#  管理员表
class Manager_Info(db.Model):
     #定义表名 ZJTMS_Manager_Info
     __tablename__ = "ZJTMS_Manager_Info"
     # 定义字段
     Manager_Id = db.Column(db.String(20),nullable=False, primary_key=True)
     Manager_Mail = db.Column(db.String(50),nullable=False)
     Manager_Pwd=db.Column(db.String(20),nullable=False)
     Manager_Permission=db.Column(db.String(20),nullable=False)

     def __init__(self, name, email, pwd, permission):
         self.Manager_Id = name
         self.Manager_Mail = email
         self.Manager_Pwd = pwd
         self.Manager_Permission = permission

# 员工档案表
class Staff_Info(db.Model):
    # 定义表名
    __tablename__ = "ZJTMS_Staff_Info"
    # 定义字段
    Staff_Name=db.Column(db.String(20),nullable=False)
    Staff_Sex=db.Column(db.String(4),nullable=False)
    Staff_Unit=db.Column(db.String(20),nullable=False)
    Staff_Phone=db.Column(db.String(20),nullable=False)
    Staff_Identify=db.Column(db.String(20),nullable=False,primary_key=True)
    Staff_Duty=db.Column(db.String(20),nullable=True)
    Staff_Years=db.Column(db.Integer,nullable=False)
    Staff_Origin=db.Column(db.String(20),nullable=False)
    Staff_GraduateCollege=db.Column(db.String(20),nullable=False)
    Staff_Major=db.Column(db.String(20),nullable=False)
    Staff_Degree=db.Column(db.String(20),nullable=False)
    Staff_Marrige=db.Column(db.String(20),nullable=False)
    Staff_Politic=db.Column(db.String(20),nullable=False)
    Staff_HistoryUnit=db.Column(db.String(255),nullable=True)

    def __init__(self,name,sex,unit,phone,identify,duty,years,origin,graduateCollege,major,degree,marrige,politic,historyUnit):
        self.Staff_Name = name
        self.Staff_Sex = sex
        self.Staff_Unit = unit
        self.Staff_Phone = phone
        self.Staff_Identify = identify
        self.Staff_Duty = duty
        self.Staff_Years = years
        self.Staff_Origin = origin
        self.Staff_GraduateCollege = graduateCollege
        self.Staff_Major = major
        self.Staff_Degree = degree
        self.Staff_Marrige = marrige
        self.Staff_Politic = politic
        self.Staff_HistoryUnit = historyUnit

#  员工评价表
class Staff_Comment(db.Model):
     #定义表名 ZJTMS_Manager_Info
     __tablename__ = "ZJTMS_Staff_Comment"
     # 定义字段
     Staff_Id = db.Column(db.String(20), nullable=False)
     Manager_Id = db.Column(db.String(20), nullable=False)
     Comments = db.Column(db.Text, nullable=False)
     Comments_Time = db.Column(db.DateTime, nullable=False, primary_key=True)

     def __init__(self, s_id, m_id, comments, time_list):
         self.Staff_Id = s_id
         self.Manager_Id = m_id
         self.Comments = comments
         self.Comments_Time = time_list

# 员工星级评定表
class Staff_Stars(db.Model):
    # 定义表名 ZJTMS_Manager_Info
    __tablename__ = "ZJTMS_Staff_Stars"
    # 定义字段
    Staff_Id = db.Column(db.String(20), nullable=False)
    Manager_Id = db.Column(db.String(20), nullable=False)
    Leadership = db.Column(db.Integer, nullable=False)#领导力
    Creativity = db.Column(db.Integer, nullable=False)#创新性
    Communication = db.Column(db.Integer, nullable=False)#交际能力
    Hardworking = db.Column(db.Integer, nullable=True)#勤奋度
    Efficiency = db.Column(db.Integer, nullable=True)#工作效率
    Comment_Time = db.Column(db.DateTime, nullable=False, primary_key=True)

    def __init__(self, s_id, m_id, L1, C2, C3, H4, E5, time):
        self.Staff_Id = s_id
        self.Manager_Id = m_id
        self.Leadership = L1
        self.Creativity = C2
        self.Communication = C3
        self.Hardworking = H4
        self.Efficiency = E5
        self.Comment_Time = time



def GBK2312():
    temp=random.randint(1,2)
    head = random.randint(0xb0, 0xf7)
    body = random.randint(0xa1, 0xfe)
    val = f'{head:x} {body:x}'
    str = bytes.fromhex(val).decode('gb2312')
    return str


@app.route('/test')
def Test():
    ## 词云生成
    # 对于某一个特定员工 生成他的所有评价文本
    comment = ""
    id = "514985520001005447"
    staff_list = db.session.query(Staff_Comment).filter(Staff_Comment.Staff_Id == id).all()
    for i in staff_list:
        temp = str(i.Comments[0:-1])
        comment = comment + temp[0:-1]
    # 分词统计
    seg_list = jieba.cut(comment)
    counts = {}
    for word in seg_list:
        counts[word] = counts.get(word, 0) + 1
    # 删除停用词
    stopword = [' ']
    with open("./stopword.csv", newline='', encoding='utf-8')  as f:
        reader = csv.reader(f)
        for row in reader:
            for i in row:
                stopword.append(i)

    for i in stopword:
        if counts.get(i, 0) != 0:
            counts.pop(i)

    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)
    # for i in range(0, 20):
        # print(items[i][0], items[i][1])

    # 选一部分词云展示 让每个员工都变得不一样（wink）
    random_list = random.sample(range(0, len(items)-1), 120)
    items_select=[]
    for i in random_list:
        items_select.append(items[i])

    ## 基于词云的五个维度评价分数生成
    Leadership_list = ["领导", "礼貌", "强", "待人", "成功"]
    Creativity_list = ["希望", "学习", "期待", "成功", "很大"]
    Communication_list = ["同事", "集体", "发言", "待人", "活动"]
    Hardworking_list = ["员工", "努力", "工作", "提高", "假期"]
    Efficiency_list = ["配合", "懂事", "听从", "遵守纪律", "纪律"]
    score_list = [0, 0, 0, 0, 0] #基于词云的分数增加
    # wordnum = 0
    for i in items:
        # wordnum = wordnum + i[1] #统计分词总数
        if i[0] in Leadership_list:
            score_list[0] = score_list[0] + i[1]
        if i[0] in Creativity_list:
            score_list[1] = score_list[1] + i[1]
        if i[0] in Communication_list:
            score_list[2] = score_list[2] + i[1]
        if i[0] in Hardworking_list:
            score_list[3] = score_list[3] + i[1]
        if i[0] in Efficiency_list:
            score_list[4] = score_list[4] + i[1]
    #print(score_list)
    for i in range(0,5):
        score_list[i]=pow(3, (score_list[i]/100)) # 3^(i/threshold)
        if score_list[i]>5:
            score_list[i]=5
    #print(score_list)
    #return  render_template("test1.html", wordData=items_select)

    ## 开始计算分数
    score_temp = [0, 0, 0, 0, 0]
    temp=db.session.query(Staff_Stars).filter(Staff_Stars.Staff_Id == id).all()
    if len(temp)>0: # 有hr打分 就计算平均分
        for i in temp:
            score_temp[0] = score_temp[0]+i.Leadership
            score_temp[1] = score_temp[1] + i.Creativity
            score_temp[2] = score_temp[2] + i.Communication
            score_temp[3] = score_temp[3] + i.Hardworking
            score_temp[4] = score_temp[4] + i.Efficiency
        for i in range(0,5):
            score_list[i]=math.floor((score_list[i]+score_temp[i]/len(temp))*10)
    print(score_list)
    return  render_template("test.html", wordData=items_select, score_list=score_list)

# 这是一个分词测试（功能已经被涵盖在test中）
@app.route('/word_frequency')
def WordFrequency():
    # 对于某一个特定员工 生成他的所有评价文本
    comment=""
    id="118673964725630096"
    staff_list = db.session.query(Staff_Comment).filter(Staff_Comment.Staff_Id == "118673964725630096").all()
    for i in staff_list:
        temp=str(i.Comments[0:-1])
        comment = comment + temp[0:-1]
    print(comment)
    with open('data.txt', 'w') as f:
        f.write(comment)  # 将字符串写入文件中
    return 'NLP finished'

# 评语增加 star打分增加
@app.route('/comment')
def comment():
    # 获取所有非COO的manager
    manager_list = db.session.query(Manager_Info).filter(Manager_Info.Manager_Permission == "N").all()
    # 获取所有非HR的员工
    staff_list = db.session.query(Staff_Info).filter(Staff_Info.Staff_Duty != "HR").all()
    end_time = datetime.datetime.now()
    start_time = datetime.datetime.now() + datetime.timedelta(days=-1000)  # 当前时间减去2年

    a1 = tuple(start_time.timetuple()[0:9])  # 设置开始日期时间元组（2020-04-11 16:30:21）
    a2 = tuple(end_time.timetuple()[0:9])  # 设置结束日期时间元组（2020-04-11 16:33:21）

    start = time.mktime(a1)  # 生成开始时间戳
    end = time.mktime(a2)  # 生成结束时间戳
    # 开始挑选幸运观众 添加评论和打分呦
    '''
    # 获取评语
    f = open("PingYu.txt", "rb")
    datatemp = f.readlines()
    f.close()
    data = []
    for i in datatemp:
        data.append(str(i, encoding="utf-8"))
    for comment in data:
        i=random.randint(0, len(manager_list)-1)
        j=random.randint(0, len(staff_list)-1)
        m_id=manager_list[i].Manager_Id
        s_id=staff_list[j].Staff_Identify
        t = random.randint(start, end)  # 在开始和结束时间戳中随机取出一个
        date_touple = time.localtime(t)  # 将时间戳生成时间元组
        date = time.strftime("%Y-%m-%d %H:%M:%S", date_touple)
        print(s_id, m_id, date)
        #staff_comment=Staff_Comment(s_id, m_id, comment, date)
        #db.session.add(staff_comment)
        #db.session.commit()
    '''
    for i in range(0,30):
        i = random.randint(0, len(manager_list) - 1)
        j = random.randint(0, len(staff_list) - 1)
        m_id = manager_list[i].Manager_Id
        s_id = staff_list[j].Staff_Identify
        # 查看记录是否存在
        temp=db.session.query(Staff_Stars).filter(Staff_Stars.Staff_Id == s_id, Staff_Stars.Manager_Id == m_id).all()
        if len(temp)>0:
            continue
        else:
            t = random.randint(start, end)  # 在开始和结束时间戳中随机取出一个
            date_touple = time.localtime(t)  # 将时间戳生成时间元组
            date = time.strftime("%Y-%m-%d %H:%M:%S", date_touple)
            print(s_id, m_id, date)
            L1=random.randint(1,5)
            C2=random.randint(1,5)
            C3=random.randint(1,5)
            H4=random.randint(1,5)
            E5=random.randint(1,5)
            #staff_stars=Staff_Stars(s_id, m_id, L1, C2, C3, H4, E5, date)
            #db.session.add(staff_stars)
            #db.session.commit()
    return "评语 打分增加完毕"


@app.route('/')
def hello_world():
    sex_list=["男","女"]
    unit_list=["Alibaba","Tencent","ByteDance","Baidu","JD","Meituan","FerryTalentMS","DiDi","Kwai"]
    duty_list=["员工","员工","员工","开发","主管","经理","小组长","HR"]
    origin_list=["北京","上海","广州","深圳","杭州","天津","合肥","南京","重庆","成都"]
    graduateCollege_list=["清华大学","厦门大学","南京大学","北京大学","天津大学","浙江大学","复旦大学","兰州大学","四川大学","东南大学","同济大学"]
    major_list=["经济学","哲学","法学","理学","工学","农学"]
    degree_list=["本科","硕士","博士","大专"]
    marrige_list=["已婚","未婚"]
    politic_list=["群众","中共党员","共青团员","民主派人士"]

    for i in range(0, 10):
        temp=random.randint(1,11)
        name=""
        for i in range(random.randint(2, 3)):
            s = GBK2312()
            name = name + s
        sex=sex_list[random.randint(0,1)]
        unit=unit_list[random.randint(0,8)]
        phone=random.randint(10000000000,99999999999)
        identify=random.randint(100000000000000000,999999999999999999)
        duty=duty_list[random.randint(0,7)]
        years=random.randint(19,40)
        origin=origin_list[random.randint(0,9)]
        graduateCollege=graduateCollege_list[random.randint(0,10)]
        major=major_list[random.randint(0,5)]
        degree=degree_list[random.randint(0,3)]
        marrige=marrige_list[random.randint(0,1)]
        politic=politic_list[random.randint(0,3)]
        historyUnit = ""
        t=random.sample(range(0, 8), 3)
        for i in t:
            judge=random.randint(0,1)
            if unit_list[i] == unit or judge == 0:
                continue
            else:
                historyUnit=historyUnit+unit_list[i]+","
        if historyUnit!="":
            historyUnit=historyUnit[0:-1]
        #print(name,sex,unit,phone,identify,duty,years,origin,graduateCollege,major,degree,marrige,politic,historyUnit)

        #staff_info=Staff_Info(name, sex, unit, phone,identify,duty,years,origin,graduateCollege,major,degree,marrige,politic,historyUnit)
        #db.session.add(staff_info)
        #db.session.commit()
    return "hello world"

if __name__ == '__main__':
    app.run(port=5000)
