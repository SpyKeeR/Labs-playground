"""Instructions
Snapple is a famous tea brand born in Brooklyn, NY. Every bottle cap hides a quirky, fun fact. 🍑

Use the random module to generate a number between 1 and 6.

Then, use an if/elif/else statement to print out one of these Snapple facts:

'Flamingos turn pink by eating shrimp.'
'Honey never goes bad.'
'Shrimp can only swim backwards.'
'A taste bud\'s life is about 10 days.'
'You can\'t sneeze while sleeping.'
'Tiny pocket in jeans was for watches.'"""

# Write code below 💖

import random

snapple = random.randint(1, 6)

if snapple == 1:
  print("Flamingos turn pink by eating shrimp.")
elif snapple == 2:
  print("Honey never goes bad.")
elif snapple == 3:
  print("Shrimp can only swim backwards.")
elif snapple == 4:
  print("A taste bud's life is about 10 days.")
elif snapple == 5:
  print("You can't sneeze while sleeping.")
elif snapple == 6:
  print("Tiny pocket in jeans was for watches.")