"""Instructions
In a five-star restaurant review system (⭐️⭐️⭐️⭐️⭐️), the stars represent different levels of satisfaction. But what does each star rating actually mean?

Start by creating a rating variable and assign it a decimal number between 0 and 5.

Next, make a rating system with an if/elif/else:

rating greater than 4.5, print 'Perfection'
rating greater than 4, print 'Excellent'
rating greater than 3, print 'Good'
rating greater than 2, print 'Fair'
Otherwise, print 'Poor'"""

# Write code below 💖

rating = float(3)

if rating > 4.5:
  print("Perfection")
elif rating > 4:
  print("Excellent")
elif rating > 3:
  print("Good")
elif rating > 2:
  print("Fair")
else:
  print("Poor")