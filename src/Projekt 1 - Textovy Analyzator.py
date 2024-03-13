texts = ['''
Situated about 10 miles west of Kemmerer,
Fossil Butte is a ruggedly impressive
topographic feature that rises sharply
some 1000 feet above Twin Creek Valley
to an elevation of more than 7500 feet
above sea level. The butte is located just
north of US 30N and the Union Pacific Railroad,
which traverse the valley.''',
'''At the base of Fossil Butte are the bright
red, purple, yellow and gray beds of the Wasatch
Formation. Eroded portions of these horizontal
beds slope gradually upward from the valley floor
and steepen abruptly. Overlying them and extending
to the top of the butte are the much steeper
buff-to-white beds of the Green River Formation,
which are about 300 feet thick.''',
'''The monument contains 8198 acres and protects
a portion of the largest deposit of freshwater fish
fossils in the world. The richest fossil fish deposits
are found in multiple limestone layers, which lie some
100 feet below the top of the butte. The fossils
represent several varieties of perch, as well as
other freshwater genera and herring similar to those
in modern oceans. Other fish such as paddlefish,
garpike and stingray are also present.
''']

"""
Projekt 1 - Textový analyzátor.py

author: David Heczko
email: heczko.david@gmail.com
discord: ellaniuss

"""
# Creation of spacer for visual separation of code pieces of final print
spacer = ('-' * 42)
# Created directory with usernames and passwored that are allowed. Added input commands for username and password
registered_users = {'bob': '123', 'ann': 'pass123', 'mike': 'password123', 'liz': 'pass123'}
username = str(input("Username: "))
password = str(input("Password: "))

print(spacer)
'#Created check of username and password validity'
logged_in = False
if username in registered_users:
    if registered_users.get(username) == password:
        print(f'Hello to the app, {username}!')
        logged_in = True
else:
    print(f'Username or Password is incorrect. Program will be terminated.')
    logged_in = False
    exit()
print(spacer)
# created empty variables for text analysis
word_count = 0
word_istitle = 0
word_isupper = 0
word_islower = 0
number_count = 0
total_sum = 0
# created input request to chose text and validity check of value inputed. Only possible values are numbers 1,2,3
text_select = input('Please choose text for analysis (1 - 3): ')
print(spacer)
if not text_select.isdigit():
    print('Selection needs to be number between 1 and 3. Program will be terminated.')
    exit()

elif text_select.isdigit():
    text_select = int(text_select)
    if text_select not in range(1, 4):
        print('Selected text does not exist. Program will be terminated.')
        exit()
else:
    text_select = int(text_select)

print(spacer)

choice = texts[(text_select - 1)]  # created variable "choice" to convert input number to index
sentence = choice.split()  # created list of each word in text on index selected by input through "choice" variable

for word in sentence:  # created loops to check number of words in chosen text
    word_count = word_count + 1
for word in sentence:  # created loop to analyse text
    if word.istitle():
        word_istitle = word_istitle + 1
    elif word.isupper():
        word_isupper = word_isupper + 1
    elif word.islower():
        word_islower = word_islower + 1
    elif word.isdigit():
        number_count = number_count + 1
        total_sum = total_sum + int(word)



print(
    f'There are {word_count} words in the selected text.\n'
    f'There are {word_istitle} titlecase words. \n'
    f'There are {word_isupper} uppercase words. \n'
    f'There are {word_islower} lowercase words. \n'
    f'There are {number_count} numeric strigns. \n'
    f'The sum of all the numbers is {total_sum}'
    )
print(spacer)
# created dictionary for lenghts of words
len_count = dict()
# created for loop to save lenghts to the created dictionary
for word in sentence:
    word_len = len(word)
    if word_len not in len_count:
        len_count[word_len] = 1
    else:
        len_count[word_len] += 1
# print of simple graph header
print(
    f'{"LEN":<3}| {"OCCURENCES":<20}| {"Nr.":<5}'
    f'\n'
    f'{spacer:}'
    )
# loop for print of simple graph using found data
for ln, occur in len_count.items():
    print(f'{ln:<3}| {"*" * occur:<20}| {occur:<5}')
