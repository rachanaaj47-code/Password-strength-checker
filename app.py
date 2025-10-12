from flask import Flask, request, jsonify, render_template
from flask import send_from_directory
from pathlib import Path
from pw_strength_checker import check_password_strength

app = Flask(__name__, static_folder='static', template_folder='templates')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json(silent=True) or {}
    password = data.get('password', '')
    feedback = check_password_strength(password)
    pw_len = len(password)

    # Enforce: until length reaches 4 chars, strength is Weak
    if pw_len > 0 and pw_len < 4:
        feedback['strength'] = 'Weak'
        # Ensure at least one actionable suggestion appears early
        starter_msg = 'Use at least 4 characters to begin with.'
        if starter_msg not in feedback['recommendations']:
            feedback['recommendations'].insert(0, starter_msg)

    # Normalize to 0-100
    total_possible = 12
    pct = int((feedback['total_score'] / total_possible) * 100)

    resp = {
        'password_length': pw_len,
        'scores': {
            'length': feedback['length_score'],
            'complexity': feedback['complexity_score'],
            'uniqueness': feedback['uniqueness_score'],
            'total': feedback['total_score'],
            'percent': pct
        },
        'strength': feedback['strength'],
        'recommendations': feedback['recommendations']
    }
    return jsonify(resp)


# Optional: serve icons or other assets from /static if needed
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)


if __name__ == '__main__':
    # Use 0.0.0.0 to allow network testing if needed
    app.run(host='0.0.0.0', port=5000, debug=True)
