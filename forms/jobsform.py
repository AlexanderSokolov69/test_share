from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField, \
    DateTimeField, DateField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    team_leader = IntegerField('ID руководителя', validators=[DataRequired()])
    job = StringField('Название работы', validators=[DataRequired()])
    work_size = IntegerField('Объем работы', validators=[DataRequired()])
    collaborators = StringField('Список id участников', validators=[DataRequired()])
    start_date = DateField('Дата начала', validators=[DataRequired()])
    end_date = DateField('Дата окончания')
    is_finished = BooleanField('Завершена ли работа')
    submit = SubmitField('Сохранить')
