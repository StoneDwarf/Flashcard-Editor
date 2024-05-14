import json
import io

log_buffer = io.StringIO()


def log_input():
    user_input = input()
    log_buffer.write(user_input + '\n')
    return user_input

def log_print(message):
    print(message)
    log_buffer.write(message + '\n')
    

def term_error(database):
    term = log_input()
    while True:
        if term in database.keys():
            log_print(f'The term "{term}" already exists. Try again:')
            term = log_input()
        else:
            return term


def definition_error(database):
    definition = log_input()
    while True:
        if definition in database.values():
            log_print(f'The definition "{definition}" already exists. Try again:')
            definition = log_input()
        else:
            return definition


def answer_error(database, answer, test_reply):
    if test_reply in database.values():
        for wrong_question, wrong_answer in database.items():
            if test_reply == wrong_answer:
                log_print(f'Wrong. The right answer is "{answer}", but your definition is correct for "{wrong_question}".')
    else:
        log_print(f'Wrong. The right answer is "{answer}".')


def add_cart(database):
    log_print('The term for card:')
    term = term_error(database)
    log_print('The definition for card ')
    definition = definition_error(database)
    database[term] = definition
    log_print(f'The pair ("{term}":"{definition}") has been added')


def remove_cart(database):
    log_print('Which card?')
    card = log_input()
    try:
        del database[card]
        log_print('The card card has been removed')
    except KeyError:
        log_print(f'Can\'t remove "{card}": there is no such card.')


def import_database(database):
    log_print('File name:')
    filename = log_input()
    merged_dict = {}
    try:
        with open(filename, 'r') as new_data:
            downloaded_dict = json.load(new_data)
            merged_dict.update(downloaded_dict.get('database', {}))
            cards_number = len(merged_dict)
            merged_dict.update(database)
            database = merged_dict
            error_database.update(downloaded_dict.get('error_database', {}))
            log_print(f'{cards_number} cards have been loaded')
            return database
    except FileNotFoundError:
        print('File not found')


def write_file(database):
    log_print('File name:')
    filename = log_input()
    combined_data = {"database": database, "error_database": error_database}
    with open(filename, 'w') as new_data:
        json.dump(combined_data, new_data)
        log_print(f'{len(database)} cards have been saved')


def ask_question(database, error_database):
    log_print('How many times to ask?')
    cards_nbr = log_input()
    for _ in range(int(cards_nbr)):
        for question, answer in database.items():
            if int(cards_nbr) > 0:
                log_print(f'Print the definition of "{question}":')
                test_reply = log_input()
                if test_reply == answer:
                    log_print("Correct!")
                else:
                    error_track(error_database, question)
                    answer_error(database, answer, test_reply)
                cards_nbr -= 1


def error_track(error_database, wrong_question):
    if wrong_question in error_database.keys():
        error_database[wrong_question] += 1
    else:
        error_database[wrong_question] = 1


def hardest_card(error_database):
    if len(error_database) == 0:
        log_print('There are no cards with errors.')
        return
    else:
        max_errors = max(error_database.values())
        hardest_cards = [term for term, errors in error_database.items() if errors == max_errors]
        if len(hardest_cards) == 1:
            log_print(f'The hardest card is "{hardest_cards[0]}". You have {max_errors} errors answering it.')
        else:
            hardest_cards_str = ', '.join([f'"{term}"' for term in hardest_cards])
            log_print(f'The hardest cards are {hardest_cards_str}. You have {max_errors} errors answering them.')


def make_log(log_data):
    log_print('File name:')
    filename = log_input()
    with open(filename, 'w') as log_file:
        log_file.write(log_data.getvalue())
    log_print('The log has been saved.')


database = {}
error_database = {}


while True:
    log_print('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):')
    action = log_input()
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
        make_log(log_buffer)
    elif action == 'hardest card':
        hardest_card(error_database)
    elif action == 'reset stats':
        error_database.clear()
        print('Card statistics have been reset')
