from menu import Menu

def main():
  # lazy exception hanling
  try:
    menu = Menu()
    menu.main_loop()
  except:
    print("Something went wrong...")

if __name__ == '__main__':
  main()
