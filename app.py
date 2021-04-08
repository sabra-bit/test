
# venv\Scripts\activate
# Set-ExecutionPolicy Unrestricted -Scope Process

import sqlite3
from flask import Flask, redirect, url_for, render_template, request, session, jsonify ,json

app = Flask(__name__)

app.secret_key = "SecretSecret"


@app.route("/sss", methods=[ "GET","POST"] )
def addAT():
        if request.method == 'POST':
            ID = request.form['data']
            con = sqlite3.connect("data_store.db") 
            cur = con.cursor()
            cur.execute("select Name,Age, Address from child where Code = ?",[ID])
            result = cur.fetchall()
            if result:
                for i in result:
                    return "name:"+i[0]+" age:"+i[1]+" address:"+i[2]
            else:
                return "QR code not faund"


            return '<h1>sabra<h1>'
        else:
            return 'try again'

@app.route('/')  
def wellcome():  
    return render_template("login.html")

@app.route('/view', methods = ['POST'])    
def view():
  
    if "admin" in session:
        con = sqlite3.connect("data_store.db") 
        cur = con.cursor()

        cur.execute("select * from child")
        result = cur.fetchall()
        return render_template("view.html" , data=result)
    else:
        return redirect("/")



@app.route('/add', methods = ['POST'])    
def add():
    if "admin" in session:   
        Name = request.form["name"]
        Age = request.form["age"]
        Address = request.form["address"]
        Code = request.form["code"]

        con = sqlite3.connect("data_store.db") 
        cur = con.cursor()
        con.execute("create table if not exists child  (id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT NOT NULL, Age TEXT NOT NULL, Address TEXT NOT NULL,Code TEXT UNIQUE NOT NULL)")
        with sqlite3.connect("data_store.db") as con:  
                    cur = con.cursor()  
                    cur.execute("INSERT into child (Name, Age, Address,Code) values (?,?,?,?)",(Name,Age,Address,Code))  
                    con.commit()  
                    msg = "doctor successfully Added" 
        return render_template("genrate.html" , name=Name,qdata=Code)
    else:
        return redirect("/")

@app.route("/gen", methods = ['GET','POST'])
def gen():
   return render_template("scanner.html")

@app.route('/login', methods = ['POST'])  
def login():
    ID = request.form["ID"]
    con = sqlite3.connect("data_store.db") 
    cur = con.cursor()
    
    con.execute("create table if not exists admin  (id INTEGER PRIMARY KEY AUTOINCREMENT, Aid TEXT NOT NULL)")
    cur.execute("select *  from admin")
    result = cur.fetchall()
    if not result:
        with sqlite3.connect("data_store.db") as con:  
            cur = con.cursor()  
            cur.execute(" INSERT into admin (Aid) values (?)",["admin"])  
            con.commit() 
        return render_template("login.html", ms="add ID")  
    else:
        cur.execute("select * from admin")
        result = cur.fetchall()
        print (result) # do session 5 min
        for row in result:
            print(row[1])
            if ID == row[1]:
                session["admin"] = row[1]
                return redirect("/admin")
    
         
        return render_template("login.html", ms="Bad ID")  
     

@app.route('/admin', methods = ['POST','GET'])  
def admin():
    if "admin" in session:
        return render_template("admin.html")
    else:
        return redirect("/")

@app.route('/out', methods = ['POST','GET'])  
def out():
    if "admin" in session:
        session.pop("admin",None)
        return redirect("/")

if __name__ == '__main__':
     app.run(host="0.0.0.0" ,port=5000 , debug= True)
    # app.run(debug= True)