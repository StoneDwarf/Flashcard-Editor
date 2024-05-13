import json


def term_error(dat):
    term = str(input())
    while True:
        if term in dat:
            print(f'The term "{term}" already exists. Try again:')
            term = input()
        else:
            return term


def definition_error(dat):
    definition = str(input())
    while True:
        if definition in dat.values():
            print(f'The definition "{definition}" already exists. Try again:')
            definition = input()
        else:
            return definition


def answer_error(dat, answer, test_reply):
    if test_reply in dat.values():
        for wrong_question, wrong_answer in dat.items():
            if test_reply == wrong_answer:
                print(f'Wrong. The right answer is "{answer}", but your definition is correct for "{wrong_question}".')
    else:
        print(f'Wrong. The right answer is "{answer}".')


def add_cart(dat):
    print('The term for card:')
    term = term_error(dat)
    print('The definition for card ')
    definition = definition_error(dat)
    dat[term] = definition
    print(f'The pair ("{term}":"{definition}") has been added')


def remove_cart(dat):
    print('Which card?')
    card = input()
    try:
        del dat[card]
        print('The card card has been removed')
    except KeyError:
        print(f'Can\'t remove "{card}": there is no such card.')


def import_database(dat):
    print('File name:')
    filename = input()
    merged_dict = {}
    try:
        with open(filename, 'r') as new_data:
            downloaded_dict = json.load(new_data)
            merged_dict.update(downloaded_dict.get('database', {}))
            cards_number = len(merged_dict)
            merged_dict.update(dat)
            dat = merged_dict
            error_database.update(downloaded_dict.get('error_database', {}))
            print(f'{cards_number} cards have been loaded')
            return dat
    except FileNotFoundError:
        print('File not found')


def write_file(dat):
    print('File name:')
    filename = input()
    combined_data = {"database": dat, "error_database": error_database}
    with open(filename, 'w') as new_data:
        json.dump(combined_data, new_data)
        print(f'{len(dat)} cards have been saved')


def ask_question(dat, error_dat):
    print('How many times to ask?')
    cards_nbr = int(input())
    for _ in range(cards_nbr):
        for question, answer in dat.items():
            if cards_nbr > 0:
                print(f'Print the definition of "{question}":')
                test_reply = str(input())
                if test_reply == answer:
                    print("Correct!")
                else:
                    error_track(error_dat, question)
                    answer_error(dat, answer, test_reply)
                cards_nbr -= 1


def error_track(error_dat, wrong_question):
    if wrong_question in error_dat.keys():
        error_dat[wrong_question] += 1
    else:
        error_dat[wrong_question] = 1


def hardest_card(error_dat):
    if len(error_dat) == 0:
        print('There are no cards with errors.')
        return
    else:
        max_errors = max(error_dat.values())
        hardest_cards = [term for term, errors in error_dat.items() if errors == max_errors]
        if len(hardest_cards) == 1:
            print(f'The hardest card is "{hardest_cards[0]}". You have {max_errors} errors answering it.')
        else:
            hardest_cards_str = ', '.join([f'"{term}"' for term in hardest_cards])
            print(f'The hardest cards are {hardest_cards_str}. You have {max_errors} errors answering them.')


def make_log(log_data):
    print('File name:')
    filename = input()
    with open(filename, 'w') as new_data:
        json.dump(log_data, new_data)
    print('The log has been saved.')


database = {}
error_database = {}

while True:
    print('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):')
    action = input()
    if action == 'add':
        add_cart(database)
    elif action == 'remove':
        remove_cart(database)
    elif action == 'import':
        import_database(database)
    elif action == 'export':
        write_file(database)
    elif action == 'ask':
        ask_question(database, error_database)
    elif action == 'exit':
        print('Bye bye!')
        break
    elif action == 'log':
        make_log(my_log)
    elif action == 'hardest card':
        hardest_card(error_database)
    elif action == 'reset stats':
        error_database.clear()
        print('Card statistics have been reset')
