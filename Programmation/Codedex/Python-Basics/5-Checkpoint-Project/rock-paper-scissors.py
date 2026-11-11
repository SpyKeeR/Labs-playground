"""Rock, Paper, Scissors is a classic game that resonates with folks from around the world.

Create a program where the user plays a round of Rock, Paper, Scissors against the computer.

The rules are as follows:

Rock beats Scissors.
Scissors beat Paper.
Paper beats Rock.
First, create a player and a computer variable.

Prompt the player to select number between 1 and 3 with input() and store it in player:

1 is for '✊' (Rock).
2 is for '✋' (Paper).
3 is for '✌️' (Scissors).
Then, use the random.randint() method to assign a number to the computer variable (1 to 3).

Lastly, use control flow to compare the user's choice and the computer's choice, determine the winner, and print out who won.

The output should look something like this:

===================
Rock Paper Scissors
===================

1) ✊
2) ✋
3) ✌️
Pick a number: 2

You chose: ✋
CPU chose: ✊
The player won!"""

# Write code below 💖
import random

player = 0
computer = 0

print("""
===================
Rock Paper Scissors
===================

1) ✊
2) ✋
3) ✌️
""")
player = int(input("Pick a number: "))
computer = random.randint(1,3)

player_choice = ""
computer_choice = ""

if computer == 1:
  computer_choice = "✊"
elif computer == 2:
  computer_choice = "✋"
elif computer == 3:
  computer_choice = "✌️"

if player == 1:
  player_choice = "✊"
elif player == 2:
  player_choice = "✋"
elif player == 3:
  player_choice = "✌️"

print()
print(f"You chose: {player_choice}")
print(f"CPU chose: {computer_choice}")

if player == 1:
  if computer == 1:
    print("It's a tie.")
  elif computer == 2:
    print("The computer won!")
  elif computer == 3:
    print("The player won!")
elif player == 2:
  if computer == 1:
    print("The player won!")
  elif computer == 2:
    print("It's a tie.")
  elif computer == 3:
    print("The computer won!")
elif player == 3:
  if computer == 1:
    print("The computer won!")
  elif computer == 2:
    print("The player won!")
  elif computer == 3:
    print("It's a tie.")