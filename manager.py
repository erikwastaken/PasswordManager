import psycopg2
from configparser import ConfigParser

def read_db_config(filename='database.ini',section='postgresql'):
  parser = ConfigParser()
  parser.read(filename)

  # get section, default to postgresql
  db = {}
  if parser.has_section(section):
    params = parser.items(section)
    for param in params:
      db[param[0]] = param[1]
  else:
    raise Exception('Section {0} not found in file {1}'.format(section,filename))
  return db

def get_version():
        conn = None
        try:
          params = read_db_config()
          print('Connecting to the PostgreSQL database...')
          conn = psycopg2.connect(**params)

          # create a cursor
          cur = conn.cursor()

          print('PostgreSQL database version: ')
          cur.execute('SELECT version()')

          db_version = cur.fetchone()
          print(db_version)

          # close the communication with PostgreSQL
          cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
          print(error)
        finally:
          if conn is not None:
            conn.close()
            print('Database connection closed.')

def get_all_accounts_for_userid(id):
  conn = None
  print('Retrieving all accounts...')
  try:
          params = read_db_config()
          print('Connecting to the PostgreSQL database...')
          conn = psycopg2.connect(**params)

          # create a cursor
          cur = conn.cursor()

          cur.execute('SELECT * FROM accounts WHERE userid = \'{0}\';'.format(id))

          accounts = cur.fetchone()
          print(accounts)  

          # close the communication with PostgreSQL
          cur.close()

  except (Exception, psycopg2.DatabaseError) as error:
          print(error)
  finally:
          if conn is not None:
            conn.close()
         
if __name__ == '__main__':
  get_all_accounts_for_userid('erik')
