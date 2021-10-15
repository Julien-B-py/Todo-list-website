import datetime
import os

from flask import Flask, render_template, url_for, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

from forms import AddTodoForm, EditTodoForm

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(120), unique=True, nullable=False)
    date_completed = db.Column(db.String(120), nullable=True)


# db.create_all()


@app.route("/", methods=['POST', 'GET'])
def home():
    """
    Main page route.
    Display all saved todos and allow the user to add new ones.
    """
    # Create a new form to allow the user to add a todo to the database
    form = AddTodoForm()

    # If user submitted the form
    if form.validate_on_submit():
        # Get data typed by user
        new_task = form.task.data
        # Check if the task already exists
        already_exists = Todo.query.filter_by(task=new_task).first()
        # If already exists redirect to home page and display a message
        if already_exists:
            flash('Task already exists')
            return redirect(url_for('home'))
        # Else create a new database entry
        todo = Todo(task=new_task)
        db.session.add(todo)
        db.session.commit()
        flash('Task successfully added')
        return redirect(url_for('home'))

    # If user loaded home page without submitting the form
    # Get all todos from database
    todos = Todo.query.all()
    # For every todo check if the date_completed column is different from NULL and if so add 1 everytime
    completed_count = sum(1 for todo in todos if todo.date_completed is not None)
    # If completed todos amount is equal to the size of todos list, then our current todo list is empty
    is_empty = (completed_count == len(todos))
    # Check if any todo has been completed to allow the display of "completed todos link"
    completed = any(todo.date_completed for todo in todos)
    # Pass todos and completed (kwargs) to render the html
    return render_template('index.html', form=form, todos=todos, completed=completed, is_empty=is_empty)


@app.route("/delete/task/<int:task_id>")
def delete(task_id):
    """
    Delete todo route.
    Allow the user to delete a todo from the database by using his id.
    parameters:
            - name: task_id
              in: path
              description: todo (task) id
              type: integer
              required: true
    """

    Todo.query.filter_by(id=task_id).delete()
    db.session.commit()
    flash('Task successfully deleted')

    return redirect(url_for('home'))


@app.route("/complete/task/<int:task_id>")
def complete(task_id):
    """
    Complete todo route.
    Allow the user to change the todo status to completed by using his id.
    parameters:
            - name: task_id
              in: path
              description: todo (task) id
              type: integer
              required: true
    """
    # Get the todo from the database
    todo_to_edit = Todo.query.get(task_id)
    # Fill the date_completed column with the current date formatted
    todo_to_edit.date_completed = datetime.datetime.today().strftime("%m/%d/%Y")
    db.session.commit()
    flash('Task successfully completed')

    return redirect(url_for('home'))


@app.route("/completed")
def get_completed_tasks():
    """
    Completed todos route.
    Allow the user to display a list of all completed todos with the date of completion
    """
    # Get all todos from database that have the date of completion column filled
    results = Todo.query.filter(Todo.date_completed != None)

    return render_template('completed.html', results=results)


@app.route("/edit/task/<int:task_id>", methods=['POST', 'GET'])
def edit(task_id):
    """
    Edit todo route.
    Allow the user to change the todo description by using his id.
    parameters:
            - name: task_id
              in: path
              description: todo (task) id
              type: integer
              required: true
    """
    form = EditTodoForm()
    # Get the current todo description to display it in the HTML
    todo_to_edit = Todo.query.get(task_id)
    task_to_edit = todo_to_edit.task

    if form.validate_on_submit():
        # Get the new todo description inputted by the user
        new_task = form.task.data
        # Update the value in the database
        todo_to_edit.task = new_task
        db.session.commit()

        flash('Task successfully edited')

        return redirect(url_for('home'))

    return render_template('edit.html', form=form, task=task_to_edit)


if __name__ == '__main__':
    app.run(debug=True)
