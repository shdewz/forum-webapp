from db import db
from sqlalchemy.sql import text
from flask import session
import users

def get_boards():
    sql = '''SELECT DISTINCT ON (boards.id)
             boards.id, boards.name, boards.description, boards.is_public, threads.id AS thread_id, threads.title AS thread_title, messages.id AS message_id, messages.author_id, users.username, messages.sent_at, permissions.user_id
             FROM boards
             LEFT JOIN threads ON threads.board_id = boards.id
             LEFT JOIN messages ON messages.thread_id = threads.id
             LEFT JOIN users ON users.id = messages.author_id
             LEFT JOIN users users2 ON users2.id = :user_id
             LEFT JOIN permissions ON permissions.user_id = :user_id AND permissions.board_id = boards.id
             WHERE boards.is_public = true OR users2.is_admin = true OR permissions.user_id IS NOT NULL ORDER BY boards.id, messages.sent_at DESC NULLS LAST'''
    result = db.session.execute(text(sql), {'user_id': users.user_id()})
    data = result.fetchall()
    return data

def add_board(title, description, private):
    if users.user_id() == 0 or not session['admin']:
        return False
    if len(title) > 24 or len(description) > 48:
        return False
    sql = 'INSERT INTO boards (name, description, is_public) VALUES (:name, :description, :is_public) RETURNING id'
    result = db.session.execute(
        text(sql), {'name': title, 'description': description, 'is_public': 'TRUE' if not private else 'FALSE'})
    thread_id = result.fetchone()[0]
    db.session.commit()
    return thread_id