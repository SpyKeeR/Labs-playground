"""Instructions
Each year at the Oscars, the Academy Award for Best Picture goes to a single film. Usually the final award presented, it’s widely considered the most prestigious.

Let’s use a list to record the recent winners! 🍿

Start with the following list:

best_pictures = [
  '2020 - Nomadland',
  '2019 - Parasite',
  '2018 - Green Book',
  '2017 - The Shape of Water',
  '2016 - Moonlight',
]

Google the Best Picture winners from 2021-2025. And add them to the front of the best_pictures list.

Lastly, print the best_pictures list.

Note: Match the format of the list. And remember, it's the year of the movie, not the year of the ceremony."""

# Write code below 💖

best_pictures = [
  '2020 - Nomadland',
  '2019 - Parasite',
  '2018 - Green Book',
  '2017 - The Shape of Water',
  '2016 - Moonlight',
]

best_pictures.insert(0, "2021 - CODA")
best_pictures.insert(0, "2022 - Everything Everywhere All at Once")
best_pictures.insert(0, "2023 - Oppenheimer")
best_pictures.insert(0, "2024 - Anora")
best_pictures.insert(0, "2025 - One Battle After Another")


print(best_pictures)