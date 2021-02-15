from flask import Flask

api = Flask(__name__)

@api.route('/')
def index():
    return 'Welcome to your password manager"

@api.route('/login')
def login():
    pass

@api.route('/logout')
def logout():
    pass

@api.route('/<str:username>/accounts')
def accounts_for_user(username):
    pass

@api.route('/<str:username>/account/<int:account_id>')
def account_for_id(username, account_id):
    pass
