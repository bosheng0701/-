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
student_ID=""
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_USE_SIGNER'] = False  
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = 7200
app.config['SESSION_FILE_THRESHOLD'] = 100  
app.config['SECRET_KEY'] = "bobb0711"

db= pymysql.connect("140.134.53.65","admin","admin123456","db_project")
cursor=db.cursor()

@app.route('/search1', methods=['GET', 'POST'])
def search():
    login_message=session.get('login_message')
    student=session.get('username')
    college=(str(request.form['college']))
    query="SELECT *,if(COUNT(section)>1,section+COUNT(section)-1,section) AS endsection  FROM course NATURAL JOIN coursetime GROUP BY c_id,day HAVING  course.class='%s'"%(college)
    cursor.execute(query)
    data =cursor.fetchall()
    for  value in data:
         print(value)
    return render_template('Courselist.html',books=data,student=student,login_message=login_message)

@app.route('/search2', methods=['GET', 'POST'])
def search2():
    
    student=session.get('username')
    login_message=session.get('login_message')
    c_id=(str(request.form['C_ID']))
    c_name=(str(request.form['C_name']))
    t_id=(str(request.form['T_ID']))
    query="SELECT *,if(COUNT(section)>1,section+COUNT(section)-1,section) AS endsection  FROM course NATURAL JOIN coursetime GROUP BY c_id,day HAVING "
    if(c_id!="" and c_name!="" and t_id!=""):
        query+="course.c_id='%s' and course.c_name='%s' and course.instructor='%s'"%(c_id,c_name,t_id)
    elif(c_id!="" and c_name!=""):
        query+="course.c_id='%s' and course.c_name='%s'"%(c_id,c_name)
    elif(c_id!="" and t_id!=""):
        query+="course.c_id='%s' and course.instructor='%s'"%(c_id,t_id)
    elif(c_name!="" and t_id!=""):
        query+="course.c_name='%s'and course.instructor='%s'"%(c_name,t_id)    
    elif(c_id!=""):
        query+="course.c_id='%s'"%(c_id)
    elif(c_name!=""):
        query+="course.c_name='%s'"%(c_name)
    elif(t_id!=""):
        query+="course.instructor='%s'"%(t_id)
    else:
        return "None"
    cursor.execute(query)
    data =cursor.fetchall()
    for  value in data:
         print(value)
    return render_template('Courselist.html',books=data,student=student,login_message=login_message)
@app.route('/searchCourse')
def f_search():
    student=session.get('username')
    print(student)
    return render_template('searchCourse.html',student=student)

@app.route('/add')
def add():
    student=session.get('username')
    course=list(request.args.values())
    
    cursor.execute("SELECT *,if(COUNT(section)>1,section+COUNT(section)-1,section) AS endsection FROM timetable"
                   " NATURAL LEFT JOIN coursetime GROUP BY s_id,c_id,day HAVING s_id=\"%s\""%(student))
    data=cursor.fetchall()

    cursor.execute("SELECT *,if(COUNT(section)>1,section+COUNT(section)-1,section) AS endsection FROM course NATURAL JOIN coursetime GROUP BY c_id,day HAVING course.c_id ='%s'"%(course[0]))
    coursetime=cursor.fetchall()

    for i in coursetime:#判斷衝堂
        for j in data:
            if(i[8]==j[5] and int(i[9])>=int(j[6]) and int(i[10])<=int(j[7])):
                return "衝堂"
    
   
    credit=int(0)
    for i in data:#判斷重複選課and課程人數
        if(course[1]==i[2]):
            return "不可重複選課"
        if(int(course[4])>=int(course[5])):
            return "課程人數已滿"
        
    cursor.execute("SELECT * FROM `timetable` WHERE `s_id`='%s'"%(student)) # 判斷學分是否超過30學分
    timetable=cursor.fetchall()
    for j in timetable:
        credit+=int(j[3])
        
    if(credit+int(course[3])>=30):
        return "超過30學分"
    
    cursor.execute("INSERT INTO timetable(s_id,c_id,c_name,credits,queue) VALUES ('%s','%s','%s','%d',0);"%(student,course[0],course[1],int(course[3])))#加選
    db.commit()
    
    return "加選成功"

@app.route('/pop')
def pop():
    student=session.get('username')
    course=list(request.args.values())
    credit=int(0)
    cursor.execute("SELECT * FROM `timetable` WHERE `s_id`='%s'"%(student)) # 判斷學分是否低於12學分
    timetable=cursor.fetchall()
    for j in timetable:
        credit+=int(j[3])
        
    if(credit-int(course[3])<12):
        return "低於12學分"
    
    cursor.execute("DELETE FROM timetable WHERE s_id='%s' and c_id='%s';"%(student,course[0]))
    db.commit()
    return "退選成功"

@app.route('/schedule') #同上 ，但是如果有收到GET/POST時要打method
def schedule():
    student=session.get('username')
    cursor.execute("SELECT *,if(COUNT(section)>1,section+COUNT(section)-1,section) AS endsection FROM timetable"
                   " NATURAL LEFT JOIN coursetime GROUP BY s_id,c_id,day HAVING s_id=\"%s\""%(student))
    data=cursor.fetchall()
    print(student)
    login_message=session.get('login_message')
    list1=[]
    list1.append((len(data),"",0,0))
    n=int(0)
    for i in data:
        if(i[5]=='一'): n=1
        elif(i[5]=='二'): n=2
        elif(i[5]=='三'): n=3
        elif(i[5]=='四'): n=4
        elif(i[5]=='五'): n=5
        elif(i[5]=='六'): n=6
        elif(i[5]=='日'): n=7
        else: n=0
        list1.append((n,i[2],i[6],i[7]))
    for i in list1:
        print(i)
    return render_template('schedule.html',student=student,books=list1,login_message=login_message)

@app.route('/index')
def f_index():
    return render_template('index.html')

@app.route('/action', methods=['GET', 'POST'])
def index():
    session.clear()
    ID = request.values['username']
    pwd =request.values['password']
    
    
    if(ID.isupper):
        ID=ID.upper()
    
    cursor.execute("SELECT * FROM `student` WHERE s_id='%s' and s_password='%s'"%(ID,pwd))
    data =cursor.fetchone()

    if(data!=None):
        session['username']=ID
        session['password']=pwd
        session['login_message']=1
        session['name']=data[1]
        session['class']=data[4]
        print(session.get('username'))
       
        return render_template('searchCourse.html',login_message=1,student=data)
    else:
        return render_template('fail.html')
        
     
    
if __name__ == "__main__": 
    app.run(debug=False, host='127.0.0.1', port=5566)  
    sys.exit()
    
