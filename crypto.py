#Import the class PasswordHasher from the argon2 library
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

#Import libraries for encryption
import base64, hashlib
from cryptography.fernet import Fernet


#Creates one PasswordHasher object that can be reused
hasher = PasswordHasher()

def hash_password(password):
    #Hashes password with Argon2 and returns salt+hash in one string
    return hasher.hash(password)

def verify_password(password, password_hash):
    #Verifies plain password against stored hash
    try:
        hasher.verify(password_hash, password)
        return True
    except VerifyMismatchError:
        return False

#Creates the function derive_key
#Runs SHA-256 on username_password. This creates a 32 byte digest
#Encodes the digest with base64 because Fernet expects 32 byte
#Returned a URL-safe base64 string
def derive_key(username_password):
    key_digest_bytes = hashlib.sha256(username_password.encode()).digest()
    return base64.urlsafe_b64encode(key_digest_bytes)


#Creates the function encrypt_password
#Encrypts application_password and returns cipher text
def encrypt_password(application_password, username_password):
    cipher = Fernet(derive_key(username_password))
    return cipher.encrypt(application_password.encode()).decode()


#Creates the function decrypt_password
#Decrypts cipher text back to plain text using the same username_password
def decrypt_password(cipher_text, username_password):
    cipher = Fernet(derive_key(username_password))
    return cipher.decrypt(cipher_text.encode()).decode()
