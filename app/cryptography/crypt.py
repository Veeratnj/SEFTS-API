from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

load_dotenv()

# Replace this with your actual encryption key
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')  # Generate this key securely and keep it safe

# Initialize Fernet with the encryption key
fernet = Fernet(ENCRYPTION_KEY)

def encrypt(data: str) -> str:
    """
    Encrypts a string using Fernet symmetric encryption.

    :param data: The string to encrypt
    :return: The encrypted string
    """
    encrypted_bytes = fernet.encrypt(data.encode())
    return encrypted_bytes.decode()

def decrypt(encrypted_data: str) -> str:
    """
    Decrypts a string encrypted with Fernet symmetric encryption.

    :param encrypted_data: The encrypted string to decrypt
    :return: The decrypted string
    """
    print('encrypted_data',encrypted_data)
    decrypted_bytes = fernet.decrypt(encrypted_data.encode())
    print('decrypted_bytes',decrypted_bytes)
    return decrypted_bytes.decode()


# from cryptography.fernet import Fernet

# key = Fernet.generate_key()
# print(key.decode())  