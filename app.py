from flask import Flask, render_template, request

app = Flask(__name__)

# Store messages (temporary storage)
messages = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # Save message
    messages.append({
        "name": name,
        "email": email,
        "message": message
    })

    return render_template('result.html', name=name, email=email, message=message)

@app.route('/messages')
def show_messages():
    return render_template('messages.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)