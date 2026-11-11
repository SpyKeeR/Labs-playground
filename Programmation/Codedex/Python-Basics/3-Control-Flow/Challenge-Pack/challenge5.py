"""Instructions
The year is 2199... Humanity is now an interplanetary species, freely traveling across the solar system! 🚀

Create a weight conversion program that:

Asks the user for their Earth weight (as a float).
Asks the user for a planet number (as an int).
Then, use an if/elif/else statement to calculate the user's weight on the destination planet.

To calculate the user's weight:

destination weight=Earth weight × relative gravity
Number	Planet	Relative Gravity
1	Mercury	0.38
2	Venus	0.91
3	Mars	0.38
4	Jupiter	2.53
5	Saturn	1.07
6	Uranus	0.89
7	Neptune	1.14
If the user enters a planet number outside of 1 - 7, print a message that says 'Invalid number'."""

# Write code below 💖

earth_weight = float(input("What is you Earth weight ? "))
print("""
1	- Mercury
2	- Venus
3	- Mars
4	- Jupiter
5	- Saturn
6	- Uranus
7	- Neptune
""")
planet_nb = int(input("What is your planet number ? "))

if planet_nb == 1:
  dest_weight = earth_weight * 0.38
  print("Your Mercury Weight is " + str(dest_weight) + "kg.")
elif planet_nb == 2:
  dest_weight = earth_weight * 0.91
  print("Your Venus Weight is " + str(dest_weight) + "kg.")
elif planet_nb == 3:
  dest_weight = earth_weight * 0.38
  print("Your Mars Weight is " + str(dest_weight) + "kg.")
elif planet_nb == 4:
  dest_weight = earth_weight * 2.53
  print("Your Jupiter Weight is " + str(dest_weight) + "kg.")
elif planet_nb == 5:
  dest_weight = earth_weight * 1.07
  print("Your Saturn Weight is " + str(dest_weight) + "kg.")
elif planet_nb == 6:
  dest_weight = earth_weight * 0.89
  print("Your Uranus Weight is " + str(dest_weight) + "kg.")
elif planet_nb == 7:
  dest_weight = earth_weight * 1.14
  print("Your Neptune Weight is " + str(dest_weight) + "kg.")
else:
  print("Invalid number")