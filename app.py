from flask import Flask, request,render_template, redirect,session,jsonify,url_for
from flask_sqlalchemy import SQLAlchemy
import bcrypt

#solve all the errors in this code  

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


    def __init__(self,email,password,name):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))

with app.app_context():
    db.create_all()

class PasswordManager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(520), nullable=False)
    title = db.Column(db.String(520), nullable=False)
    password = db.Column(db.String(520), nullable=False)


with app.app_context():
    db.create_all()

@app.route("/")
def index():
    passwordlist = PasswordManager.query.filter_by().all()
    return render_template('index.html', passwordlist=passwordlist)    

@app.route("/add",methods=["POST"])
def add():
    email = request.form['email']
    title = request.form['title']
    password = request.form['password']
    new_password_details = PasswordManager(email=email,title=title,password=password)
    db.session.add(new_password_details)
    db.session.commit()
    print(new_password_details.email)
    
    return redirect('/dashboard')



@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # handle request
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(name=name,email=email,password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    
    return render_template('register.html')


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['email'] = user.email
            return redirect('./dashboard')
        else:
            return render_template('login.html',error='Invalid user')
    return render_template('login.html')


@app.route('/generater',methods=['POST'])
def generater():
    
    return render_template('generater.html')


# @app.route('/dashboard')
# def dashboard():
#     if session['email']:
#         user = PasswordManager.query.filter_by(email=session['email']).first()
#         passwordlist = PasswordManager.query.filter_by().all()
#         user = PasswordManager.query.filter_by(email=session['email']).first()
#         return render_template('dashboard.html',user=user,passwordlist = passwordlist)
    
#     return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        user = PasswordManager.query.filter_by(email=session['email']).first()
        passwordlist = PasswordManager.query.filter_by().all()


@app.route('/edit_password_name/<int:id>', methods=['GET', 'POST'])
def edit_password_name(id):
    # This code block is handling the editing of the name of a password in the database.
    password = Password.query.get(id)
    if password:
        if request.method == 'POST':
            name = request.form['name']
            password.name = name
            db.session.commit()
            flash('Password name edited successfully!', 'success')
            return redirect(url_for('index'))
        return render_template('edit_password_name.html', password=password)
    else:
        flash('Password not found', 'danger')
        return redirect(url_for('dashboard'))

@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
  password = PasswordManager.query.get(id)
  password.website = request.form['website'] 
  password.username = request.form['username']
  password.password = request.form['password']
  db.session.commit()
  return "Password updated" 


@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)