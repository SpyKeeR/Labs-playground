"""
Instructions
Moore’s Law states that the number of transistors on a computer chip doubles around every 2 years.

That means growth isn’t linear – it’s exponential.

moore's law

Create two variables:

transistors for the number of transistors on your computer right now (e.g. 25000000000).
years for the time into the future (e.g. 10).
To calculate the future number of transistors:

transistors=transistors*(2**(years/2))
 
Print the new transistors.
"""
# Write code below 💖

transistors = 2500000000
years = 10
transistors = transistors * (2 ** (years / 2))
print (transistors)