from flask import Flask, render_template,request,flash,redirect,url_for,session
import sqlite3
import os

app = Flask(__name__)
app.secret_key="123"

con=sqlite3.connect("database.db")
con.execute("create table if not exists User(pid integer primary key,name text,address text,mail text,password text)")
con.close()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=='POST':
        name=request.form['name']
        password=request.form['password']
        con=sqlite3.connect("database.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from User where name=? and password=?",(name,password))
        data=cur.fetchone()

        if data:
            session["name"]=data["name"]
            session["mail"]=data["mail"]
            return redirect("Home")
        else:
            flash("Username and Password Mismatch","danger")
    return redirect(url_for("index"))

picFolder = os.path.join('static' ,'pics')
app.config['UPLOAD_FOLDER'] =picFolder

@app.route('/Home',methods=["GET","POST"])
def customer():
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'] , 'photos (1).gif')
    return render_template("index.html" , user_img = pic1)

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        try:
            name=request.form['name']
            address=request.form['address']
            mail=request.form['mail']
            password=request.form['password']
            con=sqlite3.connect("database.db")
            cur=con.cursor()
            cur.execute("insert into User(name,address,mail,password)values(?,?,?,?)",(name,address,mail,password))
            con.commit()
            flash("Record Added  Successfully","success")
        except:
            flash("Error in Insert Operation","danger")
        finally:
            return redirect(url_for("login"))
            con.close()

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route('/rb')
def rb():
    return render_template("rb.html")

if __name__ == '__main__':
    app.run(debug=True)
