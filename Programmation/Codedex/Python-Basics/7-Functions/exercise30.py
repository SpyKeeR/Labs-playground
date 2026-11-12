"""In September 1999, after ten months of travel to Mars, the Mars Climate Orbiter suddenly burned to pieces because it had entered the atmosphere too fast.

Oh no! The NASA engineers forgot to convert imperial data to metric data in one of the functions! This noob mistake cost American taxpayers $125 million total.

Suppose you're a NASA intern, and your team is calculating the distance a rocket needs to travel. The value calculated is in kilometers, while the next step requires miles. Your manager quickly writes this on the board:


miles= kilometers / 1.609
 

Create a new file called rocket.py.

Define a function named distance_to_miles() that converts a distance from kilometers to miles. It should:

Take in one parameter named distance (the distance in kilometers).
Print the distance in miles.
After, call the function and use 10000 as the argument."""

# Write code below 💖

def distance_to_miles(distance):
  print(distance / 1.609)
distance_to_miles(10000)