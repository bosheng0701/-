import sys
from flask import Flask, jsonify, request,render_template,session
import MySQLdb
import pymysql 
import requests
import traceback
import cgi
from flask_session import Session
from redis import Redis
import os

app = Flask(__name__)

app.config['SESSION_PERMANENT'] = True
app.config['SESSION_USE_SIGNER'] = False  
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = 7200
app.config['SESSION_FILE_THRESHOLD'] = 100  
app.config['SECRET_KEY'] = "bobb0711"
Session(app)
db= pymysql.connect("127.0.0.1","bobo","123123","bobo")
cursor=db.cursor()

@app.route('/search1', methods=['GET', 'POST'])
def search():
    
    college=(str(request.form['college']))
    query="SELECT * FROM `course` WHERE class='%s'"%(college)
    cursor.execute(query)
    data =cursor.fetchall()
    for  value in data:
         print(value)
    return str(data)

@app.route('/search2', methods=['GET', 'POST'])
def search2():
    
    c_id=(str(request.form['C_ID']))
    c_name=(str(request.form['C_name']))
    t_id=(str(request.form['T_ID']))
    query="SELECT * FROM `course` WHERE "
    if(c_id!="" and c_name!="" and t_id!=""):
        query+="c_id='%s' and c_name='%s' and instructor='%s'"%(c_id,c_name,t_id)
    elif(c_id!="" and c_name!=""):
        query+="c_id='%s' and c_name='%s'"%(c_id,c_name)
    elif(c_id!="" and t_id!=""):
        query+="c_id='%s' and instructor='%s'"%(c_id,t_id)
    elif(c_name!="" and t_id!=""):
        query+="c_name='%s'and instructor='%s'"%(c_name,t_id)    
    elif(c_id!=""):
        query+="c_id='%s'"%(c_id)
    elif(c_name!=""):
        query+="c_name='%s'"%(c_name)
    elif(t_id!=""):
        query+="instructor='%s'"%(t_id)
    else:
        return "None"
    cursor.execute(query)
    data =cursor.fetchall()
    for  value in data:
         print(value)
    return str(data)
@app.route('/searchCourse')
def f_search():
    
    return render_template('searchCourse.html',student="NULL")

@app.route('/schedule')
def f_schedule():
    return render_template('schedule.html')

@app.route('/index')
def f_index():
    return render_template('index.html')

@app.route('/action', methods=['GET', 'POST'])
def index():
    ID = request.values['username']
    pwd =request.values['password']
    
    
    if(ID.isupper):
        ID=ID.lower()
    
    cursor.execute("SELECT * FROM `student` WHERE s_id='%s' and s_password='%s'"%(ID,pwd))
    data =cursor.fetchone()

    if(data!=None):
        session['username']=ID
        session['password']=pwd
        print(session.get('username'))
        return render_template('searchCourse.html',login_message=1,student=data)
    else:
        return render_template('fail.html')
        
     
    
if __name__ == "__main__": 
    app.run(debug=False, host='127.0.0.1', port=5566)  
    sys.exit()
    
