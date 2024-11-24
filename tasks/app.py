from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

import hazelcast

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)

client = hazelcast.HazelcastClient(cluster_name="tasks")
mapp = client.get_map("tasks").blocking()


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    picture = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, nullable=False)


@app.route('/', methods=['GET'])
def index():
    user_uuid = request.args.get('uuid')
    session['uuid'] = user_uuid
    print(f"User UUID: {user_uuid}")
    tasks = Task.query.filter_by(user_id=user_uuid).all()
    return render_template('index.html', tasks=tasks, user_uuid=session.get('uuid'))



@app.route('/add', methods=['GET', 'POST'])
def add():
    user_uuid = session.get('uuid')

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        picture = request.files['picture'] if 'picture' in request.files else None

        if picture:
            filename = secure_filename(picture.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            picture.save(save_path)
        else:
            filename = None

        if user_uuid is None:
            # Handle unauthorized access
            return redirect(url_for('index', uuid=user_uuid))

        new_task = Task(title=title, description=description, picture=filename, user_id=user_uuid)
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for('index', uuid=user_uuid))

    return render_template('add.html', user_uuid=user_uuid)



@app.route('/delete/<int:task_id>', methods=['GET', 'POST'])
def delete(task_id):
    task = Task.query.get_or_404(task_id)

    if request.method == 'POST':
        db.session.delete(task)
        mapp.remove(task_id)
        db.session.commit()
        return redirect(url_for('index', uuid=session.get('uuid')))

    return render_template('delete.html', task=task)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
