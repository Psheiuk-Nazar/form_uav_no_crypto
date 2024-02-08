from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, StringField, PasswordField
from wtforms.validators import InputRequired, NumberRange, Length, DataRequired


class CoordinatesForm(FlaskForm):
    start_coordinate = StringField("START Coordinate", validators=[
        InputRequired(),
        Length(min=2, max=40, message="Координати повинні бути дробним числом розділенні ',' в форматі -> 11.1111 "),
    ])

    end_coordinate = StringField("FINISH Coordinate", validators=[
        InputRequired(),
        Length(min=2, max=40, message="Координати повинні бути дробним числом розділенні ',' в форматі -> 11.1111 "),
    ])

    fly_altitude = IntegerField("Висота польоту", validators=[
        InputRequired(),
        NumberRange(min=0, max=250, message="Введіть позитивне ціле число")
    ])
    finish_yaw = IntegerField('Кінцевий Азімут', validators=[
        InputRequired(),
        NumberRange(min=0, max=360, message="Введіть позитивне ціле число")
    ])

    submit = SubmitField('Зберегти')
