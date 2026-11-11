"""Before we dive deep into while loop, let's see a demo using a bank's ATM. 🏦

Create an enter_pin.py program and type in the following:

print('BANK OF CODÉDEX')

pin = int(input('Enter your PIN: '))

while pin != 1234:
  pin = int(input('Incorrect PIN. Enter your PIN again: '))

if pin == 1234:
  print('PIN accepted!')
Next, press the "Run" button to see the messages print to the terminal.

Try the following in the terminal on the right 👉:

Type 1111 and then the enter key.
Type 2023 and then the enter key.
Type 1991 and then the enter key.
Type 1234 and then the enter key.
Were you able to get access to the ATM?"""

# Write code below 💖

print('BANK OF CODÉDEX')

pin = int(input('Enter your PIN: '))

while pin != 1234:
  pin = int(input('Incorrect PIN. Enter your PIN again: '))

if pin == 1234:
  print('PIN accepted!')