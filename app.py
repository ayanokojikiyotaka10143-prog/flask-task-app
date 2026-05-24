from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

users = {}
tasks = {}
task_counter = 0


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in first.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if not username or not password:
            flash('Username and password are required.', 'error')
            return render_template('register.html')
        if username in users:
            flash('Username already exists.', 'error')
            return render_template('register.html')
        users[username] = password
        tasks[username] = []
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return render_template('login.html')
        if username in users and users[username] == password:
            session['username'] = username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.', 'error')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    username = session['username']
    user_tasks = tasks.get(username, [])
    return render_template('dashboard.html', tasks=user_tasks, username=username)


@app.route('/task/add', methods=['GET', 'POST'])
@login_required
def add_task():
    global task_counter
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        due_date = request.form.get('due_date', '').strip()
        if not title:
            flash('Task title is required.', 'error')
            return render_template('add_task.html')
        from datetime import datetime, date
        if due_date:
            try:
                parsed_date = datetime.strptime(due_date, '%Y-%m-%d').date()
                if parsed_date < date.today():
                    flash('Due date cannot be in the past.', 'error')
                    return render_template('add_task.html')
            except ValueError:
                flash('Invalid date format.', 'error')
                return render_template('add_task.html')
        task_counter += 1
        task = {
            'id': task_counter,
            'title': title,
            'description': description,
            'due_date': due_date,
            'completed': False
        }
        tasks[session['username']].append(task)
        flash('Task added successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_task.html')


@app.route('/task/complete/<int:task_id>')
@login_required
def complete_task(task_id):
    username = session['username']
    for task in tasks.get(username, []):
        if task['id'] == task_id:
            task['completed'] = True
            flash('Task marked as complete!', 'success')
            break
    return redirect(url_for('dashboard'))


@app.route('/task/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    username = session['username']
    tasks[username] = [t for t in tasks.get(username, []) if t['id'] != task_id]
    flash('Task deleted.', 'success')
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
