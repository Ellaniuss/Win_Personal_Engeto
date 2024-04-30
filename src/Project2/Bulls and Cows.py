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

game_num = random_generator()

spacer = ("-" * 40)

print(
    "Greetings fellow gamer! \n" +
    spacer + "\n" +
    "I have generated a random 4-digit number for you. \n" +
    "Let's play a game of Bulls and Cows. \n" +
    "Can you guess generated number ?" +
    "\n" + spacer
    )
