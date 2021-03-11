from flask import Flask, url_for, render_template, redirect, request, session, abort, flash
from flask_sqlalchemy import SQLAlchemy
import os, datetime
import random
app=Flask(__name__)
# session 秘钥
app.secret_key = os.getenv("SECRET_KEY", "secret string")

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
     Comments = db.Column(db.String(255), nullable=False)
     Comments_Time = db.Column(db.DateTime, nullable=False, primary_key=True)

     def __init__(self, s_id, m_id, comments, time):
         self.Staff_Id = s_id
         self.Manager_Id = m_id
         self.Comments = comments
         self.Comments_Time = time

#  调档申请记录表
class Staff_InfoReply(db.Model):
     #定义表名 ZJTMS_Manager_Info
     __tablename__ = "ZJTMS_Staff_InfoReply"
     # 定义字段
     ReplyManager_Id = db.Column(db.String(20), nullable=False)
     TargetCompany_Name = db.Column(db.String(20), nullable=False)
     Reply_Time=db.Column(db.DateTime,nullable=False, primary_key=True)
     Reply_Status=db.Column(db.Integer,nullable=False)
     Reply_Reason = db.Column(db.String(255), nullable=True)
     Comfirm_Id = db.Column(db.String(20), nullable=True)

     def __init__(self, m_id, company, time, status, reason, c_id):
         self.ReplyManager_Id = m_id
         self.TargetCompany_Name = company
         self.Reply_Time = time
         self.Reply_Status = status
         self.Reply_Reason = reason
         self.Comfirm_Id = c_id

# 员工星级评定表
class Staff_Stars(db.Model):
    # 定义表名 ZJTMS_Manager_Info
    __tablename__ = "ZJTMS_Staff_Stars"
    # 定义字段
    Stuff_Id = db.Column(db.String(20), nullable=False)
    Manager_Id = db.Column(db.String(20), nullable=False)
    Leadership = db.Column(db.Integer, nullable=False)#领导力
    Creativity = db.Column(db.Integer, nullable=False)#创新性
    Communication = db.Column(db.Integer, nullable=False)#交际能力
    Hardworking = db.Column(db.Integer, nullable=True)#勤奋度
    Efficiency = db.Column(db.Integer, nullable=True)#工作效率
    Comment_Time = db.Column(db.DateTime, nullable=False, primary_key=True)

    def __init__(self, s_id, m_id, L1, C2, C3, H4, E5, time):
        self.Stuff_Id = s_id
        self.Manager_Id = m_id
        self.Leadership = L1
        self.Creativity = C2
        self.Communication = C3
        self.Hardworking = H4
        self.Efficiency = E5
        self.Comment_Time = time

# 初始欢迎页
@app.route("/")
def Welcome():
    return render_template("initwelcome.html")

## 1. 登录注册流程
# 1.1 登录流程
@app.route("/login")
def Login():
    return render_template("login.html")

@app.route("/checklogin",methods=['GET', 'POST'])
def CheckLogin():
    if request.method == 'POST':
        name = request.form.get("username")
        pwd = request.form.get("password")
        print(name, pwd)
        # 匹配密码
        # 邮箱登录
        if '@' in name:
            temp = db.session.query(Manager_Info).filter(Manager_Info.Manager_Mail == name, Manager_Info.Manager_Pwd == pwd).all()
            if len(temp) > 0:
                name=temp[0].Manager_Id
        # 身份证号登录
        else:
            temp = db.session.query(Manager_Info).filter(Manager_Info.Manager_Id == name, Manager_Info.Manager_Pwd == pwd).all()
        print(temp)
        if len(temp) > 0:
            session["logged_in"] = True # 登录状态
            session["identity"] = temp[0].Manager_Id # 登录id
            # 匹配身份
            t=db.session.query(Company).filter(Company.Boss_Id == name).all()
            if len(t) > 0:  # 为COO
                session["realname"] = t[0].Boss_Name
                session["company"] = t[0].Company_Name
                session["permission"] = "S"
                return render_template("index.html", username=t[0].Boss_Name)
            else:
                ti = db.session.query(Staff_Info).filter(Staff_Info.Staff_Identify == name).first()
                session["realname"] = ti.Staff_Name
                session["company"] = ti.Staff_Unit
                session["permission"] = "N"
                return render_template("index.html", username=ti.Staff_Name)
        else:
            flash('用户名或密码错误')
            return render_template("login.html")

