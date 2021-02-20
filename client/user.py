import hashlib
import requests
import json

class User:
  @staticmethod
  def create_user(name,password,base_url='http://localhost:5000'):
    uri = base_url + '/users'
    payload = {'username': name, 'password': password}
    response = requests.post(uri,json=payload)
    return response.status_code

  def __init__(self, name, password, base_url='http://localhost:5000'):
    self.name = name
    self.password = password
    self.base_url = base_url
    self.session = requests.Session()
    self.user_id = 0
    self.accounts = []

  def is_authenticated(self):
    payload = {"username": self.name, "password": self.password}
    uri = self.base_url + '/login'
    response = self.session.post(uri, json=payload)
    self.user_id = response.json()['user_id']
    return response.status_code == requests.codes.ok

  def is_master_password(self, pw_candidate):
    return pw_candidate == self.password

  def get_accounts(self):
    uri = self.base_url + '/users/{0}/accounts'.format(self.name)
    response = self.session.get(uri)
    self.accounts = response.json()['accounts']
    return self.accounts

  def create_account(self,service, login_name, login_password):
    uri = self.base_url + '/users/{0}/accounts'.format(self.name)
    payload = {'user_id': self.user_id,
               'service': service,
               'login_name': login_name,
               'login_password': login_password }
    response = self.session.post(uri,json=payload)
    return response.status_code

  def change_account_password(self,index,new_password):
    uri = self.base_url + '/users/{0}/accounts/{1}'.format(self.name,self.accounts[index]['account_id'])
    payload = { 'login_name': self.accounts[index]['login_name'],
                'login_password': new_password }
    response = self.session.put(uri,json=payload)
    return response.status_code

  def delete_account(self,index):
    uri = self.base_url + '/users/{0}/accounts/{1}'.format(self.name,self.accounts[index]['account_id'])
    response = self.session.delete(uri)
    return response.status_code

  def change_master_password(self,new_master_password):
    uri = self.base_url + '/users/{}'.format(self.name)
    payload = { 'password': new_master_password }
    response = self.session.put(uri,json=payload)

  def delete_user(self,username,password):
    if username == self.name and password == self.password:
      uri = self.base_url + '/users/{}'.format(self.name)
      response = self.session.delete(uri)
      return response.status_code
    else:
      return 403
