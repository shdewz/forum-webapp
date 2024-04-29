from db import db
from sqlalchemy.sql import text
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

def add_board(author, name, public, permissions):
    pass