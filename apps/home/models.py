from apps import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    short_name = db.Column(db.String(64))
    tenant_id = db.Column(db.String(128), nullable=False)
    client_id = db.Column(db.String(128), nullable=False)
    client_secret = db.Column(db.String(255), nullable=False)

class Application(db.Model):
    app_id = db.Column(db.String(128), primary_key=True)
    odata_type = db.Column(db.String(128), nullable=False)
    display_name = db.Column(db.String(256), nullable=False)
    password_credentials = db.relationship('PasswordCredential', backref='application', lazy=True)

class PasswordCredential(db.Model):
    key_id = db.Column(db.String(128), primary_key=True)
    application_id = db.Column(db.String(128), db.ForeignKey('application.app_id'), nullable=False)
    additional_data = db.Column(db.JSON)
    display_name = db.Column(db.String(256), nullable=False)
    end_date_time = db.Column(db.DateTime, nullable=False)

class EnterpriseApplication(db.Model):
    app_id = db.Column(db.String(128), primary_key=True)
    display_name = db.Column(db.String(256), nullable=False)
    saml_certificate = db.relationship('SAMLCertificate', backref='enterprise_application', lazy=True)

class SAMLCertificate(db.Model):
    key_id = db.Column(db.String(128), primary_key=True)
    certificate_display_name = db.Column(db.String(256), nullable=False)
    end_date_time = db.Column(db.DateTime, nullable=False)
    enterprise_application_id = db.Column(db.String(128), db.ForeignKey('enterprise_application.app_id'), nullable=False)  # {{ edit_1 }}
