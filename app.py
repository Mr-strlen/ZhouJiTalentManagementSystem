from flask import Flask, url_for,render_template,redirect,request,session,abort
from flask_sqlalchemy import SQLAlchemy
import os
app=Flask(__name__)
# session 秘钥
app.secret_key = os.getenv("SECRET_KEY", "secret string")

# orm初始化
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ZhouJiAdmin:ZhouJi123#@47.102.195.43:3306/ZhouJiTalentMS'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Company(db.Model):
     #定义表名 ZJTMS_Manager_Info
     __tablename__ = "ZJTMS_Manager_Info"
     # 定义字段
     Manager_Id = db.Column(db.String(18),nullable=True,primary_key=True)
     Manager_Mail = db.Column(db.String(50),nullable=False)
     Manager_Pwd=db.Column(db.String(20),nullable=False)
     Manager_Permission=db.Column(db.String(20),nullable=False)

# 初始欢迎页
@app.route("/")
def Welcome():
    results=Company.query.all()
    for result in results:
        print(result.Manager_Id,result.Manager_Mail,result.Manager_Pwd)
    return render_template("initwelcome.html")

## 1. 登录注册流程
# 1.1 登录流程
@app.route("/login")
def Login():
    # 写入到session中
    session["logged_in"] = True
    return render_template("login.html")
#    return redirect(url_for("hi"))

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


@app.route("/checklogin")
def CheckLogin():
    return render_template("index.html")

# 1.2 注册流程
@app.route("/register")
def Register():
    return render_template("register.html")

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

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

if __name__ == '__main__':
    app.run(port=5000)