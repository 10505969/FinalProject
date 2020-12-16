from flask import Flask,request, jsonify, render_template, redirect, url_for
from Data import User,session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import CreateForm, LoginForm
from sqlalchemy import and_

app = Flask(__name__)
app.config['SECRET_KEY'] = 'filesystem'

#Test Login start

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def user_loader(user_id):
    #if user_id is not None:
    return session.query(User).get(user_id)
    #return None

@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    return redirect(url_for('login'))

#Test Login end


#Business Layer

def loginCheck(emailInput, passwordInput):
    user = User(email=emailInput, password=passwordInput)
    if len(user.getUser()) > 0:
        return True
    else:
        return False

def verifyEmail(emailInput):
    user = User(email=emailInput)
    if len(user.checkEmail()) > 0:
        return False
    else:
        return True

def addUser(emailInput, passwordInput):
    user = User(email=emailInput, password=passwordInput)
    if loginCheck(emailInput, passwordInput) == False:
        user.addUser()


@app.route('/')
@app.route("/home")
@app.route("/index")
@login_required
def home():
    return render_template("index.html")

@app.route("/about")
@login_required
def about():
  return render_template("about.html")


@app.route('/login', methods=['GET','POST'])
def login():
    errorMsg = False
    form = LoginForm()
    if form.validate_on_submit():
        user = session.query(User).filter(and_(User.email==form.username.data,User.password==form.password.data)).first()
        if user:
            errorMsg = False
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('home'))
        else:
            errorMsg = True
    return render_template('login.html', form=form, errorMsg=errorMsg)

        #     errorMsg = False
        #     return redirect(url_for('home'))
        # else:
        #     errorMsg = True

@app.route('/create', methods=['GET','POST'])
def createAcc():
    errorMsg = False
    form = CreateForm()
    if form.validate_on_submit():
        user = User(email=form.username.data, password=form.password.data)
        if verifyEmail(form.username.data) is True:
            errorMsg = False
            session.add(user)
            session.commit()
            login_user(user)
            return redirect(url_for('home'))
        else:
            errorMsg = True
    return render_template('createaccount.html', form=form, errorMsg=errorMsg)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
