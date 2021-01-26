from configparser import ConfigParser

class DbUtil:
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
