"""Instructions
Suppose you and three friends go out for a meal. The bill comes, and you decide to split it evenly. 👯👯

Here are the prices of what was ordered:

bill = [13.99, 28.75, 9.99, 9.99, 6.95, 7.45, 16.45, 16.45]

Using this bill list, calculate the total amount and then divide it four ways.

Initialize the total with zero and loop through the bill list to add everything up.

With the total, store what each person has to pay in a my_share variable and then print the result."""

# Write code below 💖

bill = [13.99, 28.75, 9.99, 9.99, 6.95, 7.45, 16.45, 16.45]
total = 0
for item in bill:
  total += item
my_share = total / 4

print(my_share)