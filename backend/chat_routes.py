from flask import Blueprint, jsonify, render_template
from models import ChatSession

chat_blueprint = Blueprint('chat', __name__)

@chat_blueprint.route('/api/chat/session/<int:session_id>')
def chat_session_detail(session_id):
    chat_session = ChatSession.query.get(session_id)
    if not chat_session:
        return jsonify({'error': 'Chat session not found'}), 404
    return render_template(
        'prompt_template.jinja2',
        session=chat_session,
        user=chat_session.user
    )
