from flask import render_template, request, redirect, url_for
from . import main_bp
from shared_data import deck, hand, discard, ink

@main_bp.route('/', methods=['GET', 'POST'])
def home():
    deck_visible = request.args.get('deck_visible', 'false') == 'true'
    hand_visible = request.args.get('hand_visible', 'true') == 'true'
    discard_visible = request.args.get('discard_visible', 'false') == 'true'
    ink_visible = request.args.get('ink_visible', 'false') == 'true'
    return render_template('index.html', deck=deck, hand=hand, discard=discard, ink=ink, deck_visible=deck_visible, hand_visible=hand_visible, discard_visible=discard_visible, ink_visible=ink_visible)
