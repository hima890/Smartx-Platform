import json, database, base64, os, binascii
from flask import Blueprint, render_template, jsonify, redirect, request
from .users import user


main = Blueprint('main', __name__)
# Login dic
logged_in = {}
api_loggers = {}


@main.route('/')
def home():
    return render_template('home.html', title='HOME')


@main.route("/login", methods=['GET', 'POST'])
def login():
    error = ""
    if request.method == 'POST':
        user = user.user(request.form['username'], request.form['password'])
        if user.authenticated:
            user.session_id = str(binascii.b2a_hex(os.urandom(15)))
            logged_in[user.username] = {"object": user}
            return redirect('/overview/{}/{}'.format(request.form['username'], user.session_id))
        else:
            error = "invalid Username or Passowrd"
       
    return render_template('Login.htm', error=error)
