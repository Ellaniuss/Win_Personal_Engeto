game_num = "4256"
game_in_progress = True

while game_in_progress:
    bulls = 0
    cows = 0
    guess = input("Enter guessed number: ")
    if guess == "exit":
        game_in_progress = False
        print("Exiting game.")
    else:
        for dig in range(len(game_num)):
            if guess[dig] in game_num:
                if guess[dig] == game_num[dig]:
                    bulls += 1
                else:
                    cows += 1
        print(f"Game satus is: \n Bulls: {bulls}, Cows: {cows}")
               
           
