import flask
import sqlite3
import os
from database import init_db
from flask import render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
app = flask.Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'some-random-secret_key')
init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login'))

    error = None

    if request.method == 'POST':
        amount = request.form['amount']
        category = request.form['category']
        description = request.form['description']
        date = request.form['date']
        try:
            amount = float(amount)
            if amount <= 0:
                error = 'Amount must be greater than 0'
        except ValueError:
            error = 'Invalid amount'

        if not category or not description:
            error = 'Category and description are required'

        if error is None:
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            cursor.execute('INSERT INTO expenses(amount, category, description, date, user_id) VALUES (?,?,?,?,?)', (amount, category, description, date, user_id))
            connection.commit()
            connection.close()

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT username FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    if user is None:
        return redirect(url_for('login'))
    cursor.execute('SELECT * FROM expenses WHERE user_id = ?', (user_id,))
    expenses = cursor.fetchall()
    cursor.execute('SELECT SUM(amount) FROM expenses WHERE user_id = ?', (user_id,))
    total = cursor.fetchone()[0]
    if total is None:
        total = 0
    cursor.execute('SELECT category, SUM(amount) FROM expenses WHERE user_id = ? GROUP BY category', (user_id,))
    category_totals = cursor.fetchall()
    connection.close()
    return render_template('index.html', username=user[0], expenses=expenses, total=total, category_totals=category_totals, error=error)

@app.route('/register', methods= ['GET', 'POST'])
def register():
    if request.method == 'POST':
       username = request.form['username']
       password = request.form['password']
       if not username or not password:
           return render_template('register.html', error='Username and password are required')
       hashed_password = generate_password_hash(password)
       connection = sqlite3.connect('database.db')
       cursor = connection.cursor()
       cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
       existing_user = cursor.fetchone()
       if existing_user is not None:
           connection.close()
           return render_template('register.html', error='Username already taken')
       cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)',(username, hashed_password))
       connection.commit()
       connection.close()
       print(f"USERNAME:{username}, PASSWORD:{hashed_password}")
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        existing_user = cursor.fetchone()
        connection.close()
        if existing_user is not None and check_password_hash(existing_user[2], password):
            session['user_id'] = existing_user[0]
            return redirect(url_for('index'))
        else:
            print("Invalid username or password")
        print(existing_user)
    return render_template('login.html')

@app.route('/edit_expense/<int:expense_id>', methods=['GET','POST'])
def edit_expense(expense_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login'))

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM expenses WHERE id = ? AND user_id = ?', (expense_id, user_id))
    expense = cursor.fetchone()
    connection.close()

    if request.method == 'POST':
        amount = request.form['amount']
        category = request.form['category']
        description = request.form['description']
        date = request.form['date']
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('UPDATE expenses SET amount = ?, category = ?, description = ?, date = ? WHERE ID = ? AND user_id = ?', (amount, category, description, date, expense_id, user_id))
        connection.commit()
        connection.close()
        return redirect(url_for('index'))

    return render_template('edit_expense.html', expense=expense)


@app.route('/delete-expense/<int:expense_id>')
def delete_expense(expense_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login'))

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM expenses WHERE ID = ? AND user_id = ?', (expense_id, user_id))
    connection.commit()
    connection.close()
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
