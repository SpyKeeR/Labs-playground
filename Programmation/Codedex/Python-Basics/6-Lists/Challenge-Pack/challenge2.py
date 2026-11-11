"""Instructions
Are you feeling lucky? Let's replicate a small lottery with Python lists and the random module. 🤑

Create empty lists my_numbers & winning_numbers.

Loop over range(0,5), populate both lists with five random numbers between 1-69.

Outside the loop, add to both lists one more random number between 1-26.

Print the my_numbers and winning_numbers lists.

My Numbers: [59, 66, 28, 52, 30, 12]
Winning Numbers: [26, 27, 37, 35, 47, 8]"""

# Write code below 💖
import random

my_numbers = []
winning_numbers = []
for i in range(0,5):
  my_numbers.append(random.randint(1,69))
  winning_numbers.append(random.randint(1,69))
my_numbers.append(random.randint(1,26))
winning_numbers.append(random.randint(1,26))

print("My numbers: " + str(my_numbers))
print("Winning numbers: " + str(winning_numbers))