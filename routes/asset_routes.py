from flask import Blueprint, request, redirect, url_for
import os
import requests
import json
from shared_data import deck

assets_bp = Blueprint('assets', __name__)

# Load card list from the local JSON file
with open('card_list.json', 'r') as f:
    card_list = json.load(f)

@assets_bp.route('/load_assets', methods=['POST'])
def load_assets():
    deck_visible = request.form.get('deck_visible') == 'true'
    hand_visible = request.form.get('hand_visible') == 'true'
    discard_visible = request.form.get('discard_visible') == 'true'
    ink_visible = request.form.get('ink_visible') == 'true'

    os.makedirs('static/card_assets', exist_ok=True)

    for item, _, formatted_item in deck:
        for card in card_list:
            if card["name"] == formatted_item.replace(".webp", ""):
                card_id = card["id"]
                image_url = f"https://static.dotgg.gg/lorcana/cards/{card_id}.webp"
                image_path = os.path.join('static/card_assets', formatted_item)
                if not os.path.exists(image_path):  # Avoid re-downloading if already exists
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        with open(image_path, 'wb') as f:
                            f.write(response.content)
                    else:
                        print(f"Failed to download {image_url}")
                break
    return redirect(url_for('main.home', deck_visible=deck_visible, hand_visible=hand_visible, discard_visible=discard_visible, ink_visible=ink_visible))
