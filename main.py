from flask import Flask , render_template , redirect , url_for , session,request,jsonify,Markup
from flask_mysqldb import MySQL
import MySQLdb
import numpy as np
import pickle
import pandas as pd
import json
import plotly

app = Flask(__name__)
app.secret_key = "1234353255"
model = pickle.load(open('model.pkl', 'rb'))

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "shahan1996"
app.config["MYSQL_DB"] = "zscoredb"

db = MySQL(app)



@app.route('/')
def home():
    return render_template(("home.html"))

#router for login HTML and fun(log) to authenticate the user 
#if login is successful direct to profile HTML else redirect to the login HTML

@app.route('/log', methods=['GET','POST'])
def log():
    if request.method == 'POST':
        if 'usermail' in request.form and 'userpass' in request.form:
            usermail = request.form['usermail']
            userpass = request.form['userpass']
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("select * from student where usermail =%s and userpass = %s",(usermail,userpass))
            info = cursor.fetchone()

            if info is not None:
                if info ['usermail'] == usermail and info['userpass'] == userpass:
                    session['loginsuccess']= True
                    session['usermail'] =usermail
                    return redirect(url_for("profile"))
            else:
                return redirect(url_for("log"))

    return render_template(("login.html"))

@app.route('/register2')
def register2():
    return render_template("register.html")

@app.route('/log2')
def log2():
    return render_template("login.html")

#router for register HTML and fun(register) to register a new user
#if register is successful direct to the login HTML else redirect to the register HTML

@app.route('/register', methods = ['GET','POST'])
def register():
    if request.method == "POST":
        if "username2" in request.form and "userpass2" in request.form and "usermail2" in request.form:
            username1 = request.form['username2']
            userpass1 = request.form['userpass2']
            usermail1 = request.form['usermail2']

            cur1 = db.cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cur1.execute("select * from student where usermail =%s",(usermail1,))
            info1 = cur1.fetchone()
            if info1 is not None:
                return redirect(url_for("home"))
            else:
                cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("INSERT INTO student (username,usermail,userpass) VALUES (%s,%s,%s)",(username1,usermail1,userpass1))
                db.connection.commit()
                return redirect(url_for("log"))        

    return render_template("register.html")


#to the profile *profile from logging page

@app.route('/profile',methods=['GET','POST'])
def profile():
    if session['loginsuccess'] == True:
        usermail = session['usermail']
        cu1 = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cu1.execute("select * from student where usermail = (%s)",(usermail,))
        data = cu1.fetchall()
        return render_template("profile.html", data=data)


#to input marks for prediction *marks from the profile

@app.route('/marks')
def marks():
    if session['loginsuccess'] == True:
        usermail= session['usermail']
        return render_template("marks.html")

#to predicted z score 

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0], 4)
    session["z"] = output
    usermail = session['usermail']

    if request.method == "POST":
        if "math_1" in request.form and "math_2" in request.form and "math_3" in request.form and "phy_1" in request.form and "phy_2" in request.form and "phy_3" in request.form and "chem_1" in request.form and "chem_2" in request.form and "chem_3" in request.form and "gender" in request.form and "sleeping_hours" in request.form and "distance_to_school (kms)" in request.form and "school_type" in request.form and "income(Rs)" in request.form:
            m1 = request.form['math_1']
            m2 = request.form['math_2']
            m3 = request.form['math_3']
            p1 = request.form['phy_1']
            p2 = request.form['phy_2']
            p3 = request.form['phy_3']
            c1 = request.form['chem_1']
            c2 = request.form['chem_2']
            c3 = request.form['chem_3']
            g1= request.form['gender']
            sh = request.form['sleeping_hours']
            d = request.form['distance_to_school (kms)']
            sc= request.form['school_type']
            inc= request.form['income(Rs)']

            curr = db.connection.cursor(MySQLdb.cursors.DictCursor)
            curr.execute("UPDATE zscoredb.student SET m1=%s ,m2=%s , m3=%s ,p1=%s,p2=%s,p3=%s,c1=%s,c2=%s,c3=%s,gender=%s,hours=%s,distance=%s,schtype=%s,income=%sWHERE usermail=%s",(m1,m2,m3,p1,p2,p3,c1,c2,c3,g1,sh,d,sc,inc,usermail))
            db.connection.commit()

            cu7 = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cu7.execute("select * from uni where cutoff <= %s", (output,))
            dat = cu7.fetchall()





    return render_template('pred.html',prediction_text='Student  Zscore {}'.format(output),data=dat)
#
#to input the real z score
@app.route('/realz')
def realz():
    if session['loginsuccess'] == True:
        usermail = session['usermail']
        return render_template("realz.html")

@app.route('/realzz', methods=['POST'])
def realzz():
    if session['loginsuccess'] == True:
        usermail = session['usermail']
        if request.method == "POST":
            if "Zscore" in request.form:
                z1 = request.form['Zscore']
                currr = db.connection.cursor(MySQLdb.cursors.DictCursor)
                currr.execute("UPDATE zscoredb.student SET RealZ=%s WHERE usermail=%s",(z1,usermail))
                db.connection.commit()
                return redirect(url_for('profile'))

#to logout from the profile *out

@app.route('/out')
def out():
    if session['loginsuccess'] == True:
        session.pop('loginsuccess')
        return render_template("home.html")





if __name__ == '__main__':
    app.run(debug=True)