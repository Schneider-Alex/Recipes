from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import user, recipe
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/saveuser', methods=['POST'])
def adduser():
    if not user.User.validate_account(request.form):
        return redirect('/')
    else:
        if request.form['passwordcheck'] !=  request.form['password']:
            flash('passwords do not match!')
            return redirect('/')
        else:
            user.User.save(request.form)
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    useraccount=user.User.loginuser(request.form)
    if useraccount:
        if bcrypt.check_password_hash(useraccount.password, request.form['password'] ):
            session['id'] = useraccount.id
            return redirect(f"/dashboard")
        else:
            flash('Username or Password Incorrect!')
            return redirect ('/')
    else:
        return redirect ('/')


@app.route ('/dashboard')
def dashboardpage():
    data={
                'id' : session['id']
            }
    all_recipes = recipe.Recipe.get_all()
    return render_template('dashboard.html',user=user.User.get_one(data),all_recipes=all_recipes)

@app.route('/logout', methods=['POST','GET'])
def logout():
    session.clear()
    return redirect('/')
