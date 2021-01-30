import psycopg2
import hashlib
from db_util import DbUtil

class User:
  name = " "
  password = " "
  db_config = " "
  
  def __init__(self, name, password):
    self.name = name
    self.password = password
    self.params = DbUtil.read_db_config()
  
  def is_authenticated(self):
    sql_statement = 'SELECT * FROM users WHERE user_id = \'{0}\';'.format(self.name) 
    db_user = self.__execute_select_single(sql_statement)
    # is the password correct?
    hashed_password = hashlib.sha256(self.password.encode('utf-8')).hexdigest()
    return (hashed_password == db_user[1])

  # should return a list of hash maps, i.e. dictionaries
  def get_accounts(self):
    sql_statement = 'SELECT * FROM accounts WHERE user_id = \'{0}\';'.format(self.name)
    db_accounts = self.__execute_select_all(sql_statement)
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
    self.__execute_statement_and_commit(sql_statement)
    
  def change_account_password(self,new_password,service,login_name):
    sql_statement = '''UPDATE accounts
                       SET login_password = \'{0}\'
                       WHERE user_id = \'{1}\'
                         AND service = \'{2}\'
                         AND login_name = \'{3}\';'''.format(new_password,self.name,service,login_name)
    self.__execute_statement_and_commit(sql_statement)

  def __execute_statement_and_commit(self,sql_statement):
    conn = None
    try:
      conn = psycopg2.connect(**self.params)
      # create a cursor
      cur = conn.cursor()
      cur.execute(sql_statement)
      conn.commit()
      # close the communication with PostgreSQL
      cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
      print(error)
    finally:
      if conn is not None:
        conn.close()

  def __execute_select_single(self,sql_statement):
    conn = None
    result = None
    try:
      conn = psycopg2.connect(**self.params)
      # create a cursor
      cur = conn.cursor()
      cur.execute(sql_statement)
      result = cur.fetchone()
      # close the communication with PostgreSQL
      cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
      print(error)
    finally:
      if conn is not None:
        conn.close()
    return result

  def __execute_select_all(self,sql_statement):
    conn = None
    result = None
    try:
      conn = psycopg2.connect(**self.params)
      # create a cursor
      cur = conn.cursor()
      cur.execute(sql_statement)
      result = cur.fetchall()
      # close the communication with PostgreSQL
      cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
      print(error)
    finally:
      if conn is not None:
        conn.close()
    return result

  def delete_account(self,service,login_name):
    sql_statement = '''DELETE FROM accounts 
                        WHERE user_id = \'{0}\'
                          AND service = \'{1}\'
                          AND login_name = \'{2}\';'''.format(self.name,service,login_name)
    self.__execute_statement_and_commit(sql_statement)

