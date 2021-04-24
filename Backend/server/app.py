from flask import Flask,render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'
db = SQLAlchemy(app)

class User(db.Model):
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(20))

    def __repr__(self):
        return '<user %r>' % self.username



@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        user_info=request.form['username']
        user_pass=request.form['password']
        new_user=User(username=user_info,password=user_pass)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')

        except:
            return "There was an issue adding user to database"

    else:
        users=User.query.all()
        return render_template('index.html',tasks=users)

@app.route('/delete/<usr>')    
def delete(usr):
    
    delete_usr=User.query.get_or_404(usr)

    try:
        db.session.delete(delete_usr)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an issue deleting user to database"


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

if __name__ == "__main__":
    app.run(debug=True)