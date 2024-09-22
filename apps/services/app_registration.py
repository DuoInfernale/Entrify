from azure.identity.aio import ClientSecretCredential
from msgraph import GraphServiceClient
import asyncio
from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import sessionmaker
import os
from apps.home.models import Customer
from cryptography.fernet import Fernet
from apps.home.models import Customer, Application, PasswordCredential
from datetime import datetime, timezone
from sqlalchemy.dialects.mysql import insert
from sqlalchemy import and_
import logging

# Configure the logger
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Database Configuration
DB_ENGINE = os.getenv('DB_ENGINE', '')
DB_USERNAME = os.getenv('DB_USERNAME', '')
DB_PASS = os.getenv('DB_PASS', '')
DB_HOST = os.getenv('DB_HOST', '')
DB_PORT = os.getenv('DB_PORT', '')
DB_NAME = os.getenv('DB_NAME', '')

# Set up the SQLALCHEMY_DATABASE_URI
SQLALCHEMY_DATABASE_URI = f"{DB_ENGINE}://{DB_USERNAME}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Function to fetch credentials from the database
def fetch_credentials():
    engine = create_engine(SQLALCHEMY_DATABASE_URI)  # Update with your DB details
    Session = sessionmaker(bind=engine)
    session = Session()
    
    credentials = session.execute(select(Customer)).scalars().first()  # Fetch the first row
    session.close()

    # Decrypt the client_secret
    key = os.getenv('ENCRYPTION_KEY').encode()
    cipher = Fernet(key)
    decrypted_client_secret = cipher.decrypt(credentials.client_secret.encode()).decode()
    
    return credentials.tenant_id, credentials.client_id, decrypted_client_secret  # Adjust based on your model attributes

# Fetch the credentials from the database
tenant_id, client_id, client_secret = fetch_credentials()  # Update to get values from the database

# Define the scopes
scopes = ['https://graph.microsoft.com/.default']

# Create the credential object
credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret
)

# Initialize the Graph client
graph_client = GraphServiceClient(credential, scopes)  # type: ignore

# Function to fetch applications from Microsoft Graph API
async def fetch_applications():
    result = await graph_client.applications.get()
    applications_info = []
    for app in result.value:
        app_info = {
            "Application": {
                "odata_type": app.odata_type,
                "app_id": app.app_id,
                "display_name": app.display_name,
            },
            "password_credentials": []
        }
        
        if app.password_credentials:
            for credential in app.password_credentials:
                app_info["password_credentials"].append({
                    "PasswordCredential": {
                        "additional_data": credential.additional_data,
                        "display_name": credential.display_name,
                        "end_date_time": credential.end_date_time,
                        "key_id": credential.key_id,
                    }
                })
        
        applications_info.append(app_info)
    return applications_info

# Function to store applications in the database
def store_applications(applications_info):
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Get existing applications from the database
        existing_apps = session.execute(select(Application)).scalars().all()
        existing_app_ids = {app.app_id for app in existing_apps}  # Set of existing app IDs

        for app in applications_info:
            app_id = app["Application"]["app_id"]
            # Check if the application already exists
            existing_app = session.execute(select(Application).where(Application.app_id == app_id)).scalars().first()
            if existing_app:
                # Update display_name if it has changed
                if existing_app.display_name != app["Application"]["display_name"]:
                    existing_app.display_name = app["Application"]["display_name"]
                existing_app_ids.discard(app_id)  # Remove from existing IDs
                continue  # Skip if the application already exists
            
            # Create a new Application instance
            new_app = Application(
                app_id=app_id,
                odata_type=app["Application"]["odata_type"],
                display_name=app["Application"]["display_name"],
            )
            session.add(new_app)  # Add the application to the session

        # Delete applications that are no longer in the applications_info
        for app_id in existing_app_ids:
            app_to_delete = session.execute(select(Application).where(Application.app_id == app_id)).scalars().first()
            if app_to_delete:
                session.delete(app_to_delete)  # Delete the application

        session.commit()  # Commit the transaction
        print("Applications stored successfully.")  # Debugging statement
    except Exception as e:
        session.rollback()  # Rollback in case of error
        print(f"Error storing applications: {e}")  # Print the error
    finally:
        session.close()  # Ensure the session is closed

# Function to store password credentials in the database
def store_password_credentials(applications_info):
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        all_current_key_ids = set()
        all_current_app_ids = set()

        for app in applications_info:
            app_id = app["Application"]["app_id"]
            all_current_app_ids.add(app_id)
            
            for cred in app["password_credentials"]:
                key_id = cred["PasswordCredential"]["key_id"]
                all_current_key_ids.add(key_id)
                end_date_time = cred["PasswordCredential"]["end_date_time"]
                
                # Convert end_date_time to datetime if it's not already
                if isinstance(end_date_time, str):
                    end_date_time = datetime.fromisoformat(end_date_time)
                elif not isinstance(end_date_time, datetime):
                    end_date_time = datetime.now(timezone.utc)

                # Prepare the data for upsert
                data = {
                    "key_id": key_id,
                    "application_id": app_id,
                    "additional_data": cred["PasswordCredential"].get("additional_data", "{}"),
                    "display_name": cred["PasswordCredential"]["display_name"],
                    "end_date_time": end_date_time
                }

                # Perform upsert operation
                stmt = insert(PasswordCredential).values(**data)
                stmt = stmt.on_duplicate_key_update(**data)
                session.execute(stmt)

        # Convert UUIDs to strings for comparison
        all_current_key_ids_str = {str(key_id) for key_id in all_current_key_ids}

        # Delete password credentials that are not associated with current key IDs
        delete_stmt = PasswordCredential.__table__.delete().where(
            ~PasswordCredential.key_id.in_(all_current_key_ids_str)  # Match against key_id as string
        )
        deleted_count = session.execute(delete_stmt).rowcount

        # Commit the changes
        session.commit()
        print("Secrets stored successfully.")

    except Exception as e:
        session.rollback()
        logger.error(f"Error storing password credentials: {str(e)}")  # Log the error
    finally:
        session.close()

# Main execution block
if __name__ == "__main__":
    async def main():
        applications = await fetch_applications()
        store_applications(applications)
        store_password_credentials(applications)

    # Run the main function
    asyncio.run(main())