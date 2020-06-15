from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,IntegerField
from wtforms.validators import DataRequired


class ProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Upload')


class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Upload')


class ReplyForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    id = IntegerField('id',validators=[DataRequired()])
    submit1 = SubmitField('post')


class ReplyReplyForm(FlaskForm):
    content = TextAreaField('Reply', validators=[DataRequired()])
    id = IntegerField('id',validators=[DataRequired()])
    submit2 = SubmitField('reply')
