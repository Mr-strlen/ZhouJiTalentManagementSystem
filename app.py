from flask import Flask, url_for
from flask import request
from flask import render_template,redirect
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ZhouJiAdmin:ZhouJi123#@47.102.195.43:3306/ZhouJiTalentMS'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Company(db.Model):
     #定义表名1
     __tablename__ = "Company"
     # 定义字段
     Company_Name = db.Column(db.String(20),nullable=True)
     Boss_Id = db.Column(db.String(18),primary_key=True,nullable=True)
     Boss_Name=db.Column(db.String(255))

# 初始欢迎页
@app.route("/")
def Welcome():
    results=Company.query.all()
    for result in results:
        print(result.Company_Name,result.Boss_Id,result.Boss_Name)
    return render_template("welcome.html")

## 1. 登录注册流程
# 1.1 登录流程
@app.route("/login")
def Login():
    return render_template("login.html")

@app.route("/check")
def CheckLogin():
    return render_template("index.html")

# 1.2 注册流程
@app.route("/register")
def Register():
    return render_template("index.html")

# 系统主页
@app.route("/index")
def IndexPage():
    return render_template("index.html")

## 2. 员工档案管理
# 2.1 建立档案 - 新人报道
@app.route("/stuff_add")
def StuffAdd():
    return render_template("stuff_add.html")

# 2.2 档案查询 - 员工群落
@app.route("/stuff_list")
def StuffList():
    return render_template("stuff_list.html")

# 2.3 档案修改（勘误）
@app.route("/stuff_change")
def StuffChange():
    return render_template("stuff_change.html")

# 2.4 档案修改（离职） - 员工离职
@app.route("/stuff_leave")
def StuffLeave():
    return render_template("stuff_leave.html")

## 3. 未就业员工处理 - 员工联盟
# 3.1  查询未就业人员 - 待业员工
@app.route("/unemploy_list")
def UnemployList():
    return render_template("unemploy_list.html")


if __name__ == '__main__':
    app.run(port=5000)