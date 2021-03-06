from flask import Flask
from flask import request
from flask import render_template

app=Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("login.html")
@app.route("/login.html",methods=["GET","POST"])
def login():

    print("login")
    username=request.form.get('username')
    if request.method=="POST":
        print(username)
        return "success"

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
if __name__ == '__main__':
    app.run(port=5005)