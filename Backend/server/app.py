from flask import Flask,render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'
db = SQLAlchemy(app)

#user table
class User(db.Model):
    username = db.Column(db.String(20),nullable=False, primary_key=True)
    password = db.Column(db.String(20),nullable=False)

    def __repr__(self):
        return '<user %r>' % self.username

#manager table
class Manager(db.Model):
    ManagerId = db.Column(db.String(20),nullable=False, primary_key=True)
    ManagerName = db.Column(db.String(20))


def managerInit():
    superMana=Manager(ManagerId="644132")
    db.session.add(superMana)
    db.session.commit()



#login page
@app.route('/', methods=['POST','GET'])
def index():
    if request.method=='POST':
        users=User.query.all()
        user_info=request.form['username']
        user_pass=request.form['password']

        for user in users:
            if(user.username==user_info and user.password==user_pass):
                return "successfully logged in!"
        return "no existing user, please sign up"
    else:
        users=User.query.all()
        return render_template('index.html',tasks=users)

#delete a user
@app.route('/delete/<usr>')    
def delete(usr):
    
    delete_usr=User.query.get_or_404(usr)

    try:
        db.session.delete(delete_usr)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an issue deleting user to database"


#update the user password
@app.route('/update/<usr>', methods=['GET','POST'])
def update(usr):
    usr_info=User.query.get_or_404(usr)

    if request.method == 'POST':
        usr_info.password=request.form['password']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue changing password to database"
        
    else:
        return render_template('update.html',task=usr_info)

#delete all users
@app.route('/deleteall')
def deleteall():
    users=User.query.all()

    try:
        for user in users:
            db.session.delete(user)
            db.session.commit()   
        return redirect('/')
        
    except:
         return "There was an issue clear database"

#sign up page
@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        user_info=request.form['username']
        user_pass=request.form['password']

        if(user_info!="" and user_pass!="" ):
            new_user=User(username=user_info,password=user_pass)
        else:
            return "Username and Password cannot be empty!"

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')

        except:
            return "There was an issue adding user to database"

    else:
        users=User.query.all()
        return render_template('signup.html',tasks=users)

# manager login
@app.route('/managerLogin',methods=['POST','GET'])
def managerlogin():
    managers=Manager.query.all()
    if request.method == 'POST':
        managerID=request.form['managerID']

        for manager in managers:
            if(manager.ManagerID==managerID):
                return "Manager Login Success"
        return "The manager ID is wrong"
    else:      
        return render_template('managerLogin.html',allmana=managers)




if __name__ == "__main__":
    app.run(debug=True)