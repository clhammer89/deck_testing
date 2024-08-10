from flask import Flask
import webbrowser
import threading
from routes import main_bp, deck_bp, assets_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(deck_bp)
app.register_blueprint(assets_bp)

def open_browser():
    webbrowser.open_new_tab("http://127.0.0.1:5000/")

if __name__ == '__main__':
    # Start the Flask app in a separate thread
    threading.Timer(1, open_browser).start()
    app.run(debug=False, port=5001)
