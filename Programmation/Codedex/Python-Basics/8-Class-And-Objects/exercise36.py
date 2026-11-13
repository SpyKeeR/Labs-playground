"""Ever wonder how many people live in New York City? What about London?

Create a favorite_cities.py program.

Let's make a City class that uses the __init__() method to define the following attributes:

name (string)
country (string)
population (integer rounded to the nearest thousand people)
landmarks (list of strings)
Next, create an object for your hometown and assign the attributes above.

Lastly, create another object for the city that you've always wanted to visit!

Bonus: Add 2-3 more attributes, like nickname, founding year, mayor, etc."""

# Write code below 💖

class City:
  def __init__(self, name, country, population, landmarks):
    self.name = name
    self.country = country
    self.population = population
    self.landmarks = landmarks

hometown = City('Limoges', 'France', 30000, ['Fnac', 'Beaupeyrat', 'Patinoire'])
dreamtown = City('Eindhoven', 'Pays-Bas', 90000, ['PSV Stadium','Klokgebouw','Winkels'])