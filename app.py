import os
import logging
import time
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from crypto_algorithms import CryptoEngine
from game_data import GameData
from game_history import GameHistory

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "treasure_hunt_secret_key_2024")

crypto_engine = CryptoEngine()
game_data = GameData()
game_history = GameHistory()

def init_session():
    if 'game_state' not in session:
        session['game_state'] = {
            'current_level': 1,
            'score': 0,
            'completed_levels': [],
            'hints_used': 0,
            'attempts': 0,
            'start_time': time.time() 
        }

def validate_input(algorithm, user_input):
    try:
        if algorithm == 'caesar':
            shift = int(user_input)
            if not -25 <= shift <= 25:
                return False, "Độ dịch phải nằm trong khoảng -25 đến 25"
        elif algorithm == 'vigenere':
            if not user_input.isalpha():
                return False, "Khóa phải chỉ chứa các chữ cái"
        elif algorithm == 'rsa':
            try:
                private_key = eval(user_input)
                if not isinstance(private_key, tuple) or len(private_key) != 2:
                    return False, "Khóa RSA không hợp lệ"
            except:
                return False, "Định dạng khóa RSA không hợp lệ"
        elif algorithm == 'aes':
            if len(user_input) not in [16, 24, 32]:
                return False, "Khóa AES phải có độ dài 16, 24 hoặc 32 ký tự"
        return True, ""
    except Exception as e:
        return False, f"Lỗi kiểm tra đầu vào: {str(e)}"

@app.route('/')
def index():
    """Home page with game introduction"""
    init_session()
    return render_template('index.html')

@app.route('/level/<int:level_num>')
def level(level_num):
    """Display specific level"""
    init_session()
    
    if level_num < 1 or level_num > 4:
        flash('Cấp độ không hợp lệ!', 'error')
        return redirect(url_for('index'))
    
    game_state = session['game_state']
    if level_num > game_state['current_level']:
        flash('Bạn cần hoàn thành cấp độ trước!', 'warning')
        return redirect(url_for('level', level_num=game_state['current_level']))
    
    game_state['start_time'] = time.time()
    session['game_state'] = game_state
    
    level_data = game_data.get_level_data(level_num)
    return render_template('level.html', 
                         level_data=level_data, 
                         level_num=level_num,
                         game_state=game_state)

@app.route('/decrypt', methods=['POST'])
def decrypt():
    """Handle decryption attempts"""
    init_session()
    
    level_num = int(request.form.get('level'))
    user_input = request.form.get('input', '').strip()
    algorithm = request.form.get('algorithm')
    
    game_state = session['game_state']
    game_state['attempts'] += 1
    
    level_data = game_data.get_level_data(level_num)
    encrypted_message = level_data['encrypted_message']
    expected_result = level_data['expected_result']
    
    try:
        if algorithm == 'caesar':
            shift = int(user_input)
            result = crypto_engine.caesar_decrypt(encrypted_message, shift)
        elif algorithm == 'vigenere':
            keyword = user_input.upper()
            result = crypto_engine.vigenere_decrypt(encrypted_message, keyword)
        elif algorithm == 'rsa':
            private_key = eval(user_input)
            result = crypto_engine.rsa_decrypt(encrypted_message, private_key)
        elif algorithm == 'aes':
            key = user_input.encode()
            result = crypto_engine.aes_decrypt(encrypted_message, key)
        else:
            flash('Thuật toán không hợp lệ!', 'error')
            return redirect(url_for('level', level_num=level_num))
        
        if result.strip().upper() == expected_result.strip().upper():
            time_taken = int(time.time() - game_state['start_time'])
            minutes = time_taken // 60
            seconds = time_taken % 60
            time_str = f"{minutes:02d}:{seconds:02d}"
            
            points = max(100 - (game_state['attempts'] - 1) * 10 - game_state['hints_used'] * 5, 10)
            game_state['score'] += points
            game_state['completed_levels'].append(level_num)
            
            game_history.add_record(level_num, time_str, game_state['attempts'], points)
            
            if level_num < 4:
                game_state['current_level'] = level_num + 1
                flash(f'Chúc mừng! Bạn đã giải mã thành công trong {time_str} và nhận được {points} điểm!', 'success')
                return redirect(url_for('level', level_num=level_num + 1))
            else:
                flash(f'Chúc mừng! Bạn đã hoàn thành trò chơi với {game_state["score"]} điểm!', 'success')
                return redirect(url_for('complete'))
        else:
            flash(f'Sai rồi! Kết quả: "{result}". Hãy thử lại!', 'error')
            
    except Exception as e:
        logging.error(f"Decryption error: {e}")
        flash('Có lỗi xảy ra khi giải mã. Vui lòng kiểm tra đầu vào!', 'error')
    
    session['game_state'] = game_state
    return redirect(url_for('level', level_num=level_num))

