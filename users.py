from app import app
from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
import secrets


def user_id():
    return session.get('user_id', 0)


def login(username, password):
    sql = 'SELECT id, username, password FROM users WHERE username=:username'
    result = db.session.execute(text(sql), {'username': username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['csrf_token'] = secrets.token_hex(16)
            return True
        else:
            return False


def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = 'INSERT INTO users (username, password, usergroup) VALUES (:username, :password, 0)'
        db.session.execute(
            text(sql), {'username': username, 'password': hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)


def logout():
    del session['user_id']
    del session['username']
