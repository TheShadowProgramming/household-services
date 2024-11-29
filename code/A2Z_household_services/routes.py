from flask import render_template, redirect, url_for, flash, abort;
import os;
import secrets;
import json;
from A2Z_household_services import app, db, flask_bcrypt_instance, login_manager;
from flask_login import current_user, login_user, logout_user, login_required; # type: ignore
from A2Z_household_services.forms import Signup_Customer_Form, Signup_Professional_Form, Login_Form, New_Service_Form, Edit_Service_Form, DatabaseSearchForm;
from A2Z_household_services.models import User, ServiceTypes;

@login_manager.user_loader
def load_user(user_id):

    return User.query.get(user_id);

@app.route("/")
def home():
    services_types = ServiceTypes.query.all();

    professionals = User.query.filter_by(category="Professional", user_blocked=True);

    return render_template('routes/home_content.html', title='Home', current_user=current_user, services_types=services_types, professionals=professionals);

@app.route("/signup-customer", methods=['POST', 'GET'])
def signup_customer():

        signup_customer_form = Signup_Customer_Form();

        if signup_customer_form.validate_on_submit():

            hashed_pw = flask_bcrypt_instance.generate_password_hash(signup_customer_form.password.data).decode('utf-8');

            new_customer = User(name=signup_customer_form.name.data, category="Customer", email=signup_customer_form.email.data, hashed_password=hashed_pw, password=signup_customer_form.password.data, address=signup_customer_form.address.data, pincode=signup_customer_form.pincode.data);

            db.session.add(new_customer);
            
            db.session.commit();         

            flash(f"You've successfully registered as {signup_customer_form.email.data}", 'success');

            return redirect(url_for('home'));
        
        return render_template('routes/forms/signup_customer.html', title='Home', form=signup_customer_form);

def save_pdf_file(pdf):

    pdf_file = pdf.data;

    pdf_extension = os.path.splitext(pdf_file.filename)[1];

    random_hex_code_for_pdf = secrets.token_hex(8);

    new_secret_name = random_hex_code_for_pdf + pdf_extension;

    save_path = os.path.join(app.root_path, 'static/professional_docs', new_secret_name);

    pdf_file.save(save_path);

    return new_secret_name;

@app.route("/signup-professional", methods=['GET', 'POST'])
def signup_professional():

        signup_professional_form = Signup_Professional_Form();

        if signup_professional_form.validate_on_submit():
            
            hashed_pw = flask_bcrypt_instance.generate_password_hash(signup_professional_form.password.data).decode('utf-8');
            
            new_professional = User(name=signup_professional_form.name.data, category="Professional", email=signup_professional_form.email.data, hashed_password=hashed_pw, password=signup_professional_form.password.data, address=signup_professional_form.address.data, pincode=signup_professional_form.pincode.data, service_offered=signup_professional_form.service_name.data, user_blocked=True, description=save_pdf_file(signup_professional_form.upload_files),experience=signup_professional_form.experience.data);

            db.session.add(new_professional);

            db.session.commit();

            flash(f'new professional created successfully with email {signup_professional_form.email.data}', 'success');

            return redirect(url_for('home'));

        return render_template('routes/forms/signup_professional.html', title='Home', form=signup_professional_form);



@app.route("/login", methods=['GET', 'POST'])
def login():

    login_form = Login_Form();

    if login_form.validate_on_submit():

        user = User.query.filter_by(email=login_form.email.data).first();
    
        authenticated = flask_bcrypt_instance.check_password_hash(user.hashed_password, login_form.password.data);

        if authenticated:
            
            login_user(user, remember=True);

            flash(f'successfully logged in as a {user.category}', 'success');

            return redirect(url_for('home'));

    return render_template('routes/forms/login.html', title='Login', form=login_form);

@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():

    logout_user();

    return redirect(url_for('home'));

@app.errorhandler(403)
def already_signedIn_error(error):
    return render_template('errors/403.html', error_message="Forbidden Access")

