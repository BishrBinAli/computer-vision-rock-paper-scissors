import random

def get_computer_choice():
    options = ["Rock", "Paper", "Scissors"]
    choice = random.choice(options)
    return choice

def get_user_choice():
    user_choice = input("Enter your choice(Rock, Paper, or Scissors):")
    return user_choice

print(get_computer_choice())
print(get_user_choice())