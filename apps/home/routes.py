# Import necessary modules and functions
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from jinja2 import TemplateNotFound

from apps import db
from apps.home import blueprint
from apps.home.models import Customer, Application, PasswordCredential, EnterpriseApplication, SAMLCertificate
from apps.authentication.util import encrypt_client_secret

# Route for the index page
@blueprint.route('/index')
@login_required
def index():
    """Renders the index page"""
    return render_template('home/index.html', segment='index')

# Route for rendering templates based on URL path
@blueprint.route('/<template>')
@login_required
def route_template(template):
    """Route to render a template based on the URL path"""
    if not template.endswith('.html'):
        template += '.html'

    segment = get_segment(request)

    try:
        return render_template(f"home/{template}", segment=segment)
    except TemplateNotFound:
        return render_template('home/page-404.html'), 404
    except Exception:
        return render_template('home/page-500.html'), 500

# API route for adding a new customer
@blueprint.route('/api/add-customer', methods=['POST'])
def api_post_add_customer():
    """Route to add a new customer"""
    customer_name = request.form.get('customerName')
    customer_short = request.form.get('customerShort')
    tenant_id = request.form.get('tenantId')
    client_id = request.form.get('clientId')
    client_secret = request.form.get('clientSecret')

    # Check if any customer already exists
    existing_customer = Customer.query.first()
    if existing_customer:
        flash('Only one customer is allowed!', 'danger')
        return redirect(url_for('home_blueprint.add_customer'))

    if not customer_name:
        flash('Customer Name is required!', 'danger')
        return redirect(url_for('home_blueprint.add_customer'))

    # Encrypt the client secret
    encrypted_client_secret = encrypt_client_secret(client_secret)

    new_customer = Customer(
        name=customer_name,
        short_name=customer_short,
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=encrypted_client_secret
    )
    db.session.add(new_customer)
    db.session.commit()

    flash('Customer added successfully!', 'success')
    return redirect(url_for('home_blueprint.index'))

# API route for getting all customers
@blueprint.route('/api/customers', methods=['GET'])
def api_get_customers():
    """API endpoint to get all customers"""
    customers = Customer.query.all()
    customers_list = [{"id": c.id, "name": c.name, "short_name": c.short_name, "tenant_id": c.tenant_id, "client_id": c.client_id} for c in customers]
    return jsonify(customers_list)

# API route for deleting a customer
@blueprint.route('/api/delete-customer/<int:customer_id>', methods=['DELETE'])
@login_required
def api_delete_customer(customer_id):
    """API endpoint to delete a customer"""
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return '', 204

# API route for getting the count of customers
@blueprint.route('/api/customers/count', methods=['GET'])
def api_get_customers_count():
    """API endpoint to get the count of customers"""
    count = Customer.query.count()
    return jsonify(count=count)

# Route for rendering the customers list page
@blueprint.route('/customers')
@login_required
def customers():
    """Renders the customers list page"""
    return render_template('home/customers.html', segment='customers')

# Route for rendering the add-customer page
@blueprint.route('/add-customer')
@login_required
def add_customer():
    """Renders the add-customer page"""
    return render_template('home/add_customer.html', segment='add-customer')

# API route for getting applications and their password credentials
@blueprint.route('/api/applications', methods=['GET'])
def api_get_applications():
    """API endpoint to get applications and their password credentials"""
    applications = Application.query.all()
    result = []
    for app in applications:
        app_data = {
            "app_id": app.app_id,
            "display_name": app.display_name,
            "password_credentials": [{
                "key_id": cred.key_id,
                "display_name": cred.display_name,
                "end_date_time": cred.end_date_time.isoformat() if cred.end_date_time else None
            } for cred in app.password_credentials]
        }
        result.append(app_data)
    return jsonify(result)

# API route for getting the count of app registrations
@blueprint.route('/api/applications/count', methods=['GET'])
def api_get_app_registrations_count():
    """API endpoint to get the count of app registration secrets"""
    count = Application.query.count()
    return jsonify(count=count)

# API route for getting the count of applications with expiring secrets
@blueprint.route('/api/applications/expiring-soon/count', methods=['GET'])
def api_get_applications_expiring_soon_count():
    """API endpoint to get the count of applications with secrets expiring in less than 30 days"""
    from datetime import datetime, timedelta

    threshold_date = datetime.now() + timedelta(days=30)
    count = Application.query.filter(
        Application.password_credentials.any(PasswordCredential.end_date_time < threshold_date)
    ).count()

    return jsonify(count=count)

# Route for rendering the app-registrations page
@blueprint.route('/app-registrations')
@login_required
def add_registrations():
    """Renders the app-registrations page"""
    return render_template('home/app_registrations.html', segment='app-registrations')

# Route for rendering the enterprise applications page
@blueprint.route('/enterprise-applications')
@login_required
def enterprise_applications():
    """Renders the enterprise applications page"""
    return render_template('home/enterprise_applications.html', segment='enterprise-applications')

# API route for getting enterprise applications and their SAML certificates
@blueprint.route('/api/enterprise-applications', methods=['GET'])
def api_get_enterprise_applications():
    """API endpoint to get enterprise applications and their SAML certificates"""
    enterprise_apps = EnterpriseApplication.query.all()
    result = []
    for app in enterprise_apps:
        app_data = {
            "app_id": app.app_id,
            "display_name": app.display_name,
            "saml_certificate": [{
                "key_id": cert.key_id,
                "certificate_display_name": cert.certificate_display_name,
                "end_date_time": cert.end_date_time.isoformat() if cert.end_date_time else None
            } for cert in app.saml_certificate]
        }
        result.append(app_data)
    return jsonify(result)

# API route for getting the count of enterprise applications
@blueprint.route('/api/enterprise-applications/count', methods=['GET'])
def api_get_enterprise_applications_count():
    """API endpoint to get the count of enterprise applications"""
    count = SAMLCertificate.query.count()
    return jsonify(count=count)

# API route for getting the count of expiring SAML certificates
@blueprint.route('/api/enterprise-applications/expiring-soon/count', methods=['GET'])
def api_get_saml_certificates_expiring_soon_count():
    """API endpoint to get the count of SAML certificates expiring in less than 30 days"""
    from datetime import datetime, timedelta

    threshold_date = datetime.now() + timedelta(days=30)
    count = SAMLCertificate.query.filter(
        SAMLCertificate.end_date_time < threshold_date
    ).count()

    return jsonify(count=count)

# Helper function to extract the current page name from the request
def get_segment(request):
    """
    Helper function to extract the current page name from the request.
    
    Parameters:
    - request: The Flask request object.

    Returns:
    - segment (str): The name of the current page or 'index' if the path is empty.
    """
    try:
        segment = request.path.split('/')[-1]
        return segment if segment else 'index'
    except Exception:
        return None
