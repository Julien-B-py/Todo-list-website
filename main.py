from flask import Flask, render_template, url_for, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms import StringField, validators, SubmitField

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SECRET_KEY'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(120), unique=True, nullable=False)


# render_kw={'autofocus': True} to set the cursor focused in the field
class AddTodoForm(Form):
    task = StringField(validators=[validators.input_required()], render_kw={'autofocus': True})


class EditTodoForm(Form):
    task = StringField(validators=[validators.input_required()], render_kw={'autofocus': True})

db.create_all()



@app.route("/", methods=['POST', 'GET'])
def home():
    form = AddTodoForm()

    todos = Todo.query.all()

    if form.validate_on_submit():
        new_task = form.task.data

        todo = Todo(task=new_task)

        # check if already exists
        already_exists = Todo.query.filter_by(task=new_task).first()

        if already_exists:
            flash('Task already exists')
            return redirect(url_for('home'))

        db.session.add(todo)
        db.session.commit()

        flash('Task successfully added')

        return redirect(url_for('home'))

    return render_template('index.html', form=form, todos=todos)





@app.route("/delete/task/<int:task_id>")
def delete(task_id):
    Todo.query.filter_by(id=task_id).delete()
    db.session.commit()

    flash('Task successfully deleted')

    return redirect(url_for('home'))


@app.route("/edit/task/<int:task_id>", methods=['POST', 'GET'])
def edit(task_id):
    form = EditTodoForm()

    todo_to_edit = Todo.query.get(task_id)
    task_to_edit = todo_to_edit.task


    if form.validate_on_submit():
        new_task = form.task.data


        todo_to_edit.task = new_task
        db.session.commit()

        flash('Task successfully edited')

        return redirect(url_for('home'))


    return render_template('edit.html', form=form, task=task_to_edit)


# T0DO recherche button, flash on every single action, checkbox for task done and move it to finished task part?


if __name__ == '__main__':
    app.run(debug=True)
