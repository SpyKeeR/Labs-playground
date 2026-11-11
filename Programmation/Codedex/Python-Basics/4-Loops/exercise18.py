"""Let's continue on from the code above.

Create a guess.py program and type in the following:

guess = 0

while guess != 6:
  guess = int(input("Guess the number:  "))

print("You got it!")

Run the code a few times so that you understand what it does.

Let's make it so that it's the same guessing game, but there is a new limit to the number of tries (it was infinite before).

First, introduce a variable called tries at the top and give it a value of 0.

Then, add a second condition with the tries variable to the while loop using a relational operator."""

# Write code below 💖

guess = 0
tries = 0

while guess != 6 and tries < 5:
  tries += 1
  guess = int(input("Guess the number:  "))
if guess != 6:
  print("You tried too many times.")
else:
  print("You Got it!")