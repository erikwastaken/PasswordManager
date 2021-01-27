import getpass
from user import User

def print_menu():
  print("1 - create password")
  print("2 - get password")

def is_input_clean(word):
  return word.isalnum()

print()
print("Welcome to your password_manager")
print()
print("Please log in")
print()

user_name = input("User: ")
while not is_input_clean(user_name):
  print("Entered user name contains characters which are not allowed")
  print("Please try again")
  user_name = input("User: ")

password = getpass.getpass("Password: ")
while not is_input_clean(password):
  print("Entered password contains characters which are not allowed")
  print("Please try again")
  password = getpass.getpass("Password: ")

user = User(user_name, password)
print(user.is_authenticated())
if not user.is_authenticated():
  raise Exception('User or password incorrect')

answer = " "
while answer not in '12':
  print_menu()
  print()
  answer = input("choose: ")

if answer == '1':
  print("Not yet implemented")
elif answer == '2':
  accounts = user.get_accounts()
  for a in accounts:
    print('{0} | {1}'.format(a['site'], a['password']))
