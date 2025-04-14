from flask import Flask, request, jsonify, render_template, redirect, url_for
from uuid import uuid4
import time

app = Flask(__name__)
reminders = []

def is_valid_content(content):
    return isinstance(content, str) and content.strip() != "" and len(content.strip()) <= 120

def is_valid_important(important):
    return isinstance(important, bool)

# Interfaz HTML principal
@app.route('/')
def index():
    print("🔥 Entrando a la ruta /")
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

# API REST (como ya tenías)
@app.route('/api/reminders', methods=['GET'])
def list_reminders():
    sorted_reminders = sorted(reminders, key=lambda r: (not r['important'], r['createdAt']))
    return jsonify(sorted_reminders), 200

@app.route('/api/reminders', methods=['POST'])
def create_reminder():
    data = request.get_json()
    
    content = data.get('content')
    important = data.get('important', False)

    if not is_valid_content(content) or ("important" in data and not is_valid_important(important)):
        return jsonify({'error': 'Datos inválidos'}), 400

    new_reminder = {
        'id': str(uuid4()),
        'content': content.strip(),
        'createdAt': int(time.time() * 1000),
        'important': important
    }

    reminders.append(new_reminder)
    return jsonify(new_reminder), 201

@app.route('/api/reminders/<string:reminder_id>', methods=['PATCH'])
def update_reminder(reminder_id):
    data = request.get_json()
    reminder = next((r for r in reminders if r['id'] == reminder_id), None)

    if reminder is None:
        return jsonify({'error': 'Recordatorio no encontrado'}), 404

    if 'content' in data:
        if not is_valid_content(data['content']):
            return jsonify({'error': 'Content inválido'}), 400
        reminder['content'] = data['content'].strip()

    if 'important' in data:
        if not is_valid_important(data['important']):
            return jsonify({'error': 'Important inválido'}), 400
        reminder['important'] = data['important']

    return jsonify(reminder), 200

@app.route('/api/reminders/<string:reminder_id>', methods=['DELETE'])
def delete_reminder(reminder_id):
    global reminders
    initial_length = len(reminders)
    reminders = [r for r in reminders if r['id'] != reminder_id]

    if len(reminders) == initial_length:
        return jsonify({'error': 'Recordatorio no encontrado'}), 404

    return '', 204

print("Flask está cargando este archivo correctamente.")
if __name__ == '__main__':
    app.run(debug=True)

