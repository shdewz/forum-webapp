from db import db
from sqlalchemy.sql import text

def get_boards():
    sql = '''SELECT DISTINCT ON (boards.id)
             boards.id, boards.name, boards.description, threads.id AS thread_id, threads.title AS thread_title, messages.id AS message_id, messages.author_id, users.username, users.is_admin, messages.sent_at
             FROM boards LEFT JOIN threads ON threads.board_id = boards.id LEFT JOIN messages ON messages.thread_id = threads.id LEFT JOIN users ON users.id = messages.author_id
             WHERE boards.is_public = true ORDER BY boards.id, messages.sent_at DESC NULLS LAST'''
    result = db.session.execute(text(sql))
    data = result.fetchall()
    return data

def add_board(author, name, public, permissions):
    pass