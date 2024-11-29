from flask_wtf import FlaskForm;  
from flask_wtf.file import FileAllowed, FileField;
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, SelectField; # type: ignore
from wtforms.validators import Length, DataRequired, Email, ValidationError; # type: ignore
from A2Z_household_services import app;
from A2Z_household_services.models import User, ServiceTypes;
from flask_login import current_user; # type: ignore

class Signup_Customer_Form(FlaskForm):
    
    email = StringField('Email', validators=[DataRequired(), Email()]);

    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=30)]);

    name = StringField('Full Name', validators=[DataRequired(), Length(min=3, max=30)]);

    address = TextAreaField('Address', validators=[DataRequired()]);

    pincode = IntegerField('Pin Code', validators=[DataRequired()]);

    submitButton = SubmitField('Sign Up');
    
    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first();

        if user:
            raise ValidationError('User with the given email already exists');

class Signup_Professional_Form(FlaskForm):

    with app.app_context():

        service_tuples = ServiceTypes.query.all();

        options = [];
        for service in service_tuples:
            option = (service.name, service.name);
            options.append(option);

    email = StringField('Email', validators=[DataRequired(), Email()]);

    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=30)]);

    name = StringField('Full Name', validators=[DataRequired(), Length(min=3, max=30)]);

    service_name = SelectField('Choose Service', choices=options, validators=[DataRequired()]);

    experience = IntegerField('Enter Your Experience In Years', validators=[DataRequired()]);

    upload_files = FileField('Upload The Necessary Docs For Faster Approval In Pdf Format', validators=[FileAllowed(['pdf'], 'only pdf files allowed'), DataRequired()]);

    address = TextAreaField('Address', validators=[DataRequired()]);

    pincode = IntegerField('Pin Code', validators=[DataRequired()]);

    submitButton = SubmitField('Sign Up');
    
    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first();

        if user:
            raise ValidationError('User with the given email already exists');

class Login_Form(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()]);

    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=30)]);

    submitButton = SubmitField('Log In');
    
    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first();

        if not user:
            raise ValidationError("User with the given email doesn't exists");

class New_Service_Form(FlaskForm):

    service_name = StringField('Service Name', validators=[DataRequired(), Length(min=4, max=30)]);

    description = TextAreaField('Service Description', validators=[DataRequired()]);

    base_price = IntegerField('Base Price of the service', validators=[DataRequired()]);

    submitButton = SubmitField('Add Service');

    def validate_service_name(self, service_name):

        service = ServiceTypes.query.filter_by(name=service_name.data).first();

        if service:
            raise ValidationError('Add a new service, this service already exists');
        
class Edit_Service_Form(FlaskForm):

    service_name = StringField('Service Name', validators=[DataRequired(), Length(min=4, max=30)]);

    description = TextAreaField('Service Description', validators=[DataRequired()]);

    base_price = IntegerField('Base Price of the service', validators=[DataRequired()]);

    submitButton = SubmitField('Add Service');

class DatabaseSearchForm(FlaskForm):

    options=[
        ('name','Name'),
        ('id','Id'),
        ('pincode', 'Pincode'),
        ('service_offered', 'Service')
        ];

    search_by = SelectField('Searh By', validators=[DataRequired()], choices=options);
    
    search_box = StringField('Enter text here', validators=[DataRequired()]);

    submitButton = SubmitField('Search');

class ProfessionalPortfolio(FlaskForm):

    service_portfolio = StringField('Enter A Good Description About Your Work And Experience', validators=[DataRequired()]);

    service_price = IntegerField("Enter A Price At Which You'll serve your service", validators=[DataRequired()])

    def validate_service_price(self, service_price):

        service_type = ServiceTypes.query.filter_by(name=current_user.service_offered);

        base_price = service_type.base_price;

        if not service_price.data >= base_price:
            raise ValidationError(f'Service Price should be greater than {base_price}');