from flask import Flask, request, jsonify, render_template, redirect, url_for
from uuid import uuid4
import time

app = Flask(__name__)
reminders = []

def is_valid_content(content):
    return isinstance(content, str) and content.strip() != "" and len(content.strip()) <= 120

def is_valid_important(important):
    return isinstance(important, bool)

@app.route('/')
def index():
    sorted_reminders = sorted(reminders, key=lambda r: (not r['important'], r['createdAt']))
    return render_template('index.html', reminders=sorted_reminders)


@app.route('/create', methods=['POST'])
def create():
    content = request.form.get('content')
    important = request.form.get('important') == 'on'

    if not is_valid_content(content):
        return redirect(url_for('index'))

    new_reminder = {
        'id': str(uuid4()),
        'content': content.strip(),
        'createdAt': int(time.time() * 1000),
        'important': important
    }

    reminders.append(new_reminder)
    return redirect(url_for('index'))

@app.route('/update/<string:reminder_id>', methods=['POST'])
def update(reminder_id):
    reminder = next((r for r in reminders if r['id'] == reminder_id), None)
    if not reminder:
        return redirect(url_for('index'))

    content = request.form.get('content')
    important = request.form.get('important') == 'on'

    if is_valid_content(content):
        reminder['content'] = content.strip()
        reminder['important'] = important
    return redirect(url_for('index'))

@app.route('/delete/<string:reminder_id>', methods=['POST'])
def delete(reminder_id):
    global reminders
    reminders = [r for r in reminders if r['id'] != reminder_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

