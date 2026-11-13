"""Since 1996, the Pokémon video game franchise has delighted players around the world with collectible pocket monsters. A Pokédex is a device that tracks the information for Pokémon that are seen or caught.

Create a new file called pokedex.py.

Next, let's define a Pokemon class with the following attributes:

entry (integer)
name (string)
types (list of strings)
description (string)
is_caught (boolean)
Note: Make sure to use the __init__() method.

Next, create an instance method called .speak() that prints a string of the sound a Pokémon makes. A Pokémon usually just says their name, so make the .speak() simply print out their name twice!

Then, create another instance method called .display_details() that prints the attributes of a Pokemon object like the following:

Entry Number: 25
Name: Pikachu
Type: Electric
Description: It has small electric sacs on both its cheeks. If threatened, it looses electric charges from the sacs.
Pikachu has already been caught!

Lastly, create three Pokemon class objects and use the .speak() or .display_details() instance methods for each one."""

# Write code below 💖

class Pokemon:
  def __init__(self, entry, name, types, description, is_caught):
    self.entry = entry
    self.name = name
    self.types = types
    self.description = description
    self.is_caught = is_caught
  def speak(self):
    print((self.name + ' ') * 2)
  def display_details(self):
    print(f"""
Entry number: {self.entry}
Name: {self.name}""")
    print('Type: ',end ='')
    print(*self.types, sep= ', ')
    print(f'Description: {self.description}')
    if self.is_caught == True:
      print(self.name + ' has already been caught!')
    else:
      print(self.name + ' has not been caught.')


ronflex = Pokemon(143, 'Ronflex', ['Normal'], 'Quand il ne dort pas, ce glouton passe son temps à manger. Il peut ingurgiter jusqu’à 400 kg de nourriture en une seule journée.', True)
sulfura = Pokemon(146, 'Sulfura', ['Feu', 'Vol'], 'Un des Pokémon oiseaux légendaires. On dit que sa venue annonce l’arrivée du printemps.', False)
mewtwo = Pokemon(150, 'Mewtwo', ['Psy'], 'Son ADN est presque le même que celui de Mew, mais sa taille et son caractère sont très différents.', True)

ronflex.speak()
sulfura.display_details()
mewtwo.display_details()