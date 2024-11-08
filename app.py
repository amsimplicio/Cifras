# app.py

from flask import Flask, render_template, request, jsonify
from Ciphers import get_all_ciphers

app = Flask(__name__)

# Load all ciphers
ciphers = {cipher.name: cipher for cipher in get_all_ciphers()}

@app.route('/')
def index():
    # Pass cipher names and details to the template
    cipher_data = {name: {"example": cipher.example_text, "explanation": cipher.explanation, 
                          "requires_parameter": cipher.requires_parameter, "default_parameter": cipher.default_parameter} 
                   for name, cipher in ciphers.items()}
    first_explanation = next(iter(cipher_data.values()))["explanation"]  # Get the first explanation text
    first_example = next(iter(cipher_data.values()))["example"]  # Get the first example text
    return render_template("index.html", cipher_data=cipher_data, first_example=first_example, first_explanation=first_explanation)   

@app.route('/process', methods=['POST'])
def process_text():
    cipher_name = request.form.get("cipher")
    text = request.form.get("text")
    action = request.form.get("action")  # "encode" or "decode"
    parameter = request.form.get("parameter")
    
    cipher = ciphers.get(cipher_name)

    if action == "example":
        return jsonify({"example": cipher.example_text})

    if not cipher:
        return jsonify({"error": "Cipher not found"})

    if action == "encode":
        if cipher.requires_parameter:
            result = cipher.encode(text, parameter)
        else:
            result = cipher.encode(text)
    elif action == "decode":
        if cipher.requires_parameter:
            result = cipher.decode(text, parameter)
        else:
            result = cipher.decode(text)
        
    else:
        return jsonify({"error": "Invalid action"})

    return jsonify({"result": result,"explanation": cipher.explanation, "example": cipher.example_text})

if __name__ == "__main__":
    app.run(debug=True)
