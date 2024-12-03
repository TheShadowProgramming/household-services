from flask import render_template, redirect, url_for, flash, abort, request;
import os;
import secrets;
import json;
from A2Z_household_services import app, db, flask_bcrypt_instance, login_manager;
from flask_login import current_user, login_user, logout_user, login_required; # type: ignore
from A2Z_household_services.forms import Signup_Customer_Form, Signup_Professional_Form, Login_Form, New_Service_Form, Edit_Service_Form, DatabaseSearchForm, ProfessionalPortfolioForm, CustomerProposalForm, CustomerReviewForm;
from A2Z_household_services.models import User, ServiceTypes, Service_requests_central, Service_requests_customer, Service_requests_professional, Professional_portfolio;

def non_blocked_required():
    
    if current_user.user_blocked == True:

        abort(403);

    else:

        return True;

def check_customer_category():
    if current_user.category == "Customer":
        return True;
    else:
        abort(403);

def check_professional_category():
    if current_user.category == "Professional":
        return True;
    else:
        abort(403);

def check_admin_category():
    if current_user.category == "Admin":
        return True;
    else:
        abort(403);

@app.errorhandler(403)
def already_signedIn_error(error):
    return render_template('errors/403.html', error_message="Forbidden Access");

@app.errorhandler(404)
def cant_book_another_service(error):
    return render_template('errors/403.html', error_message="Forbidden Access");

@login_manager.user_loader
def load_user(user_id):

    return User.query.get(user_id);

@app.route("/")
def home():
    services_types = ServiceTypes.query.all();

    professionals = User.query.filter_by(category="Professional", user_blocked=True);

    service_requests_open = []
    service_requests_closed = []
    service_requests_pending = []

    if current_user.is_authenticated:

        non_blocked_required()

        service_requests_pending = Service_requests_central.query.filter_by(professional_id=current_user.id, service_status="Pending")

        service_requests_open = Service_requests_central.query.filter_by(professional_id=current_user.id, service_status="Open");

        service_requests_closed = Service_requests_central.query.filter_by(professional_id=current_user.id, service_status="Closed");

    return render_template('routes/home_content.html', title='Home', current_user=current_user, services_types=services_types, professionals=professionals, service_requests_pending=service_requests_pending, service_requests_open=service_requests_open, service_requests_closed=service_requests_closed);

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

@app.route("/new-service", methods=['GET', 'POST'])
@login_required
def new_service():

        check_admin_category()        

        new_service_form = New_Service_Form();

        if new_service_form.validate_on_submit():

            new_service = ServiceTypes(name=new_service_form.service_name.data, description=new_service_form.description.data, base_price=new_service_form.base_price.data);

            db.session.add(new_service);

            db.session.commit();

            flash(f'new service :- {new_service.name} created successfully');

            return redirect(url_for('home'));

        return render_template('routes/forms/new_service.html', title='New Service', form=new_service_form);

@app.route('/approve/<professionalEmail>', methods=['GET', 'POST'])
@login_required
def approve(professionalEmail):

        check_admin_category()
    
        existing_professional = User.query.filter_by(category='Professional', user_blocked=True, email=professionalEmail).first();

        existing_professional.user_blocked = False;

        db.session.commit();

        return redirect(url_for('home'));
    

@app.route('/edit-service/<serviceId>', methods=['GET', 'POST'])
@login_required
def edit(serviceId):

        check_admin_category()
    
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


@app.route('/delete/<serviceId>', methods=['GET', 'POST'])
def delete_service(serviceId):
        check_admin_category()

        existing_service = ServiceTypes.query.filter_by(id=serviceId).first();

        db.session.delete(existing_service);

        db.session.commit();
        
        flash(f'{existing_service.name} service deleted successfully');

        return redirect(url_for('home'));

    

@app.route('/admin-database', methods=['GET', 'POST'])
@login_required
def admin_database():
        check_admin_category()
    
        form = DatabaseSearchForm()

        customers = User.query.filter_by(category="Customer");
        
        professionals = User.query.filter_by(category="Professional");

        all_services = Service_requests_central.query.all();

        if form.validate_on_submit():
            search_attribute = form.search_by.data;

            search_text = form.search_box.data;

            return redirect(url_for('admin_database_search', search_attribute=search_attribute, search_text=search_text))
        
        return render_template('routes/admin_database.html', title='Database', current_user=current_user, form=form, customers=customers, professionals=professionals, all_services=all_services);

@app.route('/admin-database/search/<search_attribute>/<search_text>', methods=['GET', 'POST'])
@login_required
def admin_database_search(search_attribute, search_text):

        check_admin_category()

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


@app.route('/block_user/<userId>/<status>')
@login_required
def block_user(userId, status):
        check_admin_category()

        bool_status = json.loads(status);

        existing_user = User.query.filter_by(id=userId).first();

        existing_user.user_blocked = bool_status;

        db.session.commit();

        flash(f'updated the blocked status of {existing_user.email}', 'success');

        return redirect(url_for('admin_database'));

