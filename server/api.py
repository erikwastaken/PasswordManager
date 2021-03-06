from flask import Flask,request,session,abort,escape
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
    db_user = db_util.execute_select_single(sql_statement,p1=escape(content['username']))
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
        session['user_id'] = user['user_id']
        return json.dumps(user)
    return abort(403)

@api.route('/logout',methods=['GET','POST'])
def logout():
    session.pop('username',None)
    session.pop('user_id',None)
    return ''

@api.route('/users',methods=['POST'])
def create_user():
    content = request.get_json()
    sql_statement = '''INSERT INTO users (username, password, created_on) VALUES (%s, %s, current_timestamp)'''
    hashed_pw = hashlib.sha256(content['password'].encode('utf-8')).hexdigest()
    db_util.execute_statement_and_commit(sql_statement,p1=escape(content['username']), p2=hashed_pw)
    return content

@api.route('/users/<string:username>/accounts', methods=['GET','POST'])
def accounts_for_user(username):
    if not _is_logged_in(username):
        return abort(403)
    if request.method == 'GET':
        sql_statement = 'SELECT * FROM accounts WHERE user_id = %s'
        db_accounts = db_util.execute_select_all(sql_statement,p1=session['user_id'])
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
                p1=escape(content['user_id']),
                p2=escape(content['service']),
                p3=escape(content['login_name']),
                p4=escape(content['login_password']))
        return content

@api.route('/users/<string:username>/accounts/<int:account_id>', methods=['GET','PUT','DELETE'])
def account_for_id(username, account_id):
    if not _is_logged_in(username):
        return abort(403)
    if request.method == 'GET':
        pass
    if request.method == 'PUT':
        content = request.get_json()
        sql_statement = '''UPDATE accounts
                           SET login_name = %s, login_password = %s, last_changed_on = current_timestamp
                           WHERE account_id = %s;'''
        db_util.execute_statement_and_commit(sql_statement,p1=escape(content['login_name']),p2=escape(content['login_password']),p3=account_id)
        return request.get_json()
    if request.method == 'DELETE':
        sql_statement = '''DELETE FROM accounts 
                            WHERE account_id = %s;'''
        db_util.execute_statement_and_commit(sql_statement,p1=account_id)
        return ''

@api.route('/users/<string:username>',methods=['PUT','DELETE'])
def update_user(username):
    if not _is_logged_in(username):
        return abort(403)
    if request.method == 'PUT':
        content = request.get_json()
        hashed_password = hashlib.sha256(content['password'].encode('utf-8')).hexdigest()
        sql_statement = '''UPDATE users
                           SET password = %s
                           WHERE user_id = %s;'''
        db_util.execute_statement_and_commit(sql_statement,p1=hashed_password,p2=session['user_id'])
        return content
    if request.method == 'DELETE':
        # delete accounts
        sql_statement = '''DELETE FROM accounts
                           WHERE user_id = %s;'''
        db_util.execute_statement_and_commit(sql_statement,p1=session['user_id'])
        # delete user
        sql_statement = '''DELETE FROM users
                           WHERE user_id = %s;'''
        db_util.execute_statement_and_commit(sql_statement,p1=session['user_id'])
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

def _is_logged_in(username):
    return ('username' in session) and (username == session['username'])

if __name__ == '__main__':
    api.run(host='0.0.0.0')
