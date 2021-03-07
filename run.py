from flask import Flask, url_for
from flask import request
from flask import render_template,redirect
import pymysql
conn=pymysql.connect(
    host='47.102.195.43',
    port=3306,
    user="ZhouJiAdmin",
    password="ZhouJi123#",
    database="ZhouJiTalentMS",
    charset='utf8'
)
if(conn):
    print("数据库连接成功")
cursor=conn.cursor();



app=Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("member-add.html")
@app.route("/login.html",methods=["GET","POST"])
def login():

    return render_template("login.html")
@app.route("/checkadd",methods=['GET','POST'])
def checkadd():
    name = request.form.get("username")
    print(name)
    pwd = request.form.get("password")
    print(pwd)
    sql = "insert into  testlogin (user,pwd) values(\"{}\",\"{}\")".format(name, pwd);
    print(sql)
    count = cursor.execute(sql)
    print(count)
    if count > 0:
        return "1"
@app.route('/check',methods=['GET','POST'])
def check():
    print("来了一个ajax请求")
    # print(login)
    print(request.method)
    if request.method == 'GET':
        name = request.args.get("username")
        pwd = request.args.get("password")
        print("name:", name, "pwd:", pwd)

    else:

        name = request.form.get("username")
        print(name)
        pwd = request.form.get("password")
        print(pwd)
        sql="select * from testlogin where user =\"{}\" and pwd=\"{}\"".format(name,pwd);
        print(sql)
        count=cursor.execute(sql)
        print(count)
        if count>0:
            return "1"

    return render_template("login.html")



@app.route("/index")
def index():
    return render_template("index.html")
@app.route("/memberadd")
def signup():
    return render_template("member-add.html")
@app.route("/welcome.html")
def welcome():
    return render_template("welcome.html")
@app.route("/admin-list")
def memberlistlist():
    return render_template("admin-list.html")

@app.route("/member-list.html")
def adminlist():
    return render_template("member-list.html")

@app.route("/member-list1.html")
def adminlist1():
    return render_template("member-list1.html")


@app.route("/member-del.html")
def memberdel():
    return render_template("member-del.html")

@app.route("/member-adddel.html")
def memberadd():
   
    return render_template("member-add.html")


if __name__ == '__main__':
    app.run(port=5007)