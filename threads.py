from db import db
from sqlalchemy.sql import text
import users


def get_threads(board_id):
    sql = '''SELECT DISTINCT ON (threads.id)
             boards.id AS board_id, boards.name, threads.id, threads.title, messages.id AS message_id, messages.author_id, users.username AS author, u2.username AS last_reply, users.usergroup, messages.sent_at
             FROM boards LEFT JOIN threads ON threads.board_id = boards.id LEFT JOIN messages ON messages.thread_id = threads.id LEFT JOIN users ON users.id = threads.author_id LEFT JOIN users u2 ON u2.id = messages.author_id
             WHERE boards.id = :board_id AND boards.is_public = true ORDER BY threads.id, messages.sent_at DESC NULLS LAST'''
    result = db.session.execute(text(sql), {'board_id': board_id})
    data = result.fetchall()
    return data


def add_thread(board_id, title, content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    if len(title) > 32 or len(content) > 512:
        return False
    sql = 'INSERT INTO threads (board_id, title, author_id) VALUES (:board_id, :title, :user_id) RETURNING id'
    result = db.session.execute(
        text(sql), {'board_id': board_id, 'title': title, 'user_id': user_id})
    thread_id = result.fetchone()[0]
    db.session.execute(
        text('INSERT INTO messages (thread_id, content, author_id, sent_at) VALUES (:thread_id, :content, :user_id, NOW())'),
        {'thread_id': thread_id, 'content': content, 'user_id': user_id})
    db.session.commit()
    return thread_id


def get_thread(thread_id):
    sql = '''SELECT * FROM threads WHERE id = :thread_id'''
    result = db.session.execute(text(sql), {'thread_id': thread_id})
    data = result.fetchone()
    return data


def delete_thread(thread_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    thread = get_thread(thread_id)
    if user_id != thread.author_id:
        return False
    sql_m = 'DELETE FROM messages WHERE thread_id = :thread_id'
    db.session.execute(text(sql_m), {'thread_id': thread_id})
    sql = 'DELETE FROM threads WHERE id = :thread_id AND author_id = :user_id'
    db.session.execute(text(sql), {'thread_id': thread_id, 'user_id': user_id})
    db.session.commit()
    return True