@app.route('/hint/<int:level_num>')
def get_hint(level_num):
    init_session()
    game_state = session['game_state']
    game_state['hints_used'] += 1
    session['game_state'] = game_state
    
    level_data = game_data.get_level_data(level_num)
    return jsonify({'hint': level_data['hint']})

@app.route('/complete')
def complete():
    init_session()
    game_state = session['game_state']
    return render_template('complete.html', game_state=game_state)

@app.route('/reset')
def reset_game():
    session.pop('game_state', None)
    flash('Trò chơi đã được đặt lại!', 'info')
    return redirect(url_for('index'))

@app.route('/explain/<algorithm>')
def explain_algorithm(algorithm):
    explanations = game_data.get_algorithm_explanations()
    if algorithm in explanations:
        return jsonify({'explanation': explanations[algorithm]})
    return jsonify({'explanation': 'Không tìm thấy giải thích cho thuật toán này.'})

@app.route('/history')
def view_history():
    history = game_history.get_history()
    return render_template('history.html', history=history)

@app.route('/clear_history')
def clear_history():
    game_history.clear_history()
    flash('Lịch sử đã được xóa!', 'info')
    return redirect(url_for('view_history'))

@app.route('/practice')
def practice_mode():
    init_session()
    algorithms = ['caesar', 'vigenere', 'rsa', 'aes']
    return render_template('practice.html', algorithms=algorithms)

@app.route('/practice/<algorithm>')
def practice_algorithm(algorithm):
    init_session()
    if algorithm not in ['caesar', 'vigenere', 'rsa', 'aes']:
        flash('Thuật toán không hợp lệ!', 'error')
        return redirect(url_for('practice_mode'))
    
    practice_data = game_data.generate_practice_data(algorithm)
    return render_template('practice_level.html', 
                         algorithm=algorithm,
                         practice_data=practice_data)

@app.route('/practice/decrypt', methods=['POST'])
def practice_decrypt():
    init_session()
    
    algorithm = request.form.get('algorithm')
    user_input = request.form.get('input', '').strip()
    encrypted_message = request.form.get('encrypted_message')
    
    is_valid, error_message = validate_input(algorithm, user_input)
    if not is_valid:
        return jsonify({
            'success': False,
            'error': error_message
        })
    
    try:
        practice_data = game_data.generate_practice_data(algorithm)
        original_message = practice_data['message']
        
        if algorithm == 'caesar':
            shift = int(user_input)
            result = crypto_engine.caesar_decrypt(encrypted_message, shift)
        elif algorithm == 'vigenere':
            keyword = user_input.upper()
            result = crypto_engine.vigenere_decrypt(encrypted_message, keyword)
        elif algorithm == 'rsa':
            private_key = eval(user_input)
            result = crypto_engine.rsa_decrypt(encrypted_message, private_key)
        elif algorithm == 'aes':
            key = user_input.encode()
            result = crypto_engine.aes_decrypt(encrypted_message, key)
        
        is_correct = result.strip().upper() == original_message.strip().upper()
        
        return jsonify({
            'success': is_correct,
            'result': result,
            'original': original_message
        })
        
    except Exception as e:
        logging.error(f"Practice decryption error: {e}")
        return jsonify({
            'success': False,
            'error': 'Có lỗi xảy ra khi giải mã. Vui lòng kiểm tra đầu vào!'
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
