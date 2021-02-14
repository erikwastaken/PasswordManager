import hashlib
import db_util

class User:
  def __init__(self, name, password):
    self.name = name
    self.password = password
    db_util.read_db_config()
  
  def is_authenticated(self):
    sql_statement = 'SELECT * FROM users WHERE user_id = %s'
    db_user = db_util.execute_select_single(sql_statement,sql_params=self.name)
    if not db_user:
      return False
    # is the password correct?
    hashed_password = hashlib.sha256(self.password.encode('utf-8')).hexdigest()
    return (hashed_password == db_user[1])

  def is_master_password(self, pw_candidate):
    return pw_candidate == self.password

  # should return a list of hash maps, i.e. dictionaries
  def get_accounts(self):
    sql_statement = 'SELECT * FROM accounts WHERE user_id = \'{0}\';'.format(self.name)
    db_accounts = db_util.execute_select_all(sql_statement)
    res_accounts = []
    if db_accounts:
      for dba in db_accounts:
        account = {}
        account['user_id'] = dba[0]
        account['service'] = dba[1]
        account['login_name'] = dba[2]
        account['login_password'] = dba[3]
        res_accounts.append(account)
    return res_accounts

  def create_account(self,service, login_name, login_password):
    sql_statement = '''INSERT INTO accounts (user_id,service,login_name,login_password)
                       VALUES (\'{0}\',\'{1}\',\'{2}\',\'{3}\');'''.format(self.name,service,login_name,login_password) 
    db_util.execute_statement_and_commit(sql_statement)
    
  def change_account_password(self,new_password,service,login_name):
    sql_statement = '''UPDATE accounts
                       SET login_password = \'{0}\'
                       WHERE user_id = \'{1}\'
                         AND service = \'{2}\'
                         AND login_name = \'{3}\';'''.format(new_password,self.name,service,login_name)
    db_util.execute_statement_and_commit(sql_statement)

  def delete_account(self,service,login_name):
    sql_statement = '''DELETE FROM accounts 
                        WHERE user_id = \'{0}\'
                          AND service = \'{1}\'
                          AND login_name = \'{2}\';'''.format(self.name,service,login_name)
    db_util.execute_statement_and_commit(sql_statement)
  
  def change_master_password(self,new_master_password):
    hashed_password = hashlib.sha256(new_master_password.encode('utf-8')).hexdigest()
    sql_statement = '''UPDATE users
                       SET hashed_pw = \'{0}\'
                       WHERE user_id = \'{1}\';'''.format(hashed_password, self.name)
    db_util.execute_statement_and_commit(sql_statement)
