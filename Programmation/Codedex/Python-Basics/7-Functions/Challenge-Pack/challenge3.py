"""Instructions
In some online multiplayer games, there's a KDA ratio to evaluate a player's in-game performance:

KDA=(k+a)/d

k is how many players you took down.
d is how many times you died.
a is how many assists you had.
Write a kda() function that takes in parameters: k, d, a.

This function should calculate and return the KDA ratio that uses these paremeters."""

# Write code below 💖

def kda(k, d, a):
  return (k + a) / d

kda(10, 2, 3)