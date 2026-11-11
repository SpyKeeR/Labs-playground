"""Instructions
A DNA sequence, such as 'ACG', TCA','CGT', is a three-letter combination of these pieces:

Adenine (A)
Cytosine (C)
Guanine (G)
Thymine (T)
Let's use a Python list to find a specific three-letter combination, starting with the following:

dna_sequence = ['GCT', 'AGC', 'AGG', 'TAA', 'ACT', 'CAT', 'TAT', 'CCC', 'ACG', 'GAA', 'ACC', 'GGA']

Next, define two variables:

item_to_find string with a three-letter combination of your choice (e.g. 'TGA').
item_found boolean, initialized to False.
Loop through each item in the dna_sequence list. Inside, use an if statement to see if an item is equal to item_to_find. If so, set item_found to True.

Outside the loop, use an if/else statement to check if item_found is True:

If so, print something like "Item Found!"
Else, print something like "Item not found."""

# Write code below 💖

dna_sequence = ['GCT', 'AGC', 'AGG', 'TAA', 'ACT', 'CAT', 'TAT', 'CCC', 'ACG', 'GAA', 'ACC', 'GGA']

item_to_find = "TCG"
item_found = False

for item in dna_sequence:
  if item == item_to_find:
    item_found = True

if item_found == True:
  print("Item Found!")
else:
  print("Item not found.")