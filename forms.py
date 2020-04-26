from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class DataForm(FlaskForm):

    url = StringField('Reddit Post Link:', validators=[DataRequired()])
    submit = SubmitField('Get Flair')
