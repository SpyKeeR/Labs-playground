"""When you pull up to a drive-thru like McDonald's, you can order food by saying item numbers.

For example, a Happy Meal might be a #3!



Create a drive_thru.py program with your favorite fast food chain's menu.

Define a get_item() function that takes in one parameter, the number of the item you want to order, and returns the name of that item!

For example, if you called the function with:

Argument value 1, it could return '🍔 Cheeseburger'.
Argument value 2, it could return '🍟 Fries'.
Argument value 3, it could return '🥤 Soda'.
Argument value 4, it could return '🍦 Ice Cream'.
Argument value 5, it could return '🍪 Cookie'.
Make sure to call this function a few times to make sure that it works!

Lastly, let's do the following:

Create a welcome menu and put that in a welcome() function.
Create a main program that takes in user input with input()."""

# Write code below 💖

items = [
'🍔 Cheeseburger',
'🍟 Fries',
'🥤 Soda',
'🍦 Ice Cream',
'🍪 Cookie'
]

def get_item(item):
  return items[item-1]

def welcome():
  print("""
  =============================
  Welcome to the Drive Thru !
  What is your Choice ?
  =============================
  """)

welcome()
option = int(input('What would you like to order? '))
print(get_item(option))