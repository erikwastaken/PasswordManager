from flask import Flask,request,session,abort
import json
import db_util
import hashlib

api = Flask(__name__)
api.secret_key = b'\xe5\xd7\x0c\x04\xa3\xd3\xa4\x91b\x84-1\xc4\t\xd0\xc7' 

@api.route('/')
def index():
    if 'username' in session:
        return 'Welcome to your password manager'
    return 'Login first'

@api.route('/login', methods=['POST'])
def login():
    content = request.get_json()
    sql_statement = 'SELECT * FROM users WHERE user_id = %s'
    db_user = db_util.execute_select_single(sql_statement,p1=content['username'])
    if not db_user:
        return abort(403)
    # is the password correct?
    hashed_password = hashlib.sha256(content['password'].encode('utf-8')).hexdigest()
    if hashed_password == db_user[1]:
        session['username'] = content['username']
        return content
    return abort(403)

@api.route('/logout',methods=['GET','POST'])
def logout():
    session.pop('username',None)
    return ''

@api.route('/<string:username>/accounts')
def accounts_for_user(username):
    pass

@api.route('/<string:username>/account/<int:account_id>')
def account_for_id(username, account_id):
    pass
