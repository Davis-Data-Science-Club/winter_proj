# Nutrition Calculator
from matplotlib.pyplot import waitforbuttonpress
import pandas as pd


def wait_for_valid_input(prompt, valid_inputs):
  """
  Continually prompts the user for input until they enter a valid input.
  """
  user_input = input(prompt)

  while user_input.lower().strip() not in valid_inputs:
    print("Input not recognized. Please try an input from the list:")
    print(valid_inputs)
    user_input = input(prompt)

  return user_input.lower().strip()


if __name__ == '__main__':
  print("Welcome to DDSC's Nutrition Calculator!")

  # Get user input
  dc = wait_for_valid_input(
    "What dinning commons did you go to? ",
    ['cuarto', 'tercero', 'segundo']
  )

  day = wait_for_valid_input(
    "What day did you go to the dinning commons? ",
    ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
  )

  meal_time = wait_for_valid_input(
    "What meal time did you go (Breakfast, Lunch, Dinner)? ",
    ['breakfast', 'lunch', 'dinner']
  )

  meal_items = input("What items did you consume (separated by commas)? ")


  # TODO: Filter data
  df = pd.read_csv(f'./data/{dc}-menu.csv')
  # df = df.loc[
  #   df['Date'].str.contains(day)
  # ]
  # df = df.loc[
  #   df['Mealtime'].str.contains(meal_time)
  # ]


  # TODO: Output results
  print(f"{df.shape[0]} items found for {day} {meal_time}.")
