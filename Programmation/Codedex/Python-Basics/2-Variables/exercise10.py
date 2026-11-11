"""
We just got home from a fun trip to South America, specifically Colombia, Peru, and Brazil. There's some leftover cash in:

🇨🇴 Colombian pesos
🇵🇪 Peruvian soles
🇧🇷 Brazilian reais
Create a currency.py program that asks the user for the amount they have in pesos, soles, and reais and calculates the total in USD.

Make sure to Google the current exchange rates for pesos, soles, and reais!



The output should look something like this, but with different results:

What do you have left in pesos? 5600
What do you have left in soles? 105
What do you have left in reais? 280
413.0

The sequence should be:

Currency code example

Cha-ching! Now you have the total in USD. 💰
"""

# Write code below 💖

pesos = int(input("What do you have left in pesos ? "))
soles = int(input("What do you have left in soles ? "))
reais = int(input("What do you have left in reais ? "))
usd = (pesos * 0.00031) + (soles * 0.29) + (reais * 0.18)
print(usd)