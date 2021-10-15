from flask_wtf import FlaskForm
from wtforms import StringField, validators


# render_kw={'autofocus': True} to set the cursor focused in the field
class AddTodoForm(FlaskForm):
    task = StringField(validators=[validators.input_required()], render_kw={'autofocus': True})


class EditTodoForm(FlaskForm):
    task = StringField(validators=[validators.input_required()], render_kw={'autofocus': True})
