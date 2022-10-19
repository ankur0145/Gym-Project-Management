from flask import Flask,render_template,request,redirect,url_for,session
import pymysql
from mylib import make_connection
app=Flask(__name__)
app.secret_key="super secret key"

@app.route('/',methods=['GET','POST'])
def welcome():
    return render_template("welcome.html")


#login file
@app.route("/login",methods=['GET','POST'])
def login():
    if(request.method=="POST"):
        em=request.form["t1"]
        pa=request.form["t2"]
        cur=make_connection()
        sql="select * from login where email='"+em+"' AND password='"+pa+"'"
        cur.execute(sql)
        n=cur.rowcount
        if(n==1):
            data=cur.fetchone()
            ut=data[2]
            #Create session
            session["email"]=em
            session["usertype"]=ut
            #send to page
            if(ut=="admin"):
                return render_template("admin_home.html")
            elif(ut=="gym"):
                return render_template("gym_home.html")
            else:
                return render_template("login.html",msg="Invalid usertype , Contact to admin")
        else:
            return render_template("login.html",msg="Either userid or password is incorrect")
    else:
        return render_template("login.html")

#logout
@app.route("/logout",methods=['GET','POST'])
def logout():
    #Check existance of session
    if("email" in session):
        # Remove session
        print("Hello")
        session.pop("email",None)
        session.pop("usertype",None)
        return redirect(url_for("login"))
    else:
        print("Hello1")
        return redirect(url_for("login"))

#Authorization Error
@app.route("/auth_error")
def auth_error():
    return render_template("authorization.html")


