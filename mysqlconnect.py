import pymysql 

#打開資料庫連接，設定連接帳號root，密碼password，資料庫student
db= pymysql.connect("127.0.0.1","root1","password","root1")

#使用cursor()方法得到操作指標
cursor=db.cursor()

#執行SQL語句
cursor.execute("SELECT id,password FROM `user` ")

#使用fetchone()得到資料
data =cursor.fetchone()
print(data)


if(data[0]==1 and data[1]==123123):
    print("success login!!!")
else:
    print("ID or password is wrong~")

db.close()
