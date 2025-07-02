# Treasure Hunt Decryption Game

A Flask-based web game where players decrypt messages using various cryptographic algorithms (Caesar, Vigenère, RSA, AES) to progress through levels and uncover a treasure.

## Setup
1. Install dependencies: `pip install flask pycryptodome`
2. Run the application: `python main.py`
3. Access the game at `http://localhost:5002`

## Features
- Four levels with increasing difficulty
- Practice mode for learning cryptographic algorithms
- Game history tracking
- Hint system and algorithm explanations

## Files
- `app.py`: Main Flask application
- `game_data.py`: Level and practice data
- `crypto_algorithms.py`: Cryptographic implementations
- `game_history.py`: History management
- `main.py`: Application entry point
- `templates/`: HTML templates
- `static/`: CSS and JavaScript files
