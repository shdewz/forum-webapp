from db import db
from sqlalchemy.sql import text

def get_threads(board_id):
    sql = '''SELECT DISTINCT ON (threads.id)
             boards.id AS board_id, boards.name, threads.id, threads.title, messages.id AS message_id, messages.author_id, users.username AS author, u2.username AS last_reply, users.usergroup, messages.sent_at
             FROM boards LEFT JOIN threads ON threads.board_id = boards.id LEFT JOIN messages ON messages.thread_id = threads.id LEFT JOIN users ON users.id = threads.author_id LEFT JOIN users u2 ON u2.id = messages.author_id
             WHERE boards.id = :board_id AND boards.is_public = true ORDER BY threads.id, messages.sent_at DESC NULLS LAST'''
    result = db.session.execute(text(sql), {'board_id': board_id})
    data = result.fetchall()
    return data

def add_thread(board_id, author, title, content):
    pass