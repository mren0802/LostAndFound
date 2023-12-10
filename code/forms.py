from flask_wtf import FlaskForm
from wtforms import Form, StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LostItemForm(Form):
    name = StringField('Item Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    is_lost = BooleanField('Is Lost')
    submit = SubmitField('Submit')

class FoundItemForm(Form):
    name = StringField('Item Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')
