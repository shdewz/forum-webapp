from app import app
from db import db
import boards
import threads
import messages
import users
from flask import redirect, render_template, request, session, url_for, abort


@app.route('/')
def index():
    boards_ = boards.get_boards()
    session['url'] = url_for('index')
    return render_template('index.html', data=boards_)


@app.route('/boards/<int:board_id>')
def board(board_id):
    threads_ = threads.get_threads(board_id)
    if len(threads_) == 0:
        return render_template('unauthorized.html')
    session['url'] = url_for('board', board_id=board_id)
    return render_template('board.html', data=threads_)


@app.route('/threads/<int:thread_id>', methods=['GET', 'DELETE'])
def thread(thread_id):
    if request.method == 'GET':
        messages_ = messages.get_messages(thread_id)
        if len(messages_) == 0:
            return render_template('unauthorized.html')
        session['url'] = url_for('thread', thread_id=thread_id)
        return render_template('thread.html', data=messages_)
    if request.method == 'DELETE':
        if threads.delete_thread(thread_id):
            return '200'
        else:
            return '403'


@app.route('/messages/<int:message_id>', methods=['DELETE'])
def message(message_id):
    if request.method == 'DELETE':
        if messages.delete_message(message_id):
            return '200'
        else:
            return '403'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.login(username, password):
            return redirect(session['url'])
        else:
            return render_template('login.html', error='Väärä käyttäjätunnus tai salasana')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_repeat = request.form['password-repeat']
        if password != password_repeat:
            return render_template('register.html', error='Salasanat eivät täsmää')
        if users.register(username, password):
            return redirect(session['url'])
        else:
            return render_template('register.html', error='Käyttäjän luonti ei onnistunut')


@app.route('/logout')
def logout():
    users.logout()
    return redirect(session['url'])


@app.route('/send', methods=['POST'])
def send():
    if session['csrf_token'] != request.form['csrf_token']:
        abort(403)
    content = request.form['message_content']
    thread_id = request.form['thread_id']

    if messages.send_message(thread_id, content):
        return redirect(session['url'])
    else:
        return redirect(session['url'])


@app.route('/threads/new', methods=['GET', 'POST'])
def new_thread():
    if request.method == 'GET':
        board_id = request.args.get('board_id', default=1, type=int)
        return render_template('newthread.html', board_id=board_id)
    if request.method == 'POST':
        if session['csrf_token'] != request.form['csrf_token']:
            abort(403)
        board_id = request.form['board_id']
        title = request.form['title']
        content = request.form['message_content']
        thread_id = threads.add_thread(board_id, title, content)
        if thread_id:
            return redirect(f'/threads/{thread_id}')
        return redirect(session['url'])


@app.route('/boards/new', methods=['GET', 'POST'])
def new_board():
    if request.method == 'GET':
        if (session['admin']):
            return render_template('newboard.html')
        else:
            abort(403)
    if request.method == 'POST':
        if session['csrf_token'] != request.form['csrf_token'] or not session['admin']:
            abort(403)
        title = request.form['title']
        description = request.form['description']
        private = request.form.get('private', False)
        board_id = boards.add_board(title, description, private)
        if board_id:
            return redirect(f'/boards/{board_id}')
        return redirect(session['url'])
