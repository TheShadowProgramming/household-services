from flask_wtf import FlaskForm;  
from flask_wtf.file import FileAllowed, FileField;
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField; # type: ignore
from wtforms.validators import Length, DataRequired, Email, ValidationError; # type: ignore
from A2Z_household_services.models import User, ServiceTypes;

class Signup_Customer_Form(FlaskForm):
    
    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=30)])

    name = StringField('Full Name', validators=[DataRequired(), Length(min=3, max=30)])

    address = TextAreaField('Address', validators=[DataRequired()])

    pincode = IntegerField('Pin Code', validators=[DataRequired()])

    submitButton = SubmitField('Sign Up')
    
    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('User with the given email already exists')

class Signup_Professional_Form(FlaskForm):
    
    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=30)])

    name = StringField('Full Name', validators=[DataRequired(), Length(min=3, max=30)])

    service_name = StringField('choose service', validators=[DataRequired()])

    experience = IntegerField('Enter your experience in years', validators=[DataRequired()])

    upload_files = FileField('Upload the necessary docs for faster approval in pdf format', validators=[FileAllowed('pdf')])

    address = TextAreaField('Address', validators=[DataRequired()])

    pincode = IntegerField('Pin Code', validators=[DataRequired()])

    submitButton = SubmitField('Sign Up')
    
    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('User with the given email already exists')

class Login_Form(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=30)])

    submitButton = SubmitField('Log In')
    
    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first()

        if not user:
            raise ValidationError("User with the given email doesn't exists")

class New_Service_Form(FlaskForm):

    service_name = StringField('Service Name', validators=[DataRequired(), Length(min=4, max=30)])

    description = TextAreaField('Service Description', validators=[DataRequired()])

    base_price = IntegerField('Base Price of the service', validators=[DataRequired()])

    submitButton = SubmitField('Add Service')

    def validate_service_name(self, service_name):

        service = ServiceTypes.query.filter_by(name=service_name.data).first()

        if service:
            raise ValidationError('Add a new service, this service already exists')