@app.route("/new-service", methods=['GET', 'POST'])
@login_required
def new_service():
    
    if current_user.category == "Admin":

        new_service_form = New_Service_Form();

        if new_service_form.validate_on_submit():

            new_service = ServiceTypes(name=new_service_form.service_name.data, description=new_service_form.description.data, base_price=new_service_form.base_price.data);

            db.session.add(new_service);

            db.session.commit();

            flash(f'new service :- {new_service.name} created successfully');

            return redirect(url_for('home'));

        return render_template('routes/forms/new_service.html', title='New Service', form=new_service_form);
    
    else:
        abort(403);

@app.route('/approve/<professionalEmail>', methods=['GET', 'POST'])
@login_required
def approve(professionalEmail):

    if current_user.category == "Admin":
        existing_professional = User.query.filter_by(category='Professional', user_blocked=True, email=professionalEmail).first();

        existing_professional.user_blocked = False;

        db.session.commit();

        return redirect(url_for('home'));
    
    else:

        abort(403);

    

@app.route('/edit-service/<serviceId>', methods=['GET', 'POST'])
@login_required
def edit(serviceId):
    
    if current_user.category == "Admin":
        service_form = Edit_Service_Form();

        existing_service = ServiceTypes.query.filter_by(id=serviceId).first();
        
        if service_form.validate_on_submit():
            existing_service.name = service_form.service_name.data;
        
            existing_service.description = service_form.description.data;

            existing_service.base_price = service_form.base_price.data;

            db.session.commit();

            flash(f'{service_form.service_name.data} service updated successfully', 'success');

            return redirect(url_for('home'));

        return render_template('routes/forms/edit_service.html', title='Edit Service', current_user=current_user, form=service_form, existing_service=existing_service);

    else:

        abort(403);

@app.route('/delete/<serviceId>', methods=['GET', 'POST'])
def delete_service(serviceId):

    if current_user.category == "Admin":
        existing_service = ServiceTypes.query.filter_by(id=serviceId).first();

        db.session.delete(existing_service);

        db.session.commit();
        
        flash(f'{existing_service.name} service deleted successfully');

        return redirect(url_for('home'));

    else:

        abort(403);

    

@app.route('/admin-database', methods=['GET', 'POST'])
@login_required
def admin_database():

    if current_user.category == "Admin":
        form = DatabaseSearchForm()

        customers = User.query.filter_by(category="Customer");
        
        professionals = User.query.filter_by(category="Professional");


        if form.validate_on_submit():
            search_attribute = form.search_by.data;

            search_text = form.search_box.data;

            return redirect(url_for('admin_database_search', search_attribute=search_attribute, search_text=search_text))
        
        return render_template('routes/admin_database.html', title='Database', current_user=current_user, form=form, customers=customers, professionals=professionals);
    else:
        
        abort(403);

@app.route('/admin-database/search/<search_attribute>/<search_text>', methods=['GET', 'POST'])
@login_required
def admin_database_search(search_attribute, search_text):

    if current_user.category == "Admin":

        form = DatabaseSearchForm();

        search_attribute=search_attribute;

        search_text=search_text;
    
        filtered_customers = User.query.filter_by(**{"category":"Customer", search_attribute:search_text});

        filtered_professionals = User.query.filter_by(**{"category": "Professional", search_attribute: search_text});

        if form.validate_on_submit():

            search_attribute = form.search_by.data;
        
            search_text = form.search_box.data;
        
            return redirect(url_for('admin_database'));
        return render_template('routes/admin_database_search.html', title='Database', current_user=current_user, form=form, filtered_customers=filtered_customers, filtered_professionals=filtered_professionals);

    else:
        abort(403)

@app.route('/block_user/<userId>/<status>')
@login_required
def block_user(userId, status):
    if current_user.category == "Admin":

        bool_status = json.loads(status);

        existing_user = User.query.filter_by(id=userId).first();

        existing_user.user_blocked = bool_status;

        db.session.commit();

        flash(f'updated the blocked status of {existing_user.email}', 'success');

        return redirect(url_for('admin_database'));

    else:

        abort(403);

