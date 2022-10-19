import pymysql
def make_connection():
    cn=pymysql.connect(host="localhost",port=3306,password="",user="root",db="b335",autocommit=True)
    cur=cn.cursor()
    return cur
