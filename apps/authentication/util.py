import os
import hashlib
import binascii
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Inspiration -> https://www.vitoshacademy.com/hashing-passwords-in-python/

# Load environment variables from .env file
load_dotenv()

def hash_pass(password):
    """Hash a password for storing."""

    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash)  # return bytes


def verify_pass(provided_password, stored_password):
    """Verify a stored password against one provided by user"""

    stored_password = stored_password.decode('ascii')
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

# Generate a key (do this once and store it securely)
# key = Fernet.generate_key()
# print(key.decode())  # Save this key securely

# Use the key you generated above
# Ensure the key is set correctly
key = os.getenv('ENCRYPTION_KEY')  # Make sure this environment variable is set
if key is None:
    raise ValueError("ENCRYPTION_KEY environment variable is not set.")
cipher = Fernet(key)

def encrypt_client_secret(client_secret):
    return cipher.encrypt(client_secret.encode()).decode()

def decrypt_client_secret(encrypted_client_secret):
    return cipher.decrypt(encrypted_client_secret.encode()).decode()