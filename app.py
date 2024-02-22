from flask import Flask, render_template, request, redirect, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__, static_folder='static', template_folder='static')

# Configuration
USERS_FILE = 'data/users.txt'
POSTS_FILE = 'data/posts.txt'
IMAGES_FOLDER = 'data/images'

# Helper functions
def read_users():
    users = []
    try:
        with open(USERS_FILE, 'r') as file:
            for line in file:
                username, password = line.strip().split(',')
                users.append({'username': username, 'password': password})
    except FileNotFoundError:
        pass  # Handle file not found if necessary
    return users

def write_user(username, password):
    with open(USERS_FILE, 'a') as file:
        file.write(f'{username},{password}\n')

def read_posts():
    posts = []
    try:
        with open(POSTS_FILE, 'r') as file:
            for line in file:
                data = line.strip().split(',')
                title = data[0]
                username = data[1]
                description = data[2]
                filename = data[3] if len(data) > 3 else None
                posts.append({'title': title, 'username': username, 'description': description, 'filename': filename})
    except FileNotFoundError:
        pass  # Handle file not found if necessary
    return posts

def write_post(title, username, description, filename):
    with open(POSTS_FILE, 'a') as file:
        file.write(f'{title},{username},{description},{filename}\n')

# Routes
@app.route('/')
def home():
    return send_from_directory('static', 'loginandsignup.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    users = read_users()

    # Check if username already exists
    if any(user['username'] == username for user in users):
        return 'Username is taken.'

    # Add the new user
    write_user(username, password)

    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    users = read_users()

    # Check if the username and password match
    if any(user['username'] == username and user['password'] == password for user in users):
        return redirect('/logged_in_home')
    else:
        return 'Invalid username or password'

@app.route('/logged_in_home')
def logged_in_home():
    posts = read_posts()
    return render_template('logged_in_home.html', posts=posts)

@app.route('/post', methods=['POST'])
def post():
    title = request.form['title']
    username = request.form['username']
    description = request.form['description']

    # Handle file upload
    file = request.files['image']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(IMAGES_FOLDER, filename))
        print(f"Saved filename: {filename}")
    else:
        filename = None

    # Add the new post
    write_post(title, username, description, filename)

    # Redirect back to the logged_in_home page
    return redirect('/logged_in_home')

if __name__ == '__main__':
    # Initialize users.txt, posts.txt, and images folder if they don't exist
    for filename in [USERS_FILE, POSTS_FILE]:
        if not os.path.exists(filename):
            open(filename, 'a').close()

    images_folder = os.path.join(os.getcwd(), IMAGES_FOLDER)
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    app.run(debug=True)
