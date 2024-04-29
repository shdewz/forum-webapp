from app import app
from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
import secrets


def user_id():
    return session.get('user_id', 0)


def login(username, password):
    sql = 'SELECT id, username, password, is_admin FROM users WHERE username=:username'
    result = db.session.execute(text(sql), {'username': username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['admin'] = user.is_admin
            session['csrf_token'] = secrets.token_hex(16)
            return True
        else:
            return False


def register(username, password, is_admin):
    hash_value = generate_password_hash(password)
    try:
        sql = 'INSERT INTO users (username, password, is_admin) VALUES (:username, :password, :is_admin)'
        db.session.execute(
            text(sql), {'username': username, 'password': hash_value, 'is_admin': 'TRUE' if is_admin else 'FALSE'})
        db.session.commit()
    except:
        return False
    return login(username, password)


def logout():
    del session['user_id']
    del session['username']
    del session['admin']
