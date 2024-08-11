from flask import Blueprint, request, redirect, url_for, jsonify
import random
import os
from shared_data import deck, hand, discard, ink, board

deck_bp = Blueprint('deck', __name__)

TXT_FILES_DIR = 'decklists'
log_file_path = 'click_log.txt'
lore = 0

#clear log on app start
def clear_log_file():
    with open(log_file_path, 'w') as log_file:
        log_file.write('App started. Paste your deck into the box above or select a deck from the dropdown.\n')
clear_log_file()

@deck_bp.route('/add_to_deck', methods=['POST'])
def add_to_deck():
    global deck
    user_input = request.form.get('user_input')
    deck_visible = request.form.get('deck_visible') == 'true'
    hand_visible = request.form.get('hand_visible') == 'true'
    board_visible = request.form.get('board_visible') == 'true'
    discard_visible = request.form.get('discard_visible') == 'true'
    ink_visible = request.form.get('ink_visible') == 'true'
    # Clear the existing deck
    deck.clear()
    # Split the input by new lines
    lines = user_input.splitlines()
    total_items = sum(int(line[0]) if line and line[0].isdigit() else 1 for line in lines)
    unique_numbers = random.sample(range(total_items), total_items)
    for line in lines:
        # Check if the first character is a digit
        if line and line[0].isdigit():
            count = int(line[0])
            item = line[1:].strip()
            formatted_item = item.replace('-', '').replace('  ', ' ').replace(" ", "-").lower() + ".webp"
            for _ in range(count):
                deck.append((item, unique_numbers.pop(), formatted_item))
        else:
            item = line.strip()
            formatted_item = item.replace('-', '').replace('  ', ' ').replace(" ", "-").lower() + ".webp"
            deck.append((item, unique_numbers.pop(), formatted_item))
    deck.sort(key=lambda x: x[1])
    log_text = "Deck loaded. Click Load Assets to download card pictures and draw your hand."
    log_click(log_text)
    return redirect(url_for('main.home', board_visible=board_visible, deck_visible=deck_visible, hand_visible=hand_visible, discard_visible=discard_visible, ink_visible=ink_visible))

@deck_bp.route('/reset', methods=['POST'])
def reset():
    global deck, hand, discard, ink, board, lore
    deck_visible = request.form.get('deck_visible') == 'false'
    hand_visible = request.form.get('hand_visible') == 'true'
    board_visible = request.form.get('board_visible') == 'true'
    discard_visible = request.form.get('discard_visible') == 'false'
    ink_visible = request.form.get('ink_visible') == 'false'
    # Clear all lists
    deck.clear()
    hand.clear()
    discard.clear()
    ink.clear()
    board.clear()
    lore = 0
    return redirect(url_for('main.home', board_visible=board_visible, deck_visible=deck_visible, hand_visible=hand_visible, discard_visible=discard_visible, ink_visible=ink_visible))

@deck_bp.route('/reset_deck', methods=['POST'])
def reset_deck():
    global deck, hand, discard, ink, board, lore
    deck_visible = request.form.get('deck_visible') == 'false'
    hand_visible = request.form.get('hand_visible') == 'true'
    board_visible = request.form.get('board_visible') == 'true'
    discard_visible = request.form.get('discard_visible') == 'false'
    ink_visible = request.form.get('ink_visible') == 'false'

    # Move items to deck
    deck.extend(hand)
    deck.extend(board)
    deck.extend(discard)
    deck.extend(ink)

    # Clear lists
    hand.clear()
    board.clear()
    discard.clear()
    ink.clear()

    # Shuffle the deck
    random.shuffle(deck)

    # Reset lore
    lore = 0
    log_text = "All cards returned to deck and Lore set to 0"
    log_click(log_text)
    return redirect(url_for('main.home', board_visible=board_visible, deck_visible=deck_visible, hand_visible=hand_visible, discard_visible=discard_visible, ink_visible=ink_visible))

@deck_bp.route('/draw_card', methods=['POST'])
def draw_card():
    global deck, hand
    deck_visible = request.form.get('deck_visible') == 'false'
    hand_visible = request.form.get('hand_visible') == 'true'
    board_visible = request.form.get('board_visible') == 'true'
    discard_visible = request.form.get('discard_visible') == 'false'
    ink_visible = request.form.get('ink_visible') == 'false'
    if deck:
        smallest_card = min(deck, key=lambda x: x[1])
        deck.remove(smallest_card)
        hand.append((smallest_card[0], 0, smallest_card[2]))
        log_text = f"{smallest_card[0]} drawn from deck"
        log_click(log_text)
    return redirect(url_for('main.home'))