#admin
@app.route("/admin_home",methods=['GET','POST'])
def  admin_home():
    #Check session
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="admin"):
            return render_template("admin_home.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#admin_reg
@app.route('/admin_reg',methods=['GET','POST'])
def admin_reg():
    #create session
    if("usertype" in session):
        ut=session["usertype"]
        if (ut=="admin"):
            if(request.method=='POST'):
                print("POST after submit")
                nm = request.form["t1"]
                add = request.form["t2"]
                con = request.form["t3"]
                email = request.form["t4"]
                pas=request.form["t5"]
                usertype = "admin"
                cn = pymysql.connect(host="localhost", port=3306, passwd="", user="root", db="b335",autocommit=True)
                cur = cn.cursor()
                sql = "insert into admin values('" + nm + "','" + add + "'," + con + ",'" + email + "')"
                sql1 = "insert into login values('" + email + "','"+ pas +"','" + usertype + "')"
                print(sql)
                print(sql1)
                try:
                    cur.execute(sql)
                    n = cur.rowcount
                    cur.execute(sql1)
                    m = cur.rowcount
                    if (n == 1 and m == 1):
                        msg = "data saved"
                    else:
                        msg="data not saved"
                except pymysql.err.IntegrityError:
                    msg="it is already registered"
                return render_template("admin_reg.html",result=msg)


            else:
                print("this is get request")
                return render_template("admin_reg.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


#change password of admin home
@app.route("/admin_change_password",methods=['GET','POST'])
def admin_change_password():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="admin"):
            if(request.method=="POST"):
                e1=session["email"]
                oldpas=request.form["t1"]
                newpas=request.form["t2"]
                cur=make_connection()
                sql="update login set password='"+newpas+"' where email='"+e1+"' AND password='"+oldpas+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    return render_template("admin_change_password.html",result="password change")
                else:
                    return render_template("admin_change_password.html",result="password not changed")
            else:
                return render_template("admin_change_password.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


#admin profile
@app.route("/adminprofile",methods=['GET','POST'])
def adminprofile():
    if("usertype"in session):
        ut=session["usertype"]
        if(ut=="admin"):
            cur=make_connection()
            e1=session["email"]
            sql="select * from admin where email='"+e1+"'"
            cur.execute(sql)
            n=cur.rowcount
            if(n>0):
                data=cur.fetchone()
                return render_template("adminprofile1.html",kota=data)
            else:
                return render_template("adminprofile1.html",msg="data not found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


#admin update
@app.route("/adminprofile1",methods=['GET','POST'])
def adminprofile1():
    if("usertype"in session):
        ut=session["usertype"]
        if(ut=="admin"):
            if(request.method=="POST"):
                cur=make_connection()
                e1=session["email"]
                sql="select * from admin where email='"+e1+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    data=cur.fetchone()
                    return render_template("adminprofile1.html",kota=data)
                else:
                    return render_template("adminprofile1.html",msg="data not found")
            else:
                return redirect(url_for("adminprofile"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


#updated admin profile2
@app.route("/adminprofile2",methods=['GET','POST'])
def adminprofile2():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="admin"):
            if(request.method=="POST"):
                nm=request.form["t1"]
                ad=request.form["t2"]
                cn=request.form["t3"]
                e1=session["email"]
                cur=make_connection()
                sql="update admin set name='"+nm+"',address='"+ad+"',contact='"+cn+"' where email='"+e1+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    return render_template("adminprofile2.html",msg="data saved")
                else:
                    return render_template("adminprofile2.html",msg="data not saved")


            else:
                return redirect(url_for("adminprofile"))

        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


#gym Home
@app.route("/gym_home",methods=['GET','POST'])
def gym_home():
    #Check session
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="gym"):
            return render_template("gym_home.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#gym reg
@app.route('/gym_reg',methods=['GET','POST'])
def gym_reg():
    #create session
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="gym"):
            if(request.method=='POST'):
                print("POST after submit")
                n=request.form["t1"]
                on=request.form["t2"]
                ad=request.form["t3"]
                ca=request.form["t4"]
                email=request.form["t5"]
                ps=request.form["t6"]
                usertype="gym"
                cur=make_connection()
                sql="insert into gym values('"+n+"','"+on+"','"+ad+"',"+ca+",'"+email+"')"
                sql1="insert into login values('"+email+"','"+ps+"','"+usertype+"')"
                print(sql)
                print(sql1)
                try:
                    cur.execute(sql)
                    n=cur.rowcount
                    cur.execute(sql1)
                    m=cur.rowcount
                    if(n==1 and m==1):

                        mg="data saved"

                    else:
                        mg="data not saved"
                except pymysql.err.IntegrityError:
                    mg="It is already registration"

                return render_template("gym_reg.html",result=mg)
            else:
                print("This is get request")
                return render_template("gym_reg.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


#change password of gym home
@app.route("/gym_change_password",methods=['GET','POST'])
def gym_change_password():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="gym"):
            if(request.method=="POST"):
                e1=session["email"]
                oldpas=request.form["t1"]
                newpas=request.form["t2"]
                cur=make_connection()
                sql="update login set password='"+newpas+"' where email='"+e1+"' AND password='"+oldpas+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    return render_template("gym_change_password.html",result="password change")
                else:
                    return render_template("gym_change_password.html",result="password not changed")
            else:
                return render_template("gym_change_password.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))



#gym profile

@app.route("/gymprofile",methods=['GET','POST'])
def gymprofile():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="gym"):
            cur=make_connection()
            e1=session["email"]
            sql="select * from gym where email='"+e1+"'"
            cur.execute(sql)
            n=cur.rowcount
            if(n>0):
                data=cur.fetchone()
                return render_template("gymprofile1.html",kota=data)
            else:
                return render_template("gymprofile1.html",msg="data not found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


#update gym profile1
@app.route("/gymprofile1",methods=['GET','POST'])
def gymprofile1():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="gym"):
            if(request.method=="POST"):
                e1=session["email"]
                cur=make_connection()
                sql="select * from gym where email='"+e1+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    data=cur.fetchone()
                    return render_template("gymprofile1.html",kota=data)
                else:
                    return render_template("gymprofile1.html",msg="no data found")
            else:
                return redirect(url_for("gymprofile"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


#updated gym profile2
@app.route("/gymprofile2",methods=['GET','POST'])
def gymprofile2():
    if("usertype" in session ):
        ut=session["usertype"]
        if(ut=="gym"):
            if(request.method=="POST"):
                n=request.form["t1"]
                on=request.form["t2"]
                ad=request.form["t3"]
                co=request.form["t4"]
                e1=session["email"]
                cur=make_connection()
                sql="update gym set name='"+n+"',owner_name='"+on+"',address='"+ad+"',contact='"+co+"' where email='"+e1+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    return render_template("gymprofile2.html",msg="data saved")
                else:
                    return render_template("gymprofile2.html",msg="data not found")
            else:
                return redirect(url_for("gymprofile"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


#show trainer

@app.route("/show_trainer",methods=['GET','POST'])
def show_trainer():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="gym"):
            cur=make_connection()
            e1=session["email"]
            sql="select * from trainer where email='"+e1+"'"
            cur.execute(sql)
            n=cur.rowcount
            if(n>0):
                data=cur.fetchone()
                return render_template("show_trainer.html",kota=data)
            else:
                return render_template("show_trainer.html",msg="data not found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


#edit trainer
@app.route("/edittrainer",methods=['GET','POST'])
def edittrainer():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="gym"):
            if(request.method=="POST"):
                e1=session["email"]
                cur=make_connection()
                sql="select * from trainer where email='"+e1+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    data=cur.fetchone()
                    return render_template("edittrainer.html",kota=data)
                else:
                    return render_template("edittrainer.html",msg="no data found")
            else:
                return redirect(url_for("show_trainer"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#edit trainer1
@app.route("/edittrainer1",methods=['GET','POST'])
def edittrainer1():
    if("usertype" in session ):
        ut=session["usertype"]
        if(ut=="gym"):
            if(request.method=="POST"):
                tn=request.form["t1"]
                ad=request.form["t2"]
                co=request.form["t3"]
                f=request.form["t4"]
                e1=session["email"]
                cur=make_connection()
                sql="update trainer set trainer_name='"+tn+"',address='"+ad+"',contact='"+co+"',fees='"+f+"' where email='"+e1+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    return render_template("edittrainer1.html",msg="data saved")
                else:
                    return render_template("edittrainer1.html",msg="data not found")
            else:
                return redirect(url_for("show_trainer"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


#add trainer
@app.route("/add_trainer",methods=['GET','POST'])
def add_trainer():
    if("usertype" in session ):
        ut=session["usertype"]
        if(ut=="gym"):
            if(request.method=='POST'):
                print("post after submit")
                tn=request.form["t1"]
                ad=request.form["t2"]
                c=request.form["t3"]
                f=request.form["t4"]
                e1=session["email"]
                cur=make_connection()
                sql="insert into trainer values('"+tn+"','"+ad+"','"+c+"',"+f+",'"+e1+"')"
                print(sql)
                try:
                    cur.execute(sql)
                    n=cur.rowcount
                    if(n==1):
                         mg="data saved"
                    else:
                        mg="data not saved"
                except pymysql.err.IntegrityError:
                    mg="it is already registration"
                return render_template("add_trainer.html",result=mg)
            else:
                print("this is get request")
                return render_template("add_trainer.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))





if __name__=="__main__":
  app.run(debug=True)
