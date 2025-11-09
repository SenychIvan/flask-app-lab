from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, SelectField, DateTimeLocalField
from wtforms.validators import DataRequired, Length
from datetime import datetime

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=150)])
    content = TextAreaField("Content", validators=[DataRequired()])
    category = SelectField(
        "Category",
        choices=[
            ("news", "News"),
            ("publication", "Publication"),
            ("tech", "Tech"),
            ("other", "Other")
        ],
        default="other"
    )
    is_active = BooleanField("Active", default=True)
    publish_date = DateTimeLocalField("Publish Date", default=datetime.utcnow, format='%Y-%m-%dT%H:%M')
    submit = SubmitField("Save Post")
