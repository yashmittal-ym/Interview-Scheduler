from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail
import os
from werkzeug.utils import secure_filename
import re

app = Flask(__name__)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT ='465',
    MAIL_USE_SSL = True, 
    MAIL_USERNAME='hash8647@gmail.com',
    MAIL_PASSWORD='94percentage'
)
app.config['UPLOAD_FOLDER']='./static/'
mail=Mail(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///store.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Candidates(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    FName = db.Column(db.String(200), nullable=False)
    LName = db.Column(db.String(200), nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    Email = db.Column(db.String(200), nullable=False)

class Users(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(200), nullable=False)
    slot = db.Column(db.String(200), nullable=False)

class Interviews(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    user1 = db.Column(db.String(200), nullable=False)
    user2 = db.Column(db.String(200), nullable=False)
    slot = db.Column(db.Integer, nullable=False)
    link = db.Column(db.String(200), nullable=False)

user1="Yash"
user2="Yash"

@app.route('/', methods=['GET', 'POST'])
def index():
    global user1
    user1="Yash"
    global user2
    user2="Yash"
    inputTime=""
    if request.method=='POST':
        user1 = request.form['user1']
        user2 = request.form['user2']
        inputTime= request.form['inputTime'] 
        # print(inputTime)
    q1=Users.query.filter_by(user=user1).all()
    q2=Users.query.filter_by(user=user2).all()
    allCandidates=Candidates.query.all()
    if(user1==user2):
        return render_template('index.html', allSlots=[],user1=user1,user2=user2,allCandidates=allCandidates)
    mp = dict()
    for i in q1:
        if i.slot in mp.keys():
            mp[i.slot] += 1
        else:
            mp[i.slot] = 1
    for i in q2:
        if i.slot in mp.keys():
            mp[i.slot] += 1
        else:
            mp[i.slot] = 1
    slots=[]
    if(inputTime in mp):
        if(mp[inputTime]<1):
            return render_template('index.html', allSlots=[],user1=user1,user2=user2,allCandidates=allCandidates,err="Not Available")
    else:
        return render_template('index.html', allSlots=[],user1=user1,user2=user2,allCandidates=allCandidates,err="Not Available")
    for slot,cnt in mp.items():
        if(cnt>1):
            slots.append(slot)
    if(len(slots)==0):
        return render_template('index.html', allSlots=[],user1=user1,user2=user2,allCandidates=allCandidates)            
    return render_template('index.html', allSlots=slots,user1=user1,user2=user2,allCandidates=allCandidates)    

@app.route('/available', methods=['GET', 'POST'])
def available():
    slot=""
    if request.method=='POST':
        slot = request.form['slot']
    
    sno1=Candidates.query.filter_by(FName=user1).first()
    sno2=Candidates.query.filter_by(FName=user2).first()
    link=str(sno1.sno)+"-"+str(sno2.sno)
    meet=Interviews(user1=user1,user2=user2,slot=slot,link=link)
    db.session.add(meet)
    del1=Users.query.filter_by(user=user1,slot=slot).first()   
    del2=Users.query.filter_by(user=user2,slot=slot).first()    
    db.session.delete(del1)
    db.session.delete(del2)

    db.session.commit()
    q1=Candidates.query.filter_by(FName=user1).first()
    q2=Candidates.query.filter_by(FName=user2).first()
    mail.send_message("hello form interviewbit",sender="hash8647@gmail.com",recipients=[q1.Email,q2.Email], body="you interview is being scheduled at time slot "+ slot)
    allInterviews=Interviews.query.all() 
    return render_template('upcoming.html', allInterviews=allInterviews)

regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

@app.route('/addCandidate',methods=['GET', 'POST'])
def addTheCandidate():
    if request.method=='POST':
        FName = request.form['FName']
        LName = request.form['LName']
        Age   = request.form['Age']
        Email = request.form['Email']
        file = request.files['file1']
        if(re.search(regex, Email)):
            add=Candidates(FName=FName,LName=LName,Age=Age,Email=Email)
            db.session.add(add)
            db.session.commit()
            filename = secure_filename(FName+str(add.sno)+".pdf")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            for i in range(5):
                slot=str(i+8)+":00 - "+str(i+9)+":00"
                user=Users(user=FName,slot=slot)
                db.session.add(user)
                db.session.commit()
            mail.send_message("hello form interviewbit",sender="hash8647@gmail.com",recipients=[Email], body="you have been successfully regitered as a candidate!")
            allCandidates = Candidates.query.all() 
            return render_template('addCandidate.html', allCandidates=allCandidates)
        else:
            return render_template('addCandidate.html', allCandidates=[],err="INVALID_EMAIL")
    allCandidates = Candidates.query.all() 
    return render_template('addCandidate.html', allCandidates=allCandidates)
    

@app.route('/upcoming')
def Upcoming():
    allInterviews = Interviews.query.all() 
    return render_template('upcoming.html', allInterviews=allInterviews)

@app.route('/displayUsers')
def display():
    allUsers = Users.query.order_by(Users.user.desc()).all() 
    return render_template('displayUsers.html', allUsers=allUsers)

@app.route('/common/<string:name>')
def common(name):
    print(name)
    sno=name[0]
    del1 = Interviews.query.filter_by(sno=sno).first()
    x = name.split("-")
    print(x)
    if((del1.user1==x[1] and del1.user2==x[2]) or (del1.user1==x[2] and del1.user2==x[1])):
        return render_template('common.html',user1=del1.user1,user2=del1.user2)
    return  render_template('error.html')

@app.route('/delete/<int:sno>')
def delete(sno):
    del1 = Interviews.query.filter_by(sno=sno).first()
    user1=del1.user1
    user2=del1.user2
    slot=del1.slot
    add1=Users(user=user1,slot=slot)   
    add2=Users(user=user2,slot=slot)
    db.session.add(add1)
    db.session.add(add2)
    db.session.delete(del1)
    db.session.commit()
    return redirect("/")

@app.route('/deleteDb')
def deleteDb():
    db.session.query(Candidates).delete()
    db.session.query(Users).delete()
    db.session.query(Interviews).delete()
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=8000)