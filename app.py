from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "secret123"

# MongoDB connection
client = MongoClient("mongodb+srv://2403031590069_db_user:vidhi_singh2005@cluster0.t02oesu.mongodb.net/?appName=Cluster0")
db = client["notes_app"]

users = db["users"]
notes = db["notes"]

# Home
@app.route('/')
def index():
    if 'user' not in session:
        return redirect('/login')
    
    user_notes = notes.find({"user": session['user']})
    return render_template('index.html', notes=user_notes)

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        if users.find_one({"username": username}):
            return "User already exists!"

        users.insert_one({"username": username, "password": password})
        return redirect('/login')

    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = users.find_one({"username": request.form['username']})

        if user and check_password_hash(user['password'], request.form['password']):
            session['user'] = user['username']
            return redirect('/')
        else:
            return "Invalid credentials"

    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

# Add Note
@app.route('/add', methods=['POST'])
def add_note():
    if 'user' in session:
        notes.insert_one({
            "text": request.form['note'],
            "user": session['user']
        })
    return redirect('/')

# Delete Note
@app.route('/delete/<id>')
def delete_note(id):
    notes.delete_one({"_id": ObjectId(id)})
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)