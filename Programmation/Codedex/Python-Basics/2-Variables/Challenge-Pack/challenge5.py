"""Instructions
Ever wondered how old your furry friend is in human years? Let's build a Pet Age Converter! 🐶🐱

First things first, pick a lane: dog or cat.

Then ask the user how old their dog/cat is and store it in an age variable. The user should see:

Enter your dog's age:

Calculate their age in human years and store it in human_age:

1 dog year ≈ 7 human years
1 cat year ≈ 6 human years
Print out human_age."""

# Write code below 💖

age = int(input("Enter your dog\'s age:"))

human_age = age * 7

print(human_age)