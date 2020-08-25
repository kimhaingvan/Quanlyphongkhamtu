import hashlib

from flask import request, redirect, flash, url_for
from flask_login import login_user

from QLPK import db
from QLPK.models import Users, Code, Quydinh


def LoginUser():
    if request.method == "POST":
        user_name = request.form.get("username")
        password = request.form.get("password", "")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        user = Users.query.filter(Users.user_name == user_name.strip(), Users.password == password).first()
        if user:
            login_user(user=user)

    return redirect("/admin")

def SignUpUser():
    if request.method == "POST":
        user_name = request.form.get("username")
        name = request.form.get("name")
        usercode = request.form.get("code")
        password = request.form.get("password", "")
        confirmpassword = request.form.get("confirmpassword", "")
        email = request.form.get("email")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        confirmpassword = str(hashlib.md5(confirmpassword.strip().encode("utf-8")).hexdigest())
        if password != confirmpassword:
            flash('Password not same.')
            return redirect(url_for('registerview.index'))
        user_code = Code.query.filter(Code.code_id == usercode, Code.is_active == 1).first()
        if not user_code:
            flash('Your code is wrong.')
            return redirect(url_for('registerview.index'))
        user = Users.query.filter(Users.email == email).first()
        if user:
            flash('Email address already exist.')
            return redirect(url_for('registerview.index'))
        new_user = Users(name=name, user_name=user_name, email=email, password=password, is_active=1, code_id=usercode)
        update_code = Code.query.get(usercode)
        update_code.is_active = 0
        db.session.add(new_user, update_code)
        db.session.commit()
    return redirect(url_for('login_admin'))


def GetAmountOfRules():
    print(len(Quydinh.query.all()))
    return len(Quydinh.query.all())
