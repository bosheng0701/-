import pymysql 

#打開資料庫連接，設定連接帳號root，密碼password，資料庫student
db= pymysql.connect("localhost","root","password","student")

#使用cursor()方法得到操作指標
cursor=db.cursor()

#執行SQL語句
cursor.execute("SELECT VERSION()")

#使用fetchone()得到資料
data =cursor.fetchone()

print("Database version: %s"%data)

db.close()