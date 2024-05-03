from db import db
from sqlalchemy.sql import text
from flask import session
import users


def add_permissions(board_id, username):
    if users.user_id() == 0 or not session['admin']:
        return False

    user = users.find_user(username)
    if not user:
        return False

    sql = 'INSERT INTO permissions (board_id, user_id) VALUES (:board_id, :user_id)'
    db.session.execute(text(sql), {'board_id': board_id, 'user_id': user.id})
    db.session.commit()
    return user
