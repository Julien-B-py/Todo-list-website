from flask_wtf import Form
from wtforms import StringField, validators


# render_kw={'autofocus': True} to set the cursor focused in the field
class AddTodoForm(Form):
    task = StringField(validators=[validators.input_required()], render_kw={'autofocus': True})


class EditTodoForm(Form):
    task = StringField(validators=[validators.input_required()], render_kw={'autofocus': True})
