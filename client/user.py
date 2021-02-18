import hashlib
import requests
import json

class User:
  def __init__(self, name, password, base_url='http://localhost:5000'):
    self.name = name
    self.password = password
    self.base_url = base_url
    self.session = requests.Session()
    
  def is_authenticated(self):
    payload = {"username": self.name, "password": self.password}
    uri = self.base_url + '/login'
    response = self.session.post(uri, json=payload)
    return response.status_code == requests.codes.ok

  def is_master_password(self, pw_candidate):
    return pw_candidate == self.password

  def get_accounts(self):
    uri = self.base_url + '/users/{0}/accounts'.format(self.name)
    response = self.session.get(uri)
    return response.json()['accounts']

  def create_account(self,service, login_name, login_password):
    sql_statement = '''INSERT INTO accounts (user_id,service,login_name,login_password)
                       VALUES (%s,%s,%s,%s);''' 
    db_util.execute_statement_and_commit(sql_statement,p1=self.name,p2=service,p3=login_name,p4=login_password)
    
  def change_account_password(self,new_password,service,login_name):
    sql_statement = '''UPDATE accounts
                       SET login_password = %s
                       WHERE user_id = %s 
                         AND service = %s
                         AND login_name = %s;'''
    db_util.execute_statement_and_commit(sql_statement,p1=new_password,p2=self.name,p3=service,p4=login_name)

  def delete_account(self,service,login_name):
    sql_statement = '''DELETE FROM accounts 
                        WHERE user_id = %s
                          AND service = %s 
                          AND login_name = %s;'''
    db_util.execute_statement_and_commit(sql_statement,p1=self.name,p2=service,p3=login_name)
  
  def change_master_password(self,new_master_password):
    hashed_password = hashlib.sha256(new_master_password.encode('utf-8')).hexdigest()
    sql_statement = '''UPDATE users
                       SET hashed_pw = %s
                       WHERE user_id = %s;'''
    db_util.execute_statement_and_commit(sql_statement,p1=hashed_password,p2=self.name)