@app.route('/professional-portfolio', methods=['GET', 'POST'])
@login_required
def professional_portfolio():
        non_blocked_required()

        check_professional_category()
            
        form = ProfessionalPortfolioForm();

        if form.validate_on_submit():

            professional_portfolio = Professional_portfolio.query.filter_by(professional_id=current_user.id).first();

            current_user.service_offered = form.service_category_change.data;


            if professional_portfolio:
                
                professional_portfolio.professional_portfolio = form.service_portfolio.data;

                professional_portfolio.professional_id = current_user.id

            else:

                professional_portfolio = Professional_portfolio(professional_id=current_user.id, professional_portfolio=form.service_portfolio.data);
            
                db.session.add(professional_portfolio)
            
            db.session.commit();

            flash('Updated Portfolio Successfully', 'success');
            
            return redirect(url_for('professional_portfolio'));
                
        elif request.method == 'GET':
            portfolio_description = Professional_portfolio.query.filter_by(professional_id=current_user.id).first();

            service_type = ServiceTypes.query.filter_by(name=current_user.service_offered).first();

            base_price = service_type.base_price;

            if portfolio_description:
                
                form.service_portfolio.data = portfolio_description.professional_portfolio;


        return render_template('routes/forms/professional_portfolio.html', title="Professional", current_user=current_user, form=form, base_price=base_price);
            

@app.route('/accept-reject-service/<serviceId>/<status>', methods=['GET', 'POST'])
@login_required
def accept_or_reject_service(serviceId, status):
        non_blocked_required()

        check_professional_category()

        service_request = Service_requests_central.query.filter_by(service_id=serviceId).first();

        service_request.service_status = status;
    
        db.session.commit()

        return redirect(url_for('home'));

@app.route('/customer/search/<service_category>', methods=['GET', 'POST'])
@login_required
def customer_search(service_category):
        non_blocked_required()

        check_customer_category()

        service_category_filter = ServiceTypes.query.filter_by(name=service_category).first();

        filtered_professionals = User.query.filter_by(service_offered=service_category);

        for professional in filtered_professionals:
            professional_portfolio = Professional_portfolio.query.filter_by(professional_id=professional.id).first();

            if professional_portfolio.professional_portfolio:
                professional.professional_portfolio = str(professional_portfolio.professional_portfolio);
        
            else: 
                professional.professional_portfolio = ""

        return render_template('routes/customer_search.html', title='Customer Search', service_category=service_category_filter, filtered_professionals=filtered_professionals);

@app.route('/book-service/<professional_id>', methods=['GET', 'POST'])
@login_required
def book_service(professional_id):
    
            non_blocked_required()

            check_customer_category()

            variable_professional_id = professional_id
            
            form = CustomerProposalForm();

            professional = User.query.filter_by(id=variable_professional_id).first();

            existing_service = Service_requests_central.query.filter_by(customer_id=current_user.id, professional_id=professional.id).first();

            if (not existing_service) or (existing_service and (existing_service.service_status == "Closed" or existing_service.service_status == "Rejected")):

                if form.validate_on_submit():

                        new_service_request = Service_requests_central(service_category=professional.service_offered, service_price=form.negotiated_price.data, service_status="Pending", customer_id=current_user.id, professional_id=professional.id, customer_pincode=current_user.pincode, professional_pincode=professional.pincode, service_review=form.proposal_message.data)

                        db.session.add(new_service_request);
                    
                        db.session.commit();

                        flash(f'Booked Service for {new_service_request.service_category} category', 'success')
                    
                        return redirect(url_for('home'))

                return render_template('routes/forms/customer_proposal.html', title="Book Service", current_user=current_user, form=form, professional=professional);
        
            else:
                        
                flash(f'Already sent a request to the professional with id :- {professional.id}')

                return redirect(url_for('customer_search', service_category=professional.service_offered))

@app.route('/customer-database', methods=['GET', 'POST'])
@login_required
def customer_database():
        non_blocked_required()

        check_customer_category()

        all_services = Service_requests_central.query.all();

        updated_services_all = []

        updated_services_open = []

        for service in all_services:

            if service.customer_id == current_user.id and service.service_status == "Open":

                professional = User.query.filter_by(id=service.professional_id).first();
    
                service.professional_name = professional.name;
    
                updated_services_open.append(service);
            
            elif service.customer_id == current_user.id:

                professional = User.query.filter_by(id=service.professional_id).first();
    
                service.professional_name = professional.name;
    
                updated_services_all.append(service);

        
        return render_template('routes/customer_database.html', title="Customer Database", current_user=current_user, service_requests=updated_services_all, service_requests_open=updated_services_open)

@app.route('/close-service/<serviceId>', methods=['GET', 'POST'])
@login_required
def close_service(serviceId):
        non_blocked_required()

        check_customer_category()
        
        form = CustomerReviewForm();

        service_to_close = Service_requests_central.query.filter_by(service_id=serviceId).first();

        professional = User.query.filter_by(id=service_to_close.professional_id).first()

        if form.validate_on_submit():

            service_to_close.service_status = "Closed";

            service_to_close.service_review = form.review_message.data + f" {form.rating.data} star review";

            db.session.commit();
        
            flash('Successfully posted review', 'success')

            return redirect(url_for('home'))
    
        return render_template('routes/forms/customer_review.html', title="Review", current_user=current_user, service_to_close=service_to_close, professional=professional, form=form)
