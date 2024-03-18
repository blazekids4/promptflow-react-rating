from flask import Flask, redirect, request, jsonify, send_from_directory
from main import handle_prompt  # Assuming you have a function `handle_prompt` in your `main.py`
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import db, User, ChatSession, ChatMessage, Rating
from chat_routes import chat_blueprint
from datetime import datetime
from flask_login import login_user, logout_user, login_required, LoginManager, UserMixin
from werkzeug.security import generate_password_hash
from flask_migrate import Migrate


app = Flask(__name__, static_folder='../build', static_url_path='/')  # Adjust static_folder as needed
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(chat_blueprint)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    name = data.get('name')

    # Check if username or email already exists
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return jsonify(message="Username or Email already exists"), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password_hash=hashed_password, email=email, name=name)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(message="User created"), 200

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user is None or not user.check_password(password):
        return jsonify({'message': 'Invalid username or password'}), 401

    login_user(user)
    return jsonify({'message': 'Logged in successfully'}), 200

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')  # Redirect to the root, which will be handled by your React app

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return send_from_directory(app.static_folder, 'index.html')

    
@app.route('/api/chat/session', methods=['POST'])
def chat_session():
    # Create a new chat session
    chat_session = ChatSession(created_at=datetime.now(), updated_at=datetime.now())
    db.session.add(chat_session)
    db.session.commit()
    return jsonify({'session_id': chat_session.id}), 201
    
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get('prompt')
    session_id = data.get('session_id')  # Get session_id from request data
    thumbs_up = data.get('thumbs_up')
    context = data.get('context')  # Get context from request data

    # Create a new chat session if none exists
    if not session_id:
        chat_session = ChatSession(created_at=datetime.now(), updated_at=datetime.now())
        db.session.add(chat_session)
        db.session.commit()
        session_id = chat_session.id

    # Retrieve the chat history for the current session
    chat_history = ChatMessage.query.filter_by(session_id=session_id).all()
    print('Chat history:', chat_history)
    if prompt:
        # Save the user's input as a chat message
        user_message = ChatMessage(session_id=session_id, message_type='user_input', content=prompt, created_at=datetime.now())
        db.session.add(user_message)
        db.session.commit()

        # Get the response from the handle_prompt function
        response = handle_prompt(prompt, chat_history, thumbs_up, context)  # Pass context to handle_prompt

        # Save the LLM response as a chat message
        llm_message = ChatMessage(session_id=session_id, message_type='llm_response', content=response, created_at=datetime.now())
        db.session.add(llm_message)
        db.session.commit()

        return jsonify({'response': response})
    else:
        return jsonify({'error': 'No prompt provided'}), 400


@app.route('/api/chat/rate', methods=['POST'])
def rate_chat():
    print('Received rating request')
    data = request.get_json()
    session_id = data.get('session_id')
    thumbs_up = data.get('thumbs_up')
    
    print('Session ID:', session_id)
    print('Thumbs up:', thumbs_up)

    # Retrieve the last message of type 'llm_response' in the chat session
    last_message = ChatMessage.query.filter_by(message_type='llm_response').order_by(ChatMessage.created_at.desc()).first()    
    
    print('Last message:', last_message)
    
    if last_message:
        # Create a new Rating instance and link it to the last message
        rating = Rating(message_id=last_message.id, rating=thumbs_up)
        db.session.add(rating)
        db.session.commit()
        return {"message": "Rating updated successfully"}, 200
    else:
        return {"error": "No messages in the chat session"}, 400
    

@app.route('/api/chat/history', methods=['GET'])
def chat_history():
    chat_sessions = ChatSession.query.all()

    history = []
    for session in chat_sessions:
        messages = ChatMessage.query.filter_by(session_id=session.id).all()
        session_history = {'session_id': session.id, 'messages': []}
        for message in messages:
            session_history['messages'].append({
                'type': message.message_type,
                'content': message.content,
                'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        history.append(session_history)

    return jsonify({'chat_history': history})

if __name__ == '__main__':
    app.run(debug=True)
