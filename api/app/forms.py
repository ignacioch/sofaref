from flask_wtf import FlaskForm
from wtforms import BooleanField,TextField, IntegerField, TextAreaField, SubmitField, RadioField,SelectField, DateTimeField
import sys
from wtforms import validators, ValidationError
from wtforms.validators import Required, Optional


#Will not be used eventually, just a template
class pre_modify(FlaskForm):

  Action = RadioField('Action', choices = [('add','Add'),('update','Update')])
  Type = SelectField('Type to modify', choices = [('match', 'Match'), ('event', 'Event'), ('media', 'Media')])

  Id = IntegerField("id")
  Match_datetime = DateTimeField(
    "Match time: Please use format 2017-01-21 10:10:10", format="%Y-%m-%d %H:%M:%S", 
    validators = [validators.optional()]
    )
 #code to find action, type etc
 #print(Action.__dict__)
 #for arg in vars(Action):
 #	if arg=='args':
 #		input = getattr(Action,arg)[0]
 #		print(getattr(Action,arg)[0])
  Team_A = TextField("Team A",validators = [validators.optional()],default = None)
  Team_B = TextField("Team B",validators = [validators.optional()])
  Competition = TextField("Competition",validators = [validators.optional()])
  Match_status = IntegerField("Match status: Select from 0,1,2",validators = [validators.optional()])
  submit = SubmitField("Send")


class first_selection(FlaskForm):
  Action = RadioField('Action', choices = [('add','Add'),('update','Update')])
  Type = SelectField('Type to modify',validators = [validators.Required()], choices = [('match', 'Match'), ('event', 'Event'), ('media', 'Media')])
  submit = SubmitField("Send")



class add_match(FlaskForm):
  match_id = IntegerField("id",validators=[ validators.NumberRange(min=0)])
  match_datetime = DateTimeField(
    "Match time: Please use format 2017-01-21 10:10:10", format="%Y-%m-%d %H:%M:%S", 
    validators = [validators.DataRequired()]
    )
  team_a = TextField("Team A",validators = [validators.DataRequired()],default = None)
  team_b = TextField("Team B",validators = [validators.DataRequired()])
  competition = TextField("Competition",validators = [validators.DataRequired()])
  match_status = IntegerField("Match status: Select from 0,1,2",validators = [validators.NumberRange(min=0, max =2)])
  submit = SubmitField("Send")



class update_match(FlaskForm):
  match_id = IntegerField("id",validators=[ validators.NumberRange(min=0)])
  match_datetime = DateTimeField(
    "Match time: Please use format 2017-01-21 10:10:10", format="%Y-%m-%d %H:%M:%S", 
    validators = [validators.optional()]
    )
  team_a = TextField("Team A",validators = [validators.optional()],default = None)
  team_b = TextField("Team B",validators = [validators.optional()])
  competition = TextField("Competition",validators = [validators.optional()])
  match_status = IntegerField("Match status: Select from 0,1,2",validators = [validators.optional(),validators.NumberRange(min=0, max =2)])
  submit = SubmitField("Send")


class add_event(FlaskForm):
  event_id = IntegerField("Event id",validators=[ validators.NumberRange(min=0)])
  match_id = IntegerField("Match id",validators=[ validators.NumberRange(min=0)])
  description = TextField("Description",validators = [validators.DataRequired()])
  question = TextField("Question text",validators = [validators.DataRequired()])
  submit = SubmitField("Send")


class update_event(FlaskForm):
  event_id = IntegerField("Event id",validators=[ validators.NumberRange(min=0)])
  match_id = IntegerField("Match id",validators=[validators.optional(), validators.NumberRange(min=0)])
  description = TextField("Description",validators = [validators.optional(),validators.DataRequired()])
  question = TextField("Question text",validators = [validators.optional(),validators.DataRequired()])
  submit = SubmitField("Send")


class add_media(FlaskForm):
  media_id = IntegerField("Media id",validators=[validators.InputRequired(), validators.NumberRange(min=0)])
  event_id = IntegerField("Event id",validators=[validators.InputRequired(), validators.NumberRange(min=0)])
  media_type = IntegerField("Media type: Select from 0,1,2",validators = [validators.InputRequired(),validators.NumberRange(min=0, max =2)])
  media_url = TextField("URL",validators = [validators.DataRequired()])
  submit = SubmitField("Send") 

class update_media(FlaskForm):
  media_id = IntegerField("Media id",validators=[validators.InputRequired(), validators.NumberRange(min=0)])
  event_id = IntegerField("Event id",validators=[validators.optional(), validators.NumberRange(min=0)])
  media_type = IntegerField("Media type: Select from 0,1,2",validators = [validators.optional(),validators.NumberRange(min=0, max =2)])
  media_url = TextField("URL",validators = [validators.optional()])
  submit = SubmitField("Send") 


class vote_form(FlaskForm):
  vote_id = IntegerField("Vote id",validators=[validators.InputRequired(), validators.NumberRange(min=0)])
  user_id = IntegerField("User id",validators=[validators.InputRequired(), validators.NumberRange(min=0)])
  vote = RadioField('Vote', choices = [('1','Agree'),('0','Disaggree')])
  event_id = IntegerField("Event id",validators=[validators.InputRequired(), validators.NumberRange(min=0)])
  submit = SubmitField("Send") 