# 1.2 注册流程
# 1.2.1 普通HR
@app.route("/register",methods=['GET', 'POST'])
def Register():
    if request.method == 'POST':
        name = request.form.get("username")
        email = request.form.get("usermail")
        pwd = request.form.get("password")
        permission = "N"
        # print(name, email, pwd, permission)

        # 已经存在账号
        temp = db.session.query(Manager_Info).filter(Manager_Info.Manager_Id == name).all()
        if len(temp) > 0:
            return "2"
        # 邮箱重复
        temp = db.session.query(Manager_Info).filter(Manager_Info.Manager_Mail == email).all()
        if len(temp) > 0:
            return "5"
        # 员工不存在
        temp = db.session.query(Staff_Info).filter(Staff_Info.Staff_Identify == name).all()
        if len(temp) > 0: # 员工不为HR
            if temp[0].Staff_Duty != "HR":
                return "4"
        else:
            return "3"

        manager_info = Manager_Info(name, email, pwd, permission)
        db.session.add(manager_info)
        db.session.commit()
        return "1"
    return render_template("register.html")

# 1.2.2 公司COO
@app.route("/COOregister",methods=['GET', 'POST'])
def COORegister():
    if request.method == 'POST':
        name = request.form.get("username")
        realname = request.form.get("realname")
        company =request.form.get("company")
        email = request.form.get("usermail")
        pwd = request.form.get("password")
        permission = "S"
        # print(name, realname, company, email, pwd, permission)

        # 公司已经注册
        temp = db.session.query(Company).filter(Company.Company_Name == company).all()
        if len(temp) > 0:
            return "2"
        # 邮箱重复
        temp = db.session.query(Manager_Info).filter(Manager_Info.Manager_Mail == email).all()
        if len(temp) > 0:
            return "3"

        # 公司信息建立
        new_company= Company(company, name, realname)
        # 账户信息建立
        manager_info = Manager_Info(name, email, pwd, permission)
        db.session.add(new_company)
        db.session.commit()
        db.session.add(manager_info)
        db.session.commit()

        return "1"
    return render_template("COOregister.html")

## 2. 员工档案管理
# 2.1 建立档案 - 新人报道
@app.route("/staff_add",methods=['GET', 'POST'])
def StaffAdd():
    # 获取Company 表的公司数据
    company_lists = db.session.query(Company).all()
    #for temp in company_lists:
        #print(temp.Company_Name)
    if request.method == 'POST':
        username = request.form.get("username")
        sexual = request.form.get("sexual")
        id = request.form.get("id")
        origin = request.form.get("origin")
        gladuate_college = request.form.get("gladuate_college")
        major = request.form.get("major")
        degree = request.form.get("degree")
        marriage = request.form.get("marriage")
        politic = request.form.get("politic")
        phone = request.form.get("phone")
        unit = request.form.get("unit")
        duty = request.form.get("duty")
        history_unit = request.form.get("history_unit", "", str)
        years = request.form.get("years")
        #print(request.method)
        #print(username,sexual,id,origin,gladuate_college,major,degree,marriage,politic,phone,unit,duty,history_unit,years)
        # 添加用户
        staff_info = Staff_Info(username, sexual, unit, phone, id, duty, years,origin , gladuate_college, major, degree, marriage, politic, history_unit)
        db.session.add(staff_info)
        db.session.commit()
        return "1"
    return render_template("staff_add.html",company_lists=company_lists)

# 2.2 档案查询 - 员工群落
@app.route("/staff_list",methods=['GET', 'POST'])
def StaffList():
    username = request.args.get("username", '', str)
    degree = request.args.get("degree", '', str)
    offset = request.args.get('offset', 0, int)
    limit = request.args.get('limit', 10, int)

    company = session.get("company")
    permission = session.get("permission")
    search_str = "Staff_Info.Staff_Unit == company," #必须为自己公司的员工

    if permission == "N": #Hr不能看到同为Hr的信息
        search_str = search_str + "Staff_Info.Staff_Duty != HR,"

    # 属性是否为空判断，拼接搜索条件
    if len(username) > 0:
        search_str = search_str + "Staff_Info.Staff_Identify == username,"
    if len(degree) > 0:
        search_str = search_str + "Staff_Info.Staff_Degree == degree,"

    # 如果搜索条件为空，即为全部搜索
    temp = []
    if len(search_str) > 0:
        search_str = search_str[0:-1] # 逗号删减
        temp = eval("db.session.query(Staff_Info).filter(" + search_str + ").order_by(Staff_Info.Staff_Identify).limit(limit).offset(offset).all()")
        count = len(eval("db.session.query(Staff_Info).filter(" + search_str + ").all()"))
    else:
        temp = db.session.query(Staff_Info).order_by(Staff_Info.Staff_Identify).limit(limit).offset(offset).all()
        count = len(db.session.query(Staff_Info).all())

    print(degree, username)

    return render_template("staff_list.html", page_data=temp, username=username, degree=degree, rangeid=0, offset=offset, limit=limit, count=count)

# 嵌套在页面内 员工个人档案查看
@app.route("/staff_look/<id>")
def StaffLook(id):
    temp = db.session.query(Staff_Info).filter(Staff_Info.Staff_Identify == id).all()
    return render_template("staff_look.html", person=temp[0])

# 嵌套在页面内 员工个人删除查看
@app.route("/staff_del/<id>",methods=['GET', 'POST'])
def StaffDel(id):
    print(id)
    temp=db.session.query(Staff_Info).filter(Staff_Info.Staff_Identify == id).first()
    print(temp)
    db.session.delete(temp)
    db.session.commit()
    data = "1"
    return data

