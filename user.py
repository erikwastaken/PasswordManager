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
  
  def is_authenticated():
    conn = None
    db_user = None
    try:
      conn = psycopg2.connect(**self.params)
      # create a cursor
      cur = conn.cursor()
      cur.execute('SELECT * FROM users WHERE name = \'{0}\';'.format(self.name))
      db_user = cur.fetchone()
      # close the communication with PostgreSQL
      cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
      print(error)
    finally:
      if conn is not None:
        conn.close()
    # is the password correct?
    hashed_password = hashlib.sha256(self.password.encode('utf-8')).hexdigest()
    return (hashed_password == db_user)

  # should return a list of hash maps, i.e. dictionaries
  def get_accounts(self):
    conn = None
    db_accounts = None
    try:
      conn = psycopg2.connect(**self.params)
      # create a cursor
      cur = conn.cursor()
      cur.execute('SELECT * FROM accounts WHERE userid = \'{0}\';'.format(self.name))
      db_accounts = cur.fetchmany()
      # close the communication with PostgreSQL
      cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
      print(error)
    finally:
      if conn is not None:
        conn.close()
    res_accounts = []
    if db_accounts:
      for dba in db_accounts:
        account = {}
        account['userid'] = dba[0]
        account['site'] = dba[1]
        account['password'] = dba[2]
        res_accounts.append(account)
    return res_accounts
