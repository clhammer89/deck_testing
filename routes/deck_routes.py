from flask import Blueprint, request, redirect, url_for
import random
from shared_data import deck, hand, discard, ink

deck_bp = Blueprint('deck', __name__)

@deck_bp.route('/add_to_deck', methods=['POST'])
def add_to_deck():
    global deck
    user_input = request.form.get('user_input')
    deck_visible = request.form.get('deck_visible') == 'true'
    hand_visible = request.form.get('hand_visible') == 'true'
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
    return redirect(url_for('main.home', deck_visible=deck_visible, hand_visible=hand_visible, discard_visible=discard_visible, ink_visible=ink_visible))

@deck_bp.route('/reset', methods=['POST'])
def reset():
    global deck, hand, discard, ink
    deck_visible = request.form.get('deck_visible') == 'false'
    hand_visible = request.form.get('hand_visible') == 'true'
    discard_visible = request.form.get('discard_visible') == 'false'
    ink_visible = request.form.get('ink_visible') == 'false'
    # Clear all lists
    deck.clear()
    hand.clear()
    discard.clear()
    ink.clear()
    return redirect(url_for('main.home', deck_visible=deck_visible, hand_visible=hand_visible, discard_visible=discard_visible, ink_visible=ink_visible))

@deck_bp.route('/draw_card', methods=['POST'])
def draw_card():
    global deck, hand
    deck_visible = request.form.get('deck_visible') == 'false'
    hand_visible = request.form.get('hand_visible') == 'true'
    discard_visible = request.form.get('discard_visible') == 'false'
    ink_visible = request.form.get('ink_visible') == 'false'
    if deck:
        smallest_card = min(deck, key=lambda x: x[1])
        deck.remove(smallest_card)
        hand.append((smallest_card[0], 0, smallest_card[2]))
    return redirect(url_for('main.home', deck_visible=deck_visible, hand_visible=hand_visible, discard_visible=discard_visible, ink_visible=ink_visible))

@deck_bp.route('/draw_seven_cards', methods=['POST'])
def draw_seven_cards():
    global deck, hand
    deck_visible = request.form.get('deck_visible') == 'false'
    hand_visible = request.form.get('hand_visible', 'true') == 'true'
    discard_visible = request.form.get('discard_visible') == 'false'
    ink_visible = request.form.get('ink_visible') == 'false'
    for _ in range(7):
        if deck:
            smallest_card = min(deck, key=lambda x: x[1])
            deck.remove(smallest_card)
            hand.append((smallest_card[0], 0, smallest_card[2]))
    return redirect(url_for('main.home', deck_visible=deck_visible, hand_visible=hand_visible, discard_visible=discard_visible, ink_visible=ink_visible))

@deck_bp.route('/move_item/<from_list>/<to_list>/<int:index>')
def move_item(from_list, to_list, index):
    global deck, hand, discard, ink
    deck_visible = request.args.get('deck_visible', 'false') == 'true'
    hand_visible = request.args.get('hand_visible', 'true') == 'true'
    discard_visible = request.args.get('discard_visible', 'false') == 'true'
    ink_visible = request.args.get('ink_visible', 'false') == 'true'
    lists = {
        'deck': deck,
        'hand': hand,
        'discard': discard,
        'ink': ink
    }
    item = lists[from_list].pop(index)
    lists[to_list].append((item[0], 0, item[2]))
    return redirect(url_for('main.home', deck_visible=deck_visible, hand_visible=hand_visible, discard_visible=discard_visible, ink_visible=ink_visible))
