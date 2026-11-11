"""Instructions
A number is "squared" when it is either multiplied by itself or taken to the second power (e.g., 4² = 4 x 4 = 16).

First, ask the user for an integer with int(input()) and store it in a number variable. Then, define a total variable with an initial value of 0.

Note: You can pass a string prompt to int(input()).

Next, use a for loop and range() function to calculate the total of the squares of all integers from 1 to that number.

Last, print the output as an integer value."""

# Write code below 💖

number = int(input("Enter a number : "))
total = 0

for i in range(1, number+1):
  square = i ** 2
  total = total + square
print(total)