# 2.3 档案修改（勘误）
@app.route("/staff_change")
def StaffChange():
    return render_template("staff_change.html")

# 2.4 档案修改（离职） - 员工离职
@app.route("/staff_leave")
def StaffLeave():
    return render_template("staff_leave.html")

## 3. 未就业员工处理 - 员工联盟
# 3.1  查询未就业人员 - 待业员工
@app.route("/unemploy_list")
def UnemployList():
    username = request.args.get("username", '', str)
    degree = request.args.get("degree", '', str)
    offset = request.args.get('offset', 0, int)
    limit = request.args.get('limit', 10, int)

    search_str = "Staff_Info.Staff_Unit=='Empty',"
    # 属性是否为空判断，拼接搜索条件
    if len(username) > 0:
        search_str = search_str + "Staff_Info.Staff_Identify == username,"
    if len(degree) > 0:
        search_str = search_str + "Staff_Info.Staff_Degree == degree,"

    # 如果搜索条件为空，即为全部搜索
    temp = []
    if len(search_str) > 0:
        search_str = search_str[0:-1]  # 逗号删减
        temp = eval(
            "db.session.query(Staff_Info).filter(" + search_str + ").order_by(Staff_Info.Staff_Identify).limit(limit).offset(offset).all()")
        count = len(eval("db.session.query(Staff_Info).filter(" + search_str + ").all()"))
    else:
        temp = db.session.query(Staff_Info).order_by(Staff_Info.Staff_Identify).limit(limit).offset(offset).all()
        count = len(db.session.query(Staff_Info).all())

    print(degree, username)

    return render_template("unemploy_list.html", page_data=temp, username=username, degree=degree, rangeid=0,
                           offset=offset, limit=limit, count=count)

# 嵌套在页面内 未就业员工历史评价查看
@app.route("/unemploy_historycomment/<id>")
def UnemployHistoryComment(id):
    temp = db.session.query(Staff_Comment).filter(Staff_Comment.Staff_Id == id).all()
    length=len(temp)
    m_name=[]
    for i in temp:
        #print(i.Manager_Id)
        t = db.session.query(Staff_Info).filter(Staff_Info.Staff_Identify == i.Manager_Id).all()
        m_name.append(t[0].Staff_Name)

    return render_template("unemploy_historycomment.html", comments=temp, length=length, m_name=m_name)


## 4 跨公司申请
# 4.1 HR提出申请
@app.route("/staffinfo_reply",methods=['GET', 'POST']) #烺
def staffInfoReply():
    # 获取Company 表的公司数据
    company_lists = db.session.query(Company).all()
    print(type(company_lists[0]))
    print(session.get("company"))
    namelists = []
    for temp in company_lists:
        namelists.append(temp.Company_Name)
    namelists.remove(session.get("company"))
    print(namelists)
    # print(company_lists.remove(session.get("company")))
    permission = session.get("permission")
    if request.method == 'POST' and permission == 'S':
        return "2"
    if  request.method == 'POST' and permission=='N':
        reply_id = session.get("identity")
        reply_company = request.form.get("reply_company")
        reply_date = datetime.datetime.today()
        reply_reason = request.form.get("reply_reason")
        reply_status = "0"
        reply_confirmid = ""
        print(reply_id, reply_company, reply_date, reply_reason)
        staffinfo_reply = Staff_InfoReply(reply_id,reply_company,reply_date,reply_status,reply_reason,reply_confirmid)
        db.session.add(staffinfo_reply)
        db.session.commit()
        return "1"
    return render_template("staffinfo_reply.html",company_lists=namelists)
# 4.2 COO批复申请
@app.route("/staffinfo_confirm") #飞
def StaffInfoConfirm():
    return render_template("staffinfo_confirm.html")

# 5 评价系统
# 5.1 HR给员工进行评价 打分
@app.route("/staff_comment/<id>")
def StaffComment(id):
    print(id)
    return render_template("staff_comment.html", staff_id=id)

# 增加评价 打分
@app.route("/staff_commentadd",methods=['GET', 'POST'])
def StaffCommentAdd():
    if request.method == 'POST':
        manager_id = session.get("identity")
        staff_id = request.form.get("staff_id")
        comments = request.form.get("comments")
        leadership = request.form.get("leadership")
        time = datetime.datetime.today()
        print(manager_id, staff_id, comments, leadership)
        staff_comment = Staff_Comment(staff_id, manager_id, comments, time)
        #db.session.add(staff_comment)
        #db.session.commit()
        return "1"

# 6 推荐系统

# 7 HR交流帖子系统

# 系统主页
@app.route("/index")
def IndexPage():
    username = session.get("identity", "默认用户")
    return render_template("index.html", username=username)

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

if __name__ == '__main__':
    db.create_all()
    app.run(port=5000)