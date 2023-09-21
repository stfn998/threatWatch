from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Optional, NumberRange
from datetime import datetime
from ThreatWatch.enums import IncidentReliability, IncidentType, IndustryType

class IncidentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired(), NumberRange(min=1900, max=datetime.now().year)])
    description = TextAreaField('Description', validators=[DataRequired()])
    impact = TextAreaField('Impact', validators=[DataRequired()])
    actions_taken = TextAreaField('Taken actions', validators=[DataRequired()])
    reliability = SelectField('Reliability', choices=[(choice.value, choice.value) for choice in IncidentReliability], validators=[DataRequired()])
    industry_type = SelectField('Industry', choices=[(choice.value, choice.value) for choice in IndustryType], validators=[DataRequired()])
    incident_type = SelectField('Type', choices=[(choice.value, choice.value) for choice in IncidentType], validators=[Optional()])
    submit = SubmitField('Add incident')
