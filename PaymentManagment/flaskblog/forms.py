from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=30)])
    address = StringField('Address',validators=[Length(min=2, max=50)])

    phonenumber = StringField('PhoneNumber',validators=[DataRequired()])

    plotnumber = StringField('PlotNumber',validators=[DataRequired(), Length(min=2, max=10)])
    flatnumber = StringField('FlatNumber')

    submit = SubmitField('Register')

    def validate_phonenumber(self,phonenumber):
        #user = User.query.filter_by(Username=username.data).first()
        phno = User.query.filter_by(PhoneNumber=phonenumber.data).first()
        if phno :
            raise ValidationError('That Phone no is alredy in the record')

    def validate_plotnumber(self, plotnumber):
        # user = User.query.filter_by(Username=username.data).first()
        pltno = User.query.filter_by(PlotNumber=plotnumber.data).first()
        if pltno:
            raise ValidationError('That Plot No is alredy in the record.')




class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class PaymentForm(FlaskForm):
    phonenumber = StringField('PhoneNumber', validators=[DataRequired()])
    receiptNo = StringField('ReceiptNo',validators=[DataRequired()])
    amount = StringField('Amout', validators=[DataRequired()])
    donation = StringField('Donation')
    submit = SubmitField('Pay')

class Search(FlaskForm):
    phonenumber = StringField('PhoneNumber', validators=[DataRequired()])
    submit = SubmitField('Search')


class Delete(FlaskForm):
    phonenumber = StringField('PhoneNumber', validators=[DataRequired()])
    submit = SubmitField('Delete')





