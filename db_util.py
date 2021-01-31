from configparser import ConfigParser
import psycopg2


def read_db_config(filename='database.ini',section='postgresql'):
  parser = ConfigParser()
  parser.read(filename)
  # get section, default to postgresql
  db = {}
  if parser.has_section(section):
    contents = parser.items(section)
    for param in contents:
      db[param[0]] = param[1]
  else:
    raise Exception('Section {0} not found in file {1}'.format(section,filename))
  return db

params = read_db_config()

def execute_statement_and_commit(sql_statement):
  conn = None
  try:
    conn = psycopg2.connect(**params)
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

def execute_select_single(sql_statement):
  conn = None
  result = None
  try:
    conn = psycopg2.connect(**params)
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

def execute_select_all(sql_statement):
  conn = None
  result = None
  try:
    conn = psycopg2.connect(**params)
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
