import getpass
import pyperclip
from user import User

class Menu:
  user = None
  
  def main_loop(self):
    self.login()
    exit = False
    while exit == False:
      self.display_menu()
      exit = ('Y' == input('Exit? (Y/N) ').upper())
    print("Goodbye")

  def display_menu(self):
    answer = " "
    while answer not in '12qQ':
      print("1 - create password")
      print("2 - get password")
      print("q - quit")
      print()
      answer = input("choose: ")
    print()
    if answer == '1':
      print("Not yet implemented")
    elif answer == '2':
      self.__display_accounts()
      print()
      index = input('Copy password to clipboard: ')
      pyperclip.copy(self.user.get_accounts()[int(index)]['login_password'])
    elif answer.upper() == 'Q':
      return

  def __is_input_clean(word):
    return word.isalnum()
  
  def login(self):
    print()
    print("Welcome to your password_manager")
    print()
    print("Please log in")
    print()

    user_name = input("User: ")
    while not Menu.__is_input_clean(user_name):
      print("Entered user name contains characters which are not allowed")
      print("Please try again")
      user_name = input("User: ")

    password = getpass.getpass("Password: ")
    while not Menu.__is_input_clean(password):
      print("Entered password contains characters which are not allowed")
      print("Please try again")
      password = getpass.getpass("Password: ")

    self.user = User(user_name, password)
    if not self.user.is_authenticated():
      raise Exception('User or password incorrect')

  def __display_accounts(self):
    c = 0
    for a in self.user.get_accounts():
      print('{0} | {1} | {2}'.format(c,a['service'], a['login_name']))
      c += 1

