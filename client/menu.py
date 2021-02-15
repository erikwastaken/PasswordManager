import getpass
import pyperclip
from user import User
import password_generator
import json

class WrongMasterData(Exception):
  pass

class Menu:
  user = None
  
  def main_loop(self):
    try:
      self.login()
      exit = False
      while exit == False:
        self.display_menu()
        exit = ('Y' == input('Exit? (Y/N) ').upper())
    except WrongMasterData as e:
      print(e)
    print("Goodbye")

  def display_menu(self):
    answer = " "
    while answer not in '123456qQ':
      print("1 - create new login account")
      print("2 - get password")
      print("3 - change password")
      print("4 - delete login account")
      print("5 - change master password")
      print("6 - generate password")
      print("q - quit")
      print()
      answer = input("choose: ")
    print()
    if answer == '1':
      self.__create_new_account()
    elif answer == '2':
      self.__get_password()
    elif answer == '3':
      self.__change_password() 
    elif answer == '4':
      self.__delete_login()
    elif answer == '5':
      self.__change_master_password()
    elif answer == '6':
      self.__generate_password()
    elif answer.upper() == 'Q':
      return

  @staticmethod
  def __is_input_clean(word):
    return word.isalnum()
  
  def login(self):
    print()
    print("Welcome to your password_manager")
    print()
    print("Please log in")
    print()
    user_name = Menu.__get_clean_input_for_field("User")
    password = Menu.__get_clean_password()

    self.user = User(user_name, password)
    if not self.user.is_authenticated():
      raise WrongMasterData('User or password incorrect')
  
  @staticmethod
  def __get_clean_input_for_field(fieldname):
    value = input("{0}: ".format(fieldname))
    while not Menu.__is_input_clean(value):
      print("Entered {0} contains characters which are not allowed".format(fieldname))
      print("Please try again")
      value = input("{0}: ".format(fieldname))
    return value

  @staticmethod
  def __get_clean_password():
    password = getpass.getpass("Password: ")
    while not Menu.__is_input_clean(password):
      print("Entered password contains characters which are not allowed")
      print("Please try again")
      password = getpass.getpass("Password: ")
    return password

  def __display_accounts(self):
    c = 0
    accounts = json.loads(self.user.get_accounts())['accounts']
    for a in accounts:
      print('{0} | {1} | {2}'.format(c,a['service'], a['login_name']))
      c += 1

  def __create_new_account(self):
    service = Menu.__get_clean_input_for_field("Service")
    login_name = Menu.__get_clean_input_for_field("Login Name")
    gen_pass = ' '
    while gen_pass not in 'YN':
      gen_pass = input('Generate Password? [Y/N] ').upper()
    if gen_pass == 'Y':
      self.__generate_password()
    login_password = Menu.__get_clean_input_for_field("Password")
    self.user.create_account(service,login_name,login_password)

  def __get_password(self):
    self.__display_accounts()
    print()
    index = input("Choose password: ")
    print()
    print("1 - display password")
    print("2 - copy password to clipboard")
    i = input("Choose: ")
    if i == '1':
      print(self.user.get_accounts()[int(index)]['login_password'])
    elif i == '2':
      pyperclip.copy(self.user.get_accounts()[int(index)]['login_password'])
      print("Password copied to clipboard")
    else:
      print("wrong input")
  
  def __change_password(self):
    self.__display_accounts()
    print()
    index = int(input("Which password should be updated? "))
    gen_pass = ' '
    while gen_pass not in 'YN':
      gen_pass = input('Generate Password? [Y/N] ').upper()
    if gen_pass == 'Y':
      self.__generate_password()
    new_password = Menu.__get_clean_input_for_field("Password")
    service = self.user.get_accounts()[index]['service']
    login_name = self.user.get_accounts()[index]['login_name']
    self.user.change_account_password(new_password,service,login_name)
    print("Password for {0} changed to {1}".format(service,new_password))

  def __delete_login(self):
    self.__display_accounts()
    print()
    index = int(input("Which password should be deleted? "))
    service = self.user.get_accounts()[index]['service']
    login_name = self.user.get_accounts()[index]['login_name']
    confirmation_answer = input("Are you sure that you want to delete the account for service {0}? Y/N ".format(service))
    if confirmation_answer.upper() == 'Y':
      self.user.delete_account(service,login_name)
      print("Account for service {0} has been deleted.".format(service))

  def __change_master_password(self):
    print()
    print("Enter current master password:")
    curr_master_pw = Menu.__get_clean_password()
    if not self.user.is_master_password(curr_master_pw):
      raise WrongMasterData("Wrong master password")
    print("Enter new master password:")
    new_password = Menu.__get_clean_password()
    print("Confirm new master password:")
    confirmation = Menu.__get_clean_password()
    if new_password == confirmation:
      self.user.change_master_password(new_password)
      print("Master password has been changed")
    else:
      print("Confirmation failed")
  
  def __generate_password(self):
    print()
    length = int(input("How many characters should the password have? "))
    gen_pw = password_generator.get_generated_password(length)
    print('Generated password: {0}'.format(gen_pw))