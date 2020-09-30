from flask_wtf import FlaskForm
from wtforms.validators import Required,Email
from wtforms import SubmitField, TextAreaField, StringField,ValidationError,SelectField
from ..models import User

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.', validators=[Required()])
    submit = SubmitField('Submit')

class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[Required()])
    subtitle = StringField('Subtitle', validators=[Required()])
    author = StringField('Author', validators=[Required()])
    content = TextAreaField('BlogPost', validators=[Required()])
    submit = SubmitField('Submit')
class WriterCommentForm(FlaskForm):
    description = TextAreaField('Add a comment:', validators = [Required()])
    submit = SubmitField('Submit')

class UserCommentForm(FlaskForm):
    name = StringField('Enter your name:',validators = [Required()])
    description = TextAreaField('Add a comment:', validators = [Required()])
    submit = SubmitField('Submit')

class SubscribeForm(FlaskForm):
    email = StringField( render_kw={"placeholder": "Enter your email address"}, validators=[Required()])
    submit = SubmitField('Subscribe')