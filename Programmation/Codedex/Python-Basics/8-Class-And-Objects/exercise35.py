"""In the last exercise, we created a Restaurant class.

In a new file called bobs_burgers.py, create an instance of the Restaurant class called bobs_burgers with the following attributes:

'Bob\'s Burgers'
'American Diner'
4.7
False
Once you do that, create two more instances of the Restaurant class with your favorite dinner spots nearby.

Then, use print(vars()) to output each of the three restaurants!"""

# Write code below 💖


class Restaurant:
  name = ''
  category = ''
  rating = 0.0
  delivery = False

bobs_burgers = Restaurant()

bobs_burgers.name = 'Bob\'s Burgers'
bobs_burgers.category = 'American Diner'
bobs_burgers.rating = 4.7
bobs_burgers.delivery = False

burger_king = Restaurant()

burger_king.name = 'Burger King'
burger_king.category = 'FastFood'
burger_king.rating = 3.9
burger_king.delivery = True

memphis_cafe = Restaurant()

memphis_cafe.name = 'Memphis Cafe'
memphis_cafe.category = 'American Diner'
memphis_cafe.rating = 4.6
memphis_cafe.delivery = False

print(vars(bobs_burgers))
print(vars(burger_king))
print(vars(memphis_cafe))

