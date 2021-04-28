from flask import Flask,render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Table, Column, Integer, ForeignKey

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'
db = SQLAlchemy(app)


#user table
class User(db.Model):
    username = db.Column(db.String(20),nullable=False, primary_key=True)
    password = db.Column(db.String(20),nullable=False)
    name = db.Column(db.String(20))
    address = db.Column(db.String(100))
    email = db.Column(db.String(40))
    trust = db.Column(db.Integer,default=0)
    untrust = db.Column(db.Integer,default=0)

    def __repr__(self):
        return '<user %r>' % self.username

#manager table
class Manager(db.Model):
    ManagerId = db.Column(db.String(20),nullable=False, primary_key=True)
    ManagerName = db.Column(db.String(20))

#book table
class Book(db.Model):
    ISBN = db.Column(db.Integer,nullable=False,primary_key=True)
    title = db.Column(db.String(30),nullable=False)
    page = db.Column(db.Integer)
    date = db.Column(db.DateTime,nullable=False, default=datetime.utcnow)
    publisher = db.Column(db.String(30), nullable=False)
    language = db.Column(db.String(30),nullable=False,default="English")
    stock = db.Column(db.Integer,nullable=False)
    price = db.Column(db.Float,nullable=False)

#author table
class Author(db.Model):
    __tablename__ = 'Author'

    name = db.Column(db.String(30),nullable=False)
    ISBN = db.Column(db.Integer,db.ForeignKey('book.ISBN', ondelete='CASCADE'),nullable=False)

    __table_args__ = (
    db.PrimaryKeyConstraint(
        name, ISBN,
        ),
    )

#order table
class Order(db.Model):
    ordernum = db.Column(db.Integer,nullable=False,primary_key=True)
    title = db.Column(db.String(30),nullable=False)
    copynum = db.Column(db.Integer,nullable=False)
    username = db.Column(db.String(30),db.ForeignKey('user.username', ondelete='CASCADE'),nullable=False)

#comment table
class Comment(db.Model):
    __tablename__ = 'comment'
    comment = db.Column(db.Integer,primary_key=True)
    ISBN = db.Column(db.Integer,db.ForeignKey('book.ISBN', ondelete='CASCADE'),nullable=False)
    username = db.Column(db.String(20),db.ForeignKey('user.username', ondelete='CASCADE'),nullable=False)
    text = db.Column(db.String(100))
    usefulscore = db.Column(db.Integer,default=1)
    comsocore = db.Column(db.Integer,default=5)

    __table_args__ = (
    db.UniqueConstraint(
        ISBN, username
        ),
    )

