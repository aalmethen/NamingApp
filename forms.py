from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SubmitField


class AddForm(FlaskForm):

    name = StringField('ما الاسم المناسب بنظرك ')
    submit = SubmitField('شارك')
