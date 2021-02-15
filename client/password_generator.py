from random import randint

options = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

def get_generated_password(no_of_chars):
  res = ''
  for i in range(no_of_chars):
    r = randint(0,len(options)-1)
    res += options[r]
  return res
