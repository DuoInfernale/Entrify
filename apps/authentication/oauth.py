from dotenv import load_dotenv
import os
from flask import current_app as app 
from flask_login import current_user, login_user
from flask_dance.consumer import oauth_authorized
from flask_dance.contrib.azure import azure, make_azure_blueprint
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from sqlalchemy.orm.exc import NoResultFound
from apps.config import Config
from .models import Users, db, OAuth
from flask import redirect, url_for
from flask import flash

load_dotenv()

azure_blueprint = make_azure_blueprint(
    client_id=os.getenv('ENTRA_ID'),
    client_secret=os.getenv('ENTRA_SECRET'),
    tenant=os.getenv('AZURE_TENANT'),
    storage=SQLAlchemyStorage(
        OAuth,
        db.session,
        user=current_user,
        user_required=False,        
    ),  
)

@oauth_authorized.connect_via(azure_blueprint)
def azure_logged_in(blueprint, token):
    if not token:
        # print(token)
        flash("Failed to log in with azure.", category="error")
        return False

    resp = blueprint.session.get("/v1.0/me")
    # azure.get
    if not resp.ok:
        # print(resp)
        msg = "Failed to fetch user info from Azure."
        flash(msg, category="error")
        return False

    azure_info = resp.json()
    azure_user_id = str(azure_info["id"])
    # print(azure_user_id)
    # Find this OAuth token in the database, or create it
    query = OAuth.query.filter_by(
        provider=blueprint.name,
        provider_user_id=azure_user_id,
    )
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(
            provider=blueprint.name,
            provider_user_id=azure_user_id,
            token=token,
        )

    if oauth.user:
        login_user(oauth.user)
        flash("Successfully signed in with Azure.")

    else:
        # Create a new local user account for this user
        user = Users(
            # create user with user information from Microsoft Graph
            email=azure_info["mail"],
            username=azure_info["userPrincipalName"],
            surname=azure_info["surname"],
            givenName=azure_info["givenName"]
        )
        # Associate the new local user account with the OAuth token
        oauth.user = user
        # Save and commit our database models
        db.session.add_all([user, oauth])
        db.session.commit()
        # Log in the new local user account
        login_user(user)
        flash("Successfully signed in with Azure.")

    # Disable Flask-Dance's default behavior for saving the OAuth token
    return False