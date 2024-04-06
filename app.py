from flask import Flask
from flask import redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
app.secret_key = getenv('SECRET')
db = SQLAlchemy(app)


@app.route('/')
def index():
    sql = 'SELECT DISTINCT ON (boards.id) boards.id, boards.name, boards.description, threads.id AS thread_id, threads.title AS thread_title, messages.id AS message_id, messages.author_id, users.username, users.usergroup, messages.sent_at FROM boards LEFT JOIN threads ON threads.board_id = boards.id LEFT JOIN messages ON messages.thread_id = threads.id LEFT JOIN users ON users.id = messages.author_id WHERE boards.is_public = true ORDER BY boards.id, messages.sent_at DESC NULLS LAST'
    result = db.session.execute(text(sql))
    boards = result.fetchall()
    session['url'] = url_for('index')
    return render_template('index.html', data=boards)


@app.route('/boards/<int:id>')
def board(id):
    sql = 'SELECT DISTINCT ON (threads.id) boards.id AS board_id, boards.name, threads.id, threads.title, messages.id AS message_id, messages.author_id, users.username AS author, u2.username AS last_reply, users.usergroup, messages.sent_at FROM boards LEFT JOIN threads ON threads.board_id = boards.id LEFT JOIN messages ON messages.thread_id = threads.id LEFT JOIN users ON users.id = threads.author_id LEFT JOIN users u2 ON u2.id = messages.author_id WHERE boards.id = :board_id AND boards.is_public = true ORDER BY threads.id, messages.sent_at DESC NULLS LAST'
    result = db.session.execute(text(sql), {'board_id': id})
    threads = result.fetchall()
    if len(threads) == 0:
        return render_template('unauthorized.html')
    session['url'] = url_for('board', id=id)
    return render_template('board.html', data=threads)


@app.route('/threads/<int:id>')
def thread(id):
    sql = 'SELECT m.id, b.id AS board_id, b.name, m.thread_id, t.title AS thread_title, m.content, m.author_id, m.sent_at, u.id AS user_id, u.username, u.usergroup, m.author_id = t.author_id AS op FROM messages m LEFT JOIN users u ON u.id = m.author_id LEFT JOIN threads t ON t.id = m.thread_id LEFT JOIN boards b ON b.id = t.board_id WHERE m.thread_id = :thread_id ORDER BY sent_at ASC;'
    result = db.session.execute(text(sql), {'thread_id': id})
    messages = result.fetchall()
    if len(messages) == 0:
        return render_template('unauthorized.html')
    session['url'] = url_for('thread', id=id)
    return render_template('thread.html', data=messages)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login-submit', methods=['POST'])
def login_submit():
    username = request.form['username']
    password = request.form['password']

    sql = 'SELECT id, password FROM users WHERE username=:username'
    result = db.session.execute(text(sql), {'username': username})
    user = result.fetchone()
    if not user:
        # missing user
        # todo: add error message / redirect to sign up
        return redirect('login')
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            # correct password
            session['username'] = username
            return redirect(session['url'])
        else:
            # invalid password
            # todo: add error message
            return redirect('login')


@app.route('/logout')
def logout():
    del session['username']
    return redirect(session['url'])
