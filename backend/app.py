from flask import Flask, request, jsonify
from main import handle_prompt  # Assuming you have a function `handle_prompt` in your `main.py`
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import db, User, ChatSession, ChatMessage, Rating
from datetime import datetime

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:jmlgbb24@localhost:5432/genai_chat_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

    
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
        response = handle_prompt(prompt, chat_history, thumbs_up)

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
