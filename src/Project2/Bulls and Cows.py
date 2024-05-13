""""
Bulls and Cows.py: druhý projekt do Engeto Online Python Akademie
author: David Heczko
email: heczko.david@gmail.com
discord: ellaniuss
"""

# import modulu random pro dalsi praci s generovanim nahodnych cisel
import random

# prvni cast kodu definuje fci generator nahodneho cisla o 4 cislicich

def random_generator():
    gen_number = ""
    while len(gen_number) < 4:
        digit = str(random.randint(1, 9))
        if digit not in gen_number:
            gen_number += digit
    return gen_number

def input_check(guess):
  """
  Function check if the input is 4-digit number.

  Arguments:
    guess(str): The input string made by player that needs to be checked.

  Returns:
    bool: True if the input is 4-digit unique number, False if not.

  The function check whether there are other characters than digits, whether it contains exactly 4-digits, whether number doesn't beggin with 0 and whether there are no duplicated characters.
  If any of these conditions are not met, errors are appended to the list of errors.
  If errors occurs, they are specifically printed and function retunrs False. Otherwise it returns True.

  """

  errors = []

  error_types = [
      (not guess.isdigit(), "Not a number."),
      (len(guess) != 4, "More or less than 4 characters."),
      (guess[0] == '0', "Beggins with 0."),
      (len(guess) != len(set(guess)), "Duplicate characters.")
    ]

  for error, message in error_types:
    if error:
      errors.append(message)

  if errors:
    print(f"An error or errors occured while entering number. Please see below list with details:")
    print("\n".join(errors))
    return False
  else:
    return True


def guess_evaluation(game_num, guess):
  """
  Function evalueates player's guess with generated random number.

  Arguments:
    game_num (str): Randomly generated number by the game.
    guess(str): The number guessed by the player

  Returns:
    tuple: Tuple containing the count of bulls and cows.

  This function evaluates number added by player agains generated number by the game.
  It returns number of bulls for all digits that are correct and on same possition, and cows for all digits that are correct but on different possition.
  """

  bulls = 0
  cows = 0

  for dig in range(len(game_num)):
    if guess[dig] in game_num:
      if guess[dig] == game_num[dig]:
        bulls += 1
      else:
        cows += 1
  return bulls, cows

def tries_counter(tries):
  """
  Function created to count players tries needed to guess generated number by the game.

  Arguments:
    tries(int): Current number of tries.

  Retunrs:
    int: Updated count of tries by 1.
  """
  tries += 1
  return tries


def end_game(bulls):
  """
  Function evaluates when game ends.

  Arguments:
    bulls(int): Number of bulls achieved in the game.

  Returns:
    bool: True if the count of bulls is 4, False if not.
  """
  if bulls == 4:
    return True
  else:
    return False

def main():
  """
  Executes the Bulls and Cows game.

  This is the main function of the program that serves as entry point for the game.
  It generates random 4-digit number using random_generator function
  and prompts user to input guesses until the correct number is wholy guessed,
  or the player decides to end the game.
  For each guess, it check validity of input using the input_check function.
  If the input is correct, it evaluates entered number using guess_evaluation function and returns and determine number of bulls and cows.
  """
  game_num = random_generator()
  spacer = ("-" * 40)

  print(
    "Greetings fellow gamer! \n" +
    spacer + "\n" +
    "I have generated a random 4-digit number for you. \n" +
    "Let's play a game of Bulls and Cows. \n" +
    "Entered number cannot contain duplicate values and needs to be 4 digits long. \n" +
    "In case you would like to finish the game please enter 'end' \n" +
    "\n" + "Can you guess generated number ? \n" + spacer
    )
  
  tries = 0

  while True:
    guess = input("Enter number: ")
    if not guess == "end":
      if input_check(guess):
        tries = tries_counter(tries)
        bulls, cows = guess_evaluation(game_num, guess)
        if not end_game(bulls):
          print(f"Bull: {bulls}" if bulls <= 1 else f"Bulls: {bulls}", f"Cow: {cows}" if cows <= 1 else f"Cows: {cows}")
        else:
          print(f"You have guessed it right! It took you {tries} tries.")
          break
    else:
      print("You have ended the game!")
      break

if __name__ == __main__:
    main()
