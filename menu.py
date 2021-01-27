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
print(user.get_accounts())

answer = " "

while answer not in '12':
  print_menu()
  print()
  answer = input("choose: ")

print("Not yet implemented")
