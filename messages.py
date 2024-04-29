from db import db
from sqlalchemy.sql import text
import users


def get_messages(thread_id):
    sql = '''SELECT m.id, b.id AS board_id, b.name, m.thread_id, t.title AS thread_title, m.content, m.author_id, m.sent_at, u.id AS user_id, u.username, u.is_admin, m.author_id = t.author_id AS op
             FROM messages m LEFT JOIN users u ON u.id = m.author_id LEFT JOIN threads t ON t.id = m.thread_id LEFT JOIN boards b ON b.id = t.board_id
             WHERE m.thread_id = :thread_id ORDER BY sent_at ASC'''
    result = db.session.execute(text(sql), {'thread_id': thread_id})
    data = result.fetchall()
    return data


def get_message(message_id):
    sql = '''SELECT * FROM messages WHERE id = :message_id'''
    result = db.session.execute(text(sql), {'message_id': message_id})
    data = result.fetchone()
    return data


def send_message(thread_id, content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    if len(content) > 512:
        return False
    sql = 'INSERT INTO messages (thread_id, content, author_id, sent_at) VALUES (:thread_id, :content, :user_id, NOW())'
    db.session.execute(
        text(sql), {'thread_id': thread_id, 'content': content, 'user_id': user_id})
    db.session.commit()
    return True


def delete_message(message_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    message = get_message(message_id)
    if user_id != message.author_id:
        return False
    sql = 'DELETE FROM messages WHERE id = :message_id AND author_id = :user_id'
    db.session.execute(
        text(sql), {'message_id': message_id, 'user_id': user_id})
    db.session.commit()
    return True
