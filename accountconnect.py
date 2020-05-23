import sys
from flask import Flask, jsonify, request
import MySQLdb
import pymysql 
import requests

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    ID = request.values['username']
    pwd =request.values['password']
    
    db= pymysql.connect("127.0.0.1","root1","password","root1")
  
    cursor=db.cursor()
    cursor.execute("SELECT id,password FROM `user` WHERE id='%s' and password='%s'"%(ID,pwd))
    data =cursor.fetchone()
    results = """
    <p></p>
    """
    if(data!=None):
        results += "<p>success login!</p>"
    else:
        results += "<p>ID or password is wrong~</p>"
        
     
    return results
    
if __name__ == "__main__":
    app.run(debug=False, host='127.0.0.1', port=5566)  
    sys.exit()
    
