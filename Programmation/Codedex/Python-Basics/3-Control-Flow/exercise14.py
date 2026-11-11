"""
The Magic 8 Ball is a popular office toy and children's toy invented in the 1940s for fortune-telling and advice seeking. 🎱

It's an oversized 8 ball with some of the following answers:

Yes - definitely.
It is decidedly so.
Without a doubt.
Reply hazy, try again.
Ask again later.
Better not tell you now.
My sources say no.
Outlook not so good.
Very doubtful.
Create a magic8.py program that can respond to any Yes or No questions with a different answer each time it executes.

The output should have the following format:

Question:      [Question]
Magic 8 Ball:  [Answer]

For example:

Question:      Is Codédex better than Udemy yet?
Magic 8 Ball:  Better not tell you now.
"""

# Write code below 💖
import random

question = input("Question: ")

ball_8 = random.randint(1, 9)
ball_answer = ""

if ball_8 == 1:
  ball_answer = "Yes - definitely."
elif ball_8 == 2:
  ball_answer = "It is decidedly so."
elif ball_8 == 3:
  ball_answer = "Without a doubt."
elif ball_8 == 4:
  ball_answer = "Reply hazy, try again."
elif ball_8 == 5:
  ball_answer = "Ask again later."
elif ball_8 == 6:
  ball_answer = "Better not tell you now."
elif ball_8 == 7:
  ball_answer = "My sources say no."
elif ball_8 == 8:
  ball_answer = "Outlook not so good."
else:
  ball_answer = "Very doubtful."

print("Magic 8 Ball:" + " " + ball_answer)