#useful score table
class Usefulscore(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    score = db.Column(db.Integer,default=1)
    comid = db.Column(db.String(20),db.ForeignKey('comment.comment', ondelete='CASCADE'),nullable=False)

def managerInit():
    superMana=Manager(ManagerId="644132",ManagerName="Matt")
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
                curuser=user.username
                return redirect(url_for('main',id=user.username))
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
        return redirect('/customerMana')
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
            return redirect('/customerMana')
        except:
            return "There was an issue changing password to database"
        
    else:
        return render_template('update.html',task=usr_info)

#update the stock
@app.route('/updateb/<isbn>', methods=['GET','POST'])
def updateb(isbn):
    book=Book.query.get_or_404(isbn)

    if request.method == 'POST':
        book.stock=request.form['stock']
        db.session.commit()
        return redirect('/bookMana')
       
        
    else:
        return render_template('updateb.html',nbook=book)

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
        name=request.form['name']
        email=request.form['email']
        address=request.form['address']

        if(user_info!="" and user_pass!="" ):
            new_user=User(username=user_info,password=user_pass,name=name,email=email,address=address)
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

#manager login
@app.route('/managerLogin',methods=['POST','GET'])
def managerlogin():
    managers=Manager.query.all()
    if request.method == 'POST':
        managerID=request.form['managerId']

        for manager in managers:
            if(manager.ManagerId==managerID):
                return redirect('/managerAdd')
        return "The manager ID is wrong"
    else:      
        return render_template('managerLogin.html',allmana=managers)

#manager add
@app.route('/managerAdd',methods=['POST','GET'])
def managerAdd():
    if request.method == 'POST':
        managerID=request.form['managerId']
        managerName=request.form['managerName']
        if(managerID!='' and managerName!=''):
            newmana=Manager(ManagerId=managerID, ManagerName=managerName)
        else:
            return "manager ID or name cannot be empty"
       
        try:
            db.session.add(newmana)
            db.session.commit()
            return redirect('/managerAdd')
        except:
            return "something wrong when adding new manager"
    else:
        managerss=Manager.query.all()
        return render_template('managerControl.html',managers=managerss)

#book add
@app.route('/bookAdd',methods=['POST','GET'])
def bookAdd():
    if request.method == 'POST':

        title=request.form['title']
        ISBN=request.form['ISBN']
        page=request.form['page']
        date=datetime.strptime(request.form['date'],'%Y-%m-%d')
        publisher=request.form['publisher']
        language=request.form['language']
        stock=request.form['stock']
        price=request.form['price']
        authors=request.form['authors']
        inauthors=authors.split(",")

        for author in inauthors:
            newauthor=Author(ISBN=ISBN,name=author)
            db.session.add(newauthor)
            db.session.commit()
        
        newbook=Book(ISBN=ISBN,title=title,page=page,date=date,publisher=publisher,language=language
        ,stock=stock,price=price)
        
        db.session.add(newbook)
        db.session.commit()
        return redirect('/bookAdd')

    else:
        return render_template('bookAdd.html')

@app.route('/customerMana')
def cusMana():
    customers=User.query.all()
    return render_template('customerManage.html',allCus=customers)

@app.route('/bookMana')
def bookMana():
    authors=Author.query.all()
    books=Book.query.all()
    return render_template('bookManage.html',allbook=books,allAuthors=authors)

@app.route('/main/<id>')
def main(id):
    username=id
    authors=Author.query.all()
    books=Book.query.order_by(Book.date).all()
    return render_template('main.html',allbook=books,allAuthors=authors,user=username)

@app.route('/oneBook/<isbn>/<id>')
def oneBook(isbn,id):
    book=Book.query.get_or_404(isbn)
    comments=Comment.query.all()
    return render_template("singleBook.html",nbook=book,user=id,allcom=comments)

@app.route('/order/<isbn>/<id>',methods=['POST','GET'])
def order(isbn,id):
    if request.method=="POST":
        nocop=request.form['nocopy']
        nbook=Book.query.get_or_404(isbn)
        if nbook.stock>=int(nocop):
            nbook.stock-=int(nocop)
            db.session.commit()
        else:
            return "book out of stock"
        newOrder=Order(title=nbook.title,copynum=nocop,username=id)
        db.session.add(newOrder)
        db.session.commit()
        return redirect(url_for('main',id=id))
    else:
        nbook=Book.query.get_or_404(isbn)
        return render_template('order.html',book=nbook,user=id)

@app.route('/orderInfo/<id>')
def orderInfo(id):
    orders=Order.query.all()
    return render_template('OrderInfo.html',user=id,allorder=orders)

@app.route('/profile/<id>')
def profile(id):
    profile=User.query.get_or_404(id)
    return render_template('profile.html',user=profile)

@app.route('/alluser/<id>')
def alluser(id):
    users=User.query.all()
    return render_template('other.html',alluser=users,user=id)

@app.route('/oneuser/<myid>/<viewid>',methods=['POST','GET'])
def oneuser(myid,viewid):
    viewi=User.query.get_or_404(viewid)
    return render_template('oneprofile.html',myuser=myid,viewuser=viewi)
 
@app.route('/addtrust/<myid>/<viewid>')
def addtrust(myid,viewid):
    viewi=User.query.get_or_404(viewid)
    viewi.trust+=1
    db.session.commit()
    return redirect(url_for('oneuser',myid=myid,viewid=viewid))

@app.route('/adduntrust/<myid>/<viewid>')
def adduntrust(myid,viewid):
    viewi=User.query.get_or_404(viewid)
    viewi.untrust+=1
    db.session.commit()
    return redirect(url_for('oneuser',myid=myid,viewid=viewid))

@app.route('/addcomment/<id>/<isbn>',methods=['POST','GET'])
def addcomment(id,isbn):
    if request.method=='POST':
        cscore=request.form['cscore']
        comment=request.form['text']
        newcomment=Comment(ISBN=isbn,username=id,text=comment,comsocore=int(cscore))
        db.session.add(newcomment)
        db.session.commit()

        return redirect(url_for('oneBook',isbn=isbn,id=id))
    else:
        return redirect(url_for('oneBook',isbn=isbn,id=id))

@app.route('/adduseful/<comid>/<isbn>/<id>',methods=['POST','GET'])
def adduseful(comid,isbn,id):
    if request.method=="POST":
        uscore=request.form['uscore']
        newuseful=Usefulscore(score=uscore,comid=comid)
        db.session.add(newuseful)
        db.session.commit()
        return redirect(url_for('oneBook',isbn=isbn,id=id))


if __name__ == "__main__":
    app.run(port=8000,debug=True)