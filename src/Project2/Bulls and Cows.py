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
bulls = 0
cows = 0
# Uvodni text
print(
    "Greetings fellow gamer! \n" +
    spacer + "\n" +
    "I have generated a random 4-digit number for you. \n" +
    "Let's play a game of Bulls and Cows. \n" +
    "Entered number cannot contain duplicate values and needs to be 4 digits long. \n" +
    "In case you would like to finish the game please enter 'end' \n" +
    "\n" + "Can you guess generated number ? \n" + spacer
    )

game_in_progress = True  # promenna pro urceni prubehu hry
tries = 0  # promenna pro urceni poctu pokusu

# Hlavni cast kodu pri keterem se vyhodnocuje podobnost zadaneho cisla s cislem generovanym
while game_in_progress:
    bulls = 0
    cows = 0

    guess = input("Enter guessed number or type 'end': ").lower()

    if bulls == 4:
        game_in_progress = False
        print("You have guessed correct number and won the game!")
    elif guess == "end":
        game_in_progress = False
        print("Exiting game.")
    elif not guess.isdigit():
        print("You have to enter number!")
        continue
    elif len(guess) != 4:
        print("Entered number has to have 4 digits!") 
        continue
    elif guess[0] == "0":
        print("Entered number cannot beggin with 0!")
        continue
    elif len(guess) != len(set(guess)):
        print("The input number contains duplicate values!")
        continue
    else:
        for dig in range(len(game_num)):  # for loop ktery overuje jednotlive znaky na indexech
            if guess[dig] in game_num:  # overeni zda-li je cislice ve vygenerovanem cisle
                if guess[dig] == game_num[dig]:  # overeni zda je cislice na stejnem indexu
                    bulls += 1
                else:
                    cows += 1
        # cast kodu ktery zajistuje mnozna a jednotna cisla
        if bulls <= 1 and cows <= 1:
            print(f"Bull: {bulls}, Cow: {cows} \n")
        else:    
            print(f"Bulls: {bulls}, Cows: {cows} \n")
        
        tries += 1
        if not bulls < 4:
            print(f"You have guessed the correct number in {tries} tries. You Win!")
            game_in_progress = False
            
            