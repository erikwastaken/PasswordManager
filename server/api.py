from flask import Flask,request,session,abort
import json
import db_util
import hashlib

api = Flask(__name__)

api.secret_key = db_util.get_configuration(section='apikey')['skey']

@api.route('/')
def index():
    if 'username' in session:
        return 'Welcome to your password manager'
    return 'Login first'

@api.route('/login', methods=['POST'])
def login():
    content = request.get_json()
    sql_statement = 'SELECT * FROM users WHERE username = %s'
    db_user = db_util.execute_select_single(sql_statement,p1=content['username'])
    if not db_user:
        return abort(403)
    user = {}
    user['user_id'] = db_user[0]
    user['username'] = db_user[1]
    user['password'] = db_user[2]
    # is the password correct?
    hashed_password = hashlib.sha256(content['password'].encode('utf-8')).hexdigest()
    if hashed_password == user['password']:
        session['username'] = content['username']
        return json.dumps(user)
    return abort(403)

@api.route('/logout',methods=['GET','POST'])
def logout():
    session.pop('username',None)
    return ''

@api.route('/<string:username>/accounts', methods=['GET','POST'])
def accounts_for_user(username):
    if not _is_logged_in(username):
        return abort(403)
    if request.method == 'GET':
        sql_statement = 'SELECT * FROM users WHERE username = %s'
        db_user = db_util.execute_select_single(sql_statement,p1=username)
        sql_statement = 'SELECT * FROM accounts WHERE user_id = %s'
        db_accounts = db_util.execute_select_all(sql_statement,p1=db_user[0])
        res_accounts = []
        if db_accounts:
            for dba in db_accounts:
                account = {}
                account['account_id'] = dba[0]
                account['user_id'] = dba[1]
                account['service'] = dba[2]
                account['login_name'] = dba[3]
                account['login_password'] = dba[4]
                account['created_on'] = dba[5]
                account['last_changed_on'] = dba[6]
                res_accounts.append(account)
        content = {}
        content['accounts'] = res_accounts
        # default necessary, because datetime is not JSON serializable
        return json.dumps(content,default=str)
    if request.method == 'POST':
        content = request.get_json()
        sql_statement = '''INSERT INTO accounts (user_id,service,login_name,login_password,created_on)
                           VALUES (%s,%s,%s,%s,current_timestamp);''' 
        db_util.execute_statement_and_commit(
                sql_statement,
                p1=content['user_id'],
                p2=content['service'],
                p3=content['login_name'],
                p4=content['login_password'])
        return content

@api.route('/<string:username>/account/<int:account_id>', methods=['GET','PUT','DELETE'])
def account_for_id(username, account_id):
    if not _is_logged_in(username):
        return abort(403)
    if request.method == 'GET':
        pass
    if request.method == 'PUT':
        pass
    if request.method == 'DELETE':
        pass

def _is_logged_in(username):
    return ('username' in session) and (username == session['username'])
