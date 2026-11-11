""""99 Bottles of Beer" is an old song that annoying kids, oops I mean everyone, sang on road trips to pass the time.

Create a 99_bottles.py program and use a for loop and a range() function to print out all the verses of "99 Bottles of Beer."

99 bottles of beer on the wall

99 bottles of beer

Take one down, pass it around

98 bottles of beer on the wall

And don't forget to use string interpolation!"""

# Write code below 💖

for bottles in range(99, 0, -1):
  print(f"{bottles} bottles of beer on the wall")
  print(f"{bottles} bottles of beer")
  print("Take one down, pass it around")
  print(f"{bottles-1} bottles of beer on the wall")