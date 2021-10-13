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
    submit = SubmitField()


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
            flash('Already exists')
            return redirect(url_for('home'))

        db.session.add(todo)
        db.session.commit()

        return redirect(url_for('home'))


    return render_template('index.html', form=form, todos=todos)


if __name__ == '__main__':
    app.run(debug=True)