@deck_bp.route('/draw_seven_cards', methods=['POST'])
def draw_seven_cards():
    global deck, hand
    deck_visible = request.form.get('deck_visible') == 'false'
    hand_visible = request.form.get('hand_visible', 'true') == 'true'
    board_visible = request.form.get('board_visible', 'true') == 'true'
    discard_visible = request.form.get('discard_visible') == 'false'
    ink_visible = request.form.get('ink_visible') == 'false'
    for _ in range(7):
        if deck:
            smallest_card = min(deck, key=lambda x: x[1])
            deck.remove(smallest_card)
            hand.append((smallest_card[0], 0, smallest_card[2]))
            log_text = f"{smallest_card[0]} drawn from deck"
            log_click(log_text)
    return redirect(url_for('main.home'))

@deck_bp.route('/move_item/<from_list>/<to_list>/<int:index>')
def move_item(from_list, to_list, index):
    global deck, hand, discard, ink, board
    lists = {
        'deck': deck,
        'hand': hand,
        'discard': discard,
        'ink': ink,
        'board': board
    }

    # Extract the item from the source list
    item = lists[from_list].pop(index)
    
    # Handle moving to the deck with an assignment number
    if to_list == 'deck':
        add_to_top = request.args.get('add_to_top', default=False, type=bool)
        add_to_bottom = request.args.get('add_to_bottom', default=False, type=bool)
        if add_to_top:
            # Assign a number that is smaller than any current number in the deck (add to top)
            log_text = f"{item[0]} moved from {from_list} to top of deck"
            new_assignment_number = min(deck, key=lambda x: x[1])[1] - 1 if deck else 0
        elif add_to_bottom:
            # Assign a number that is larger than any current number in the deck (add to bottom)
            log_text = f"{item[0]} moved from {from_list} to bottom of deck"
            new_assignment_number = max(deck, key=lambda x: x[1])[1] + 1 if deck else 0
        else:
            # Default behavior, just append with a new number (usually for other cases)
            log_text = f"{item[0]} moved from {from_list} to {to_list}"
            new_assignment_number = max(deck, key=lambda x: x[1])[1] + 1 if deck else 0
        # Append to the deck with the new assignment number
        lists[to_list].append((item[0], new_assignment_number, item[2]))
    else:
        # For all other moves, just append to the destination list
        log_text = f"{item[0]} moved from {from_list} to {to_list}"
        lists[to_list].append((item[0], 0, item[2]))  # You might want to adjust this as per your use case

    log_click(log_text)

    return redirect(url_for('main.home'))

@deck_bp.route('/shuffle_deck', methods=['POST'])
def shuffle_deck():
    global deck

    # Get the total number of items in the deck
    total_items = len(deck)

    # Generate a list of unique numbers between 0 and the total number of items
    unique_numbers = random.sample(range(total_items), total_items)

    # Reassign new unique assignment numbers to each card in the deck
    for i in range(total_items):
        deck[i] = (deck[i][0], unique_numbers[i], deck[i][2])

    # Sort the deck based on the new assignment numbers
    deck.sort(key=lambda x: x[1])

    log_text = "Deck shuffled"
    log_click(log_text)

    return redirect(url_for('main.home', deck_visible=True, hand_visible=True, discard_visible=True, ink_visible=True, board_visible=True))

@deck_bp.route('/list_files', methods=['GET'])
def list_files():
    # List all .txt files in the directory
    files = [f for f in os.listdir(TXT_FILES_DIR) if f.endswith('.txt')]
    return jsonify(files)

@deck_bp.route('/get_file_content', methods=['GET'])
def get_file_content():
    file_name = request.args.get('file')
    if file_name:
        file_path = os.path.join(TXT_FILES_DIR, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
            return content
    return '', 404

@deck_bp.route('/get_lore', methods=['GET'])
def get_lore():
    global lore
    return jsonify(lore=lore)

@deck_bp.route('/increment_lore', methods=['POST'])
def increment_lore():
    global lore
    lore += 1
    log_text = f"Lore incremented by 1, new total: {lore}"
    log_click(log_text)
    return jsonify(lore=lore)

@deck_bp.route('/decrement_lore', methods=['POST'])
def decrement_lore():
    global lore
    lore -= 1
    log_text = f"Lore decreased by 1, new total: {lore}"
    log_click(log_text)
    return jsonify(lore=lore)

@deck_bp.route('/log_click', methods=['POST'])
def log_click(log_entry):
    #log_text = request.json.get('log_text')
    with open(log_file_path, 'a') as log_file:
        log_file.write(f'{log_entry}\n')
    return jsonify(status="success")

@deck_bp.route('/get_log', methods=['GET'])
def get_log():
    with open(log_file_path, 'r') as log_file:
        log_contents = log_file.read()
    return jsonify(log=log_contents)