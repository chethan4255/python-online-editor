from flask import Flask, render_template, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_code():
    data = request.get_json()
    code = data.get('code')
    user_input = data.get('input', '')

    with open('temp.py', 'w') as f:
        f.write(code)

    try:
        result = subprocess.run(
            ['python', 'temp.py'],
            input=user_input.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )
        output = result.stdout.decode() + result.stderr.decode()
    except subprocess.TimeoutExpired:
        output = "Error: Code execution timed out."

    return jsonify({'output': output})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
