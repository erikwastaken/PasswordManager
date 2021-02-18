import hashlib
import db_util
import json

class User:
  def __init__(self, name, password):
    self.name = name
    self.password = password
    db_util.get_configuration(section='postgresql')
  
  def is_authenticated(self):
    sql_statement = 'SELECT * FROM users WHERE user_id = %s'
    db_user = db_util.execute_select_single(sql_statement,p1=self.name)
    if not db_user:
      return False
    # is the password correct?
    hashed_password = hashlib.sha256(self.password.encode('utf-8')).hexdigest()
    return (hashed_password == db_user[1])

  def is_master_password(self, pw_candidate):
    return pw_candidate == self.password

  # should return a JSON string
  def get_accounts(self):
    sql_statement = 'SELECT * FROM accounts WHERE user_id = %s'
    db_accounts = db_util.execute_select_all(sql_statement,p1=self.name)
    res_accounts = []
    if db_accounts:
      for dba in db_accounts:
        account = {}
        account['user_id'] = dba[0]
        account['service'] = dba[1]
        account['login_name'] = dba[2]
        account['login_password'] = dba[3]
        res_accounts.append(account)
    content = {}
    content['accounts'] = res_accounts
    return json.dumps(content)

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
