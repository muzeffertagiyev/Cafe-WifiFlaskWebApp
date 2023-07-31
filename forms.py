from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, ValidationError, EmailField , URLField
from wtforms.validators import DataRequired, Length, URL, Email, EqualTo

choices = ['✅', '❌']

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=4, max=200)])
    email = EmailField('Email', validators=[DataRequired(),Length(min=4, max=300) ,Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8,max=300)])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),Length(min=8,max=300),
        EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Register')
    def validate_confirm_password(self, field):
        if field.data != self.password.data:
            raise ValidationError('Passwords must match.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Length( max=200)])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8, max=300)])
    submit = SubmitField('Let Me In')


class CafeForm(FlaskForm):
    name = StringField('Cafe name', validators=[DataRequired(),Length(min=3,max=250)])
    map_url = URLField('Cafe Location on Google Maps(URL)',validators=[URL(),Length(min=20, max=300), DataRequired()])
    img_url = URLField('Image URL',validators=[URL(),Length(min=20, max=300), DataRequired()])
    location = StringField('City Name', validators=[DataRequired(),Length(min=3,max=250)])
    seats = StringField('Number of Seats', validators=[DataRequired(),Length(max=250)])
    has_toilet = SelectField('Has Toilet?', choices=choices, validators=[DataRequired()])
    has_wifi = SelectField('Has Wifi?', choices=choices, validators=[DataRequired()])
    has_sockets = SelectField('Has Sockets?', choices=choices,  validators=[DataRequired()])
    can_take_calls = SelectField('Can you make Reservations?', choices=choices, validators=[DataRequired()])
    coffee_price = StringField('What is coffee price, Please add Currency too. (EUR, USD...)',validators=[DataRequired(),Length(max=250)])
    submit = SubmitField('Submit')
    

class UpdateDetailsForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=4, max=200)])
    email = EmailField('Email', validators=[DataRequired(),Length( max=300),Email()])
    submit = SubmitField('Update Details')


class ResetPasswordForm(FlaskForm):
    old_password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=300)])
    new_password = PasswordField('Password', validators=[DataRequired(), Length(min=8,max=300)])
    new_confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),Length(min=8,max=300),
        EqualTo('new_password', message='Passwords must match.')
    ])
    submit = SubmitField('Reset Password')
    def validate_confirm_password(self, field):
        if field.data != self.new_password.data:
            raise ValidationError('Passwords must match.')
