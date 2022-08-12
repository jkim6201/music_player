from flask_app import app
from flask import flash, render_template,redirect,session,request
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def log_and_reg():
    return render_template("log_and_reg.html")

@app.route('/login',methods=["POST"])
def login():
    #Validate login form
    if not User.validate_login(request.form):
        return redirect('/')
    user = User.get_user_by_email(request.form)
    if user:
        #if user exists, check if password matches
        if not bcrypt.check_password_hash(user.password,request.form["password"]):
            #if password did not match
            flash("Email/Password combination is incorrect")
            return redirect("/")
    
        #if password matched!
        session['user_id'] = user.id
        flash("Login was successful")
        return redirect("/dashboard")

    flash("Email is not tied to an account")
    return redirect("/")

@app.route('/register',methods=["POST"])
def register():
    #Validate register form
    if not User.validate_register(request.form):
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    print(pw_hash)
    register_data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash
    }

    user_id = User.register_user(register_data)
    session["user_id"] = user_id
    flash ("Registration was successful")
    return redirect("/dashboard")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')