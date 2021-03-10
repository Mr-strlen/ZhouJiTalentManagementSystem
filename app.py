from flask import Flask, url_for,render_template,redirect,request,session,abort,flash
from flask_sqlalchemy import SQLAlchemy
import os
import random
app=Flask(__name__)
# session 秘钥
app.secret_key = os.getenv("SECRET_KEY", "secret string")

# orm初始化
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ZhouJiAdmin:ZhouJi123#@47.102.195.43:3306/ZhouJiTalentMS'
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
    Boss_Name = db.Column(db.String(30))

    def __init__(self, name, boss_id, boss_name):
        self.Company_Name = name
        self.Boss_Id = boss_id
        self.Boss_Name = boss_name

#  管理员表
class Manager_Info(db.Model):
     #定义表名 ZJTMS_Manager_Info
     __tablename__ = "ZJTMS_Manager_Info"
     # 定义字段
     Manager_Id = db.Column(db.String(20),nullable=False,primary_key=True)
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


# 初始欢迎页
@app.route("/")
def Welcome():
    return render_template("initwelcome.html")

## 1. 登录注册流程
# 1.1 登录流程
@app.route("/login")
def Login():
    # 写入到session中
    session["logged_in"] = True
    return render_template("login.html")
#    return redirect(url_for("hi"))
'''
## session 样例 储存信息 读取信息并进行判断
@app.route("/admin")
def admin():
    if "logged_in" not in session:
        abort(403)
    return "welcome to admin page"
## 读取session 并做不同判断
@app.route("/hi")
def hi():
    name = request.args.get("name")
    if name is None:
        # 从cookie中取值
        name = request.cookies.get("name", "default")
        response = "<h1>hi, %s</h1>" % name
        # 根据用户的不同状态返回不同的内容
        print("session: %s" % session)
        print("type(session): %s" % type(session))
        print("session.get('logged_in'): %s" % session.get('logged_in'))
    if 'logged_in' in session:
        response += "<p>[Authenticated]</p>"
    else:
        response += "<p>[Not Authenticated]</p>"
    return response

## session 登出
@app.route("/logout")
def logout():
    if "logged_in" in session:
        session.pop("logged_in")
    return redirect(url_for("hi"))
'''

@app.route("/checklogin",methods=['GET', 'POST'])
def CheckLogin():
    if request.method == 'POST':
        name = request.form.get("username")
        pwd = request.form.get("password")
        print(name, pwd)
        temp=db.session.query(Manager_Info).filter(Manager_Info.Manager_Id == name, Manager_Info.Manager_Pwd == pwd).all()
        print(temp)
        if len(temp) > 0:
            return render_template("index.html")
        else:
            flash('用户名或密码错误')
            return render_template("login.html")

# 1.2 注册流程
@app.route("/register",methods=['GET', 'POST'])
def Register():
    if request.method == 'POST':
        name = request.form.get("username")
        email = request.form.get("usermail")
        pwd = request.form.get("password")
        permission = "N"
        print(name, email, pwd, permission)
        manager_info = Manager_Info(name, email, pwd, permission)
        db.session.add(manager_info)
        db.session.commit()
        return "1"
    return render_template("register.html")

# 系统主页
@app.route("/index")
def IndexPage():
    return render_template("index.html")

## 2. 员工档案管理
# 2.1 建立档案 - 新人报道
@app.route("/staff_add")
def StaffAdd():
    return render_template("staff_add.html")

# 2.2 档案查询 - 员工群落
@app.route("/staff_list",methods=['GET', 'POST'])
def StaffList():
    name = request.form.get("username", '', str)
    degree = request.form.get("degree", '', str)
    offset = request.args.get('offset', 0, int)
    limit = request.args.get('limit', 10, int)

    search_str = ""
    # 属性是否为空判断，拼接搜索条件
    if len(name) > 0:
        search_str = search_str + "Staff_Info.Staff_Identify == name,"
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

    for v in temp:
        print(v.Staff_Name)

    return render_template("staff_list.html", page_data=temp, rangeid=0, offset=offset, limit=limit, count=count)

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
    data="1"
    return data

# 2.3 档案修改（勘误）
@app.route("/staff_change")
def StaffChange():
    return render_template("staff_change.html",)

# 2.4 档案修改（离职） - 员工离职
@app.route("/staff_leave")
def StaffLeave():
    return render_template("staff_leave.html")

## 3. 未就业员工处理 - 员工联盟
# 3.1  查询未就业人员 - 待业员工
@app.route("/unemploy_list")
def UnemployList():
    return render_template("unemploy_list.html")

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

if __name__ == '__main__':
    app.run(port=5000)