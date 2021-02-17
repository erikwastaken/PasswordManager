from configparser import ConfigParser
import psycopg2


def get_configuration(section,filename='server/database.ini'):
  parser = ConfigParser()
  parser.read(filename)
  config = {}
  if parser.has_section(section):
    contents = parser.items(section)
    for param in contents:
      config[param[0]] = param[1]
  else:
    raise Exception('Section {0} not found in file {1}'.format(section,filename))
  return config

params = get_configuration(section='postgresql')

def execute_statement_and_commit(sql_statement,**sql_params):
  conn = None
  try:
    conn = psycopg2.connect(**params)
    # create a cursor
    cur = conn.cursor()
    cur.execute(sql_statement,list(sql_params.values()))
    conn.commit()
    # close the communication with PostgreSQL
    cur.close()
  except (Exception, psycopg2.DatabaseError) as error:
    print(error)
  finally:
    if conn is not None:
      conn.close()

def execute_select_single(sql_statement,**sql_params):
  conn = None
  result = None
  try:
    conn = psycopg2.connect(**params)
    # create a cursor
    cur = conn.cursor()
    cur.execute(sql_statement,list(sql_params.values()))
    result = cur.fetchone()
    # close the communication with PostgreSQL
    cur.close()
  except (Exception, psycopg2.DatabaseError) as error:
    print(error)
  finally:
    if conn is not None:
      conn.close()
  return result

def execute_select_all(sql_statement,**sql_params):
  conn = None
  result = None
  try:
    conn = psycopg2.connect(**params)
    # create a cursor
    cur = conn.cursor()
    cur.execute(sql_statement,list(sql_params.values()))
    result = cur.fetchall()
    # close the communication with PostgreSQL
    cur.close()
  except (Exception, psycopg2.DatabaseError) as error:
    print(error)
  finally:
    if conn is not None:
      conn.close()
  return result
