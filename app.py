from flask import Flask, request, jsonify, render_template
import subprocess
import tempfile
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_code():
    data = request.json
    code = data.get('code', '')

    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
        tmp.write(code.encode())
        tmp_filename = tmp.name

    try:
        result = subprocess.run(
            ['python', tmp_filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5,
            text=True
        )
        output = result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        output = "Error: Code execution timed out."
    finally:
        os.remove(tmp_filename)

    return jsonify({'output': output})

if __name__ == '__main__':
    app.run(debug=True)
