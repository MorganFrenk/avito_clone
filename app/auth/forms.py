from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Введите пароль', validators=[DataRequired()])
    remember_me = BooleanField('Оставаться в системе')
    submit = SubmitField('Подтвердить')

class RegForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Length(1, 64), Email()])
    fname = StringField('Введите ваше имя, которое будет видно другим пользователям', 
        validators=[DataRequired(), Length(2, 64), 
                    Regexp('^[А-Яа-я]+$', 0,
                            'Имя может содержать только буквы русского алфавита.')])
    lname = StringField('Введите вашу фамилию (опционально)', validators=[Length(2, 64),
        Regexp('^[А-Яа-я]+$', 0,
                'Фамилия может содержать только буквы русского алфавита.')])
    password = PasswordField('Введите пароль', validators=[DataRequired(), Length(8, 64),
        EqualTo('pass_conf', message='Пароли не совпадают.')])
    pass_conf = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('E-mail уже зарегистрирован')
    