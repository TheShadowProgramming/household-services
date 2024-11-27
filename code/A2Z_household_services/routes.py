from flask import render_template, redirect, url_for, flash, request;
import os;
from A2Z_household_services import app, db, flask_bcrypt_instance, login_manager;
from flask_login import current_user, login_user, logout_user, login_required; # type: ignore
from A2Z_household_services.forms import Signup_Customer_Form, Signup_Professional_Form, Login_Form, New_Service_Form;
from A2Z_household_services.models import User, ServiceTypes;

@login_manager.user_loader
def load_user(user_id):

    return User.query.get(user_id)

@app.route("/")
def home():
    services_types = ServiceTypes.query.all()

    return render_template('routes/home_content.html', title='Home', current_user=current_user, services_types=services_types)

@app.route("/signup-customer", methods=['POST', 'GET'])
def signup_customer():
    
    signup_customer_form = Signup_Customer_Form()

    if signup_customer_form.validate_on_submit():

        hashed_pw = flask_bcrypt_instance.generate_password_hash(signup_customer_form.password.data).decode('utf-8')

        new_customer = User(name=signup_customer_form.name.data, category="Customer", email=signup_customer_form.email.data, hashed_password=hashed_pw, password=signup_customer_form.password.data, address=signup_customer_form.address.data, pincode=signup_customer_form.pincode.data)

        db.session.add(new_customer)
        
        db.session.commit()         

        flash(f"You've successfully registered as {signup_customer_form.email.data}", 'success')

        return redirect(url_for('home'))
    
    return render_template('routes/forms/signup_customer.html', title='Home', form=signup_customer_form)

def save_pdf_file(pdf):

    pdf_extension = os.path.splitext(pdf.filename)[1]

    random_hex_code_for_pdf = secret
@app.route("/signup-professional", methods=['GET', 'POST'])
def signup_professional():

    signup_professional_form = Signup_Professional_Form()

    if signup_professional_form.validate_on_submit():
        
        hashed_pw = flask_bcrypt_instance.generate_password_hash(signup_professional_form.password.data)
        
        new_professional = User(name=signup_professional_form.name.data, category="Professional", email=signup_professional_form.email.data, hashed_password=hashed_pw, password=signup_professional_form.password.data, address=signup_professional_form.address.data, pincode=signup_professional_form.pincode.data, service_offered=signup_professional_form.service_name.data, description_file=)

    return render_template('routes/forms/signup_professional.html', title='Home', form=signup_professional_form)

@app.route("/login", methods=['GET', 'POST'])
def login():

    login_form = Login_Form();

    if login_form.validate_on_submit():

        user = User.query.filter_by(email=login_form.email.data).first()
    
        authenticated = flask_bcrypt_instance.check_password_hash(user.hashed_password, login_form.password.data)

        if authenticated:
            
            login_user(user, remember=True)

            flash(f'successfully logged in as a {user.category}', 'sucess')

            return redirect(url_for('home'))

    return render_template('routes/forms/login.html', title='Login', form=login_form)

@app.route("/logout", methods=['GET', 'POST'])
def logout():

    logout_user()

    return redirect(url_for('home'))

@app.route("/new-service", methods=['GET', 'POST'])
def new_service():

    new_service_form = New_Service_Form()

    if new_service_form.validate_on_submit():

        new_service = ServiceTypes(name=new_service_form.service_name.data, description=new_service_form.description.data, base_price=new_service_form.base_price.data);

        db.session.add(new_service);

        db.session.commit();

        flash(f'new service :- {new_service.name} created successfully')

        return redirect(url_for('home'));

    return render_template('routes/forms/new_service.html', title='New Service', form=new_